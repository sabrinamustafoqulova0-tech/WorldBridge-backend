import secrets
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_db
from models.user import User
from schemas.auth import AccessToken, Token, TokenRefresh
from schemas.user import UserCreate, UserResponse
from services.auth_service import AuthService
from utils.dependencies import get_current_active_user
from utils.jwt import create_access_token, create_refresh_token, decode_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])

_GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
_GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
_GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user account."""
    svc = AuthService(db)
    existing = await svc.get_user_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await svc.create_user(payload)
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Login with email + password (OAuth2 form). Returns access & refresh tokens."""
    svc = AuthService(db)
    user = await svc.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/refresh", response_model=AccessToken)
async def refresh_token(payload: TokenRefresh, db: AsyncSession = Depends(get_db)):
    """Exchange a valid refresh token for a new access token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
    )
    try:
        data = decode_token(payload.refresh_token)
        if data.get("type") != "refresh":
            raise credentials_exception
        user_id = int(data["sub"])
    except (JWTError, KeyError, ValueError):
        raise credentials_exception

    svc = AuthService(db)
    user = await svc.get_user_by_id(user_id)
    if not user or not user.is_active:
        raise credentials_exception
    return AccessToken(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    """Return the currently authenticated user's profile."""
    return current_user


@router.get("/google")
async def google_login():
    """Redirect browser to Google's OAuth consent screen."""
    redirect_uri = f"{settings.BACKEND_URL}/api/v1/auth/google/callback"
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }
    return RedirectResponse(f"{_GOOGLE_AUTH_URL}?{urlencode(params)}")


@router.get("/google/callback")
async def google_callback(
    code: str | None = None,
    error: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Handle Google OAuth callback: exchange code → tokens → find/create user → redirect to frontend."""
    if error or not code:
        return RedirectResponse(f"{settings.FRONTEND_URL}/login?error=oauth_cancelled")

    redirect_uri = f"{settings.BACKEND_URL}/api/v1/auth/google/callback"

    async with httpx.AsyncClient() as client:
        # Exchange authorization code for Google access token
        token_resp = await client.post(
            _GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        if token_resp.status_code != 200:
            return RedirectResponse(f"{settings.FRONTEND_URL}/login?error=oauth_failed")

        google_access_token = token_resp.json().get("access_token")
        if not google_access_token:
            return RedirectResponse(f"{settings.FRONTEND_URL}/login?error=oauth_failed")

        # Fetch user profile from Google
        userinfo_resp = await client.get(
            _GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {google_access_token}"},
        )
        if userinfo_resp.status_code != 200:
            return RedirectResponse(f"{settings.FRONTEND_URL}/login?error=oauth_failed")

        profile = userinfo_resp.json()

    email: str = profile.get("email", "")
    if not email:
        return RedirectResponse(f"{settings.FRONTEND_URL}/login?error=oauth_no_email")

    svc = AuthService(db)
    user = await svc.get_user_by_email(email)

    if user is None:
        # Auto-register with a random unusable password
        user = User(
            email=email,
            full_name=profile.get("name") or email.split("@")[0],
            hashed_password=hash_password(secrets.token_urlsafe(32)),
            avatar_url=profile.get("picture"),
            is_active=True,
            is_admin=False,
        )
        db.add(user)
        await db.flush()
        await db.refresh(user)
    elif not user.is_active:
        return RedirectResponse(f"{settings.FRONTEND_URL}/login?error=account_disabled")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return RedirectResponse(
        f"{settings.FRONTEND_URL}/auth/callback"
        f"?access_token={access_token}&refresh_token={refresh_token}"
    )
