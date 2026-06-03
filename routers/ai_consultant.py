import uuid
import re
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from utils.dependencies import get_current_active_user
from models.user import User
from models.ai_chat import AIChatMessage
from database import get_db

router = APIRouter(prefix="/ai", tags=["AI Consultant"])


# ── Request / Response Schemas ──────────────────────────────────────────────

class StartSessionResponse(BaseModel):
    session_id: str
    message: str


class ChatMessageRequest(BaseModel):
    session_id: str
    content: str


class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    chat_type: str
    session_id: str
    created_at: datetime


class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessageResponse]


class CountryRecommendation(BaseModel):
    slug: str
    name: str
    flag: str
    match_score: int
    reason: str
    top_programs: List[str]


class AIRecommendationReport(BaseModel):
    recommended_countries: List[CountryRecommendation]
    success_chance: int
    next_steps: List[str]
    summary: str


# ── Static Data ─────────────────────────────────────────────────────────────

LANG_SCORES = {"none": 0, "a1": 1, "a2": 2, "b1": 3, "b2": 4, "c1": 5, "c2": 6}
EDU_SCORES = {"school": 1, "college": 2, "bachelor": 3, "master": 4, "phd": 5}
BUDGET_SCORES = {"low": 1, "medium": 2, "high": 3}

COUNTRY_PROFILES = {
    "de": {
        "name": "Германия", "flag": "🇩🇪",
        "min_german": 2, "min_english": 0, "min_age": 16, "max_age": 45,
        "programs": ["Ausbildung", "FSJ", "Au Pair", "Studium", "Arbeit"],
        "budget": "medium"
    },
    "fr": {
        "name": "Франция", "flag": "🇫🇷",
        "min_german": 0, "min_english": 2, "min_age": 18, "max_age": 40,
        "programs": ["Au Pair", "Study", "Erasmus+", "Seasonal Work"],
        "budget": "medium"
    },
    "be": {
        "name": "Бельгия", "flag": "🇧🇪",
        "min_german": 0, "min_english": 2, "min_age": 18, "max_age": 40,
        "programs": ["Au Pair", "Work", "Study", "Internship"],
        "budget": "medium"
    },
    "ch": {
        "name": "Швейцария", "flag": "🇨🇭",
        "min_german": 1, "min_english": 2, "min_age": 18, "max_age": 40,
        "programs": ["Hotel Internship", "Study", "Au Pair", "Seasonal Work"],
        "budget": "high"
    },
    "at": {
        "name": "Австрия", "flag": "🇦🇹",
        "min_german": 2, "min_english": 0, "min_age": 16, "max_age": 40,
        "programs": ["Ausbildung", "Au Pair", "Work & Study", "Seasonal"],
        "budget": "medium"
    },
    "pl": {
        "name": "Польша", "flag": "🇵🇱",
        "min_german": 0, "min_english": 1, "min_age": 18, "max_age": 50,
        "programs": ["Factory Jobs", "Warehouse", "Study", "Work Visa"],
        "budget": "low"
    },
    "cz": {
        "name": "Чехия", "flag": "🇨🇿",
        "min_german": 0, "min_english": 1, "min_age": 18, "max_age": 45,
        "programs": ["Free Education", "Work", "Language", "Student Visa"],
        "budget": "low"
    },
    "ca": {
        "name": "Канада", "flag": "🇨🇦",
        "min_german": 0, "min_english": 3, "min_age": 18, "max_age": 45,
        "programs": ["Study Permit", "Work Permit", "Express Entry", "Co-op"],
        "budget": "high"
    },
    "us": {
        "name": "США", "flag": "🇺🇸",
        "min_german": 0, "min_english": 3, "min_age": 18, "max_age": 30,
        "programs": ["Work & Travel", "Au Pair", "Camp America", "Internship"],
        "budget": "high"
    },
}


# ── AI Brain Logic ──────────────────────────────────────────────────────────

def compute_score(age: int, education: str, english_level: str, german_level: str, budget: str, profile: dict) -> int:
    score = 0
    eng = LANG_SCORES.get(english_level.lower(), 0)
    ger = LANG_SCORES.get(german_level.lower(), 0)
    edu = EDU_SCORES.get(education.lower(), 1)
    budget_val = BUDGET_SCORES.get(budget.lower(), 1)
    req_budget_val = BUDGET_SCORES.get(profile["budget"], 2)

    # Language match
    if eng >= profile["min_english"]:
        score += 25
    if ger >= profile["min_german"]:
        score += 20

    # Age match
    if profile["min_age"] <= age <= profile["max_age"]:
        score += 20

    # Budget
    if budget_val >= req_budget_val:
        score += 15
    elif budget_val == req_budget_val - 1:
        score += 7

    # Education
    score += min(edu * 3, 10)

    return min(score, 100)


def generate_recommendations(age: int, education: str, english_level: str, german_level: str, budget: str, desired_country: Optional[str] = None) -> dict:
    results = []
    eng_score = LANG_SCORES.get(english_level.lower(), 0)
    ger_score = LANG_SCORES.get(german_level.lower(), 0)
    edu_score = EDU_SCORES.get(education.lower(), 1)

    for slug, profile in COUNTRY_PROFILES.items():
        if desired_country and desired_country != "any" and desired_country.lower() != slug:
            continue
        score = compute_score(age, education, english_level, german_level, budget, profile)
        if score >= 30:
            # build reason
            reasons = []
            if ger_score >= profile["min_german"] and profile["min_german"] > 0:
                reasons.append("уровень немецкого подходит")
            if eng_score >= profile["min_english"] and profile["min_english"] > 0:
                reasons.append("уровень английского достаточен")
            if profile["min_age"] <= age <= profile["max_age"]:
                reasons.append(f"возраст ({age} лет) входит в диапазон")
            if not reasons:
                reasons.append("базовые критерии соблюдены")
            reason = "Подходит: " + ", ".join(reasons)
            
            results.append(CountryRecommendation(
                slug=slug,
                name=profile["name"],
                flag=profile["flag"],
                match_score=score,
                reason=reason,
                top_programs=profile["programs"][:3]
            ))

    results.sort(key=lambda x: x.match_score, reverse=True)
    top = results[:4]

    if not top:
        # Fallback to general recommend
        top = [CountryRecommendation(
            slug="de",
            name="Германия",
            flag="🇩🇪",
            match_score=50,
            reason="Рекомендовано как универсальное направление с сильной социальной поддержкой.",
            top_programs=["FSJ", "Ausbildung"]
        )]

    avg_score = sum(r.match_score for r in top) / len(top)
    success_chance = min(int(avg_score * 0.9 + edu_score * 2), 95)

    steps = [
        "📄 Собрать базовый пакет документов (загранпаспорт, аттестат/диплом)",
        "💰 Начать формирование финансовой подушки для переезда"
    ]
    if eng_score < 3:
        steps.append("📚 Подтянуть английский язык до уровня B1-B2")
    if ger_score < 2 and any(t.slug in ["de", "at", "ch"] for t in top):
        steps.append("🇩🇪 Начать изучение немецкого языка (цель A2-B1)")
    steps.append("📝 Пройти консультацию с нашим специалистом по выбранной программе")

    best = top[0]
    summary = (
        f"На основе ваших ответов (возраст: {age}, образование: {education}, "
        f"языки: EN-{english_level.upper()}/DE-{german_level.upper()}) "
        f"лучшим направлением для вас является {best.flag} {best.name} с совместимостью {best.match_score}%. "
        f"Общие шансы оцениваются в {success_chance}%."
    )

    return {
        "recommended_countries": top,
        "success_chance": success_chance,
        "next_steps": steps,
        "summary": summary
    }


# ── AI API Endpoints ────────────────────────────────────────────────────────

@router.post("/session", response_model=StartSessionResponse)
async def start_ai_session(
    chat_type: str,  # "chat" or "consultation"
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Starts a new AI session, saves the initial greeting to DB, and returns session details."""
    session_id = str(uuid.uuid4())
    
    if chat_type == "consultation":
        greeting = (
            "Привет! Я твой интерактивный AI-консультант WorldBridge. 🌍\n"
            "Давай подберем идеальную программу для твоего переезда. Ответь на несколько вопросов.\n\n"
            "Для начала, **сколько тебе лет?**"
        )
    else:
        greeting = (
            "Привет! Я персональный AI-ассистент WorldBridge. 🤖\n"
            "Я могу рассказать о визах, программах, стоимости жизни или требованиях к языкам.\n"
            "Задай мне любой вопрос!"
        )

    # Save initial assistant message
    initial_msg = AIChatMessage(
        user_id=current_user.id,
        role="assistant",
        content=greeting,
        chat_type=chat_type,
        session_id=session_id
    )
    db.add(initial_msg)
    await db.flush()

    return StartSessionResponse(session_id=session_id, message=greeting)


@router.get("/history", response_model=ChatHistoryResponse)
async def get_ai_history(
    chat_type: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieves full chat or consultation history for the user."""
    stmt = select(AIChatMessage).where(
        AIChatMessage.user_id == current_user.id,
        AIChatMessage.chat_type == chat_type
    ).order_by(AIChatMessage.created_at.asc())
    
    result = await db.execute(stmt)
    messages = result.scalars().all()
    
    return ChatHistoryResponse(messages=[
        ChatMessageResponse(
            id=m.id,
            role=m.role,
            content=m.content,
            chat_type=m.chat_type,
            session_id=m.session_id,
            created_at=m.created_at
        ) for m in messages
    ])


@router.post("/chat", response_model=ChatMessageResponse)
async def ai_chat_message(
    req: ChatMessageRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Free-form chat interaction with AI, fully persisted in database."""
    # 1. Save user message
    user_msg = AIChatMessage(
        user_id=current_user.id,
        role="user",
        content=req.content,
        chat_type="chat",
        session_id=req.session_id
    )
    db.add(user_msg)
    
    # 2. Analyze user message and generate high-quality helper response
    q = req.content.lower()
    
    if "герман" in q or "deutsch" in q or "de" in q and len(q) < 5:
        reply = (
            "🇩🇪 **Германия** — одно из самых популярных направлений.\n\n"
            "Здесь доступны программы:\n"
            "• **Ausbildung** (дуальное проф. обучение, платят стипендию 800-1400€/мес)\n"
            "• **FSJ/BFD** (социальный год для молодежи, предоставляют жилье и карманные расходы)\n"
            "• **Studium** (высшее образование, обучение часто бесплатное на немецком)\n\n"
            "Для большинства программ требуется немецкий язык от уровня A2 до B2."
        )
    elif "виз" in q or "visa" in q:
        reply = (
            "📄 **Получение визы** — ключевой этап relocation-процесса.\n\n"
            "Основные документы:\n"
            "1. Официальное приглашение от работодателя, вуза или благотворительной организации.\n"
            "2. Финансовые гарантии (блокированный счет, выписка из банка или спонсорское письмо).\n"
            "3. Подтверждение владения языком (сертификаты Goethe-Institut, IELTS, TOEFL).\n"
            "4. Медицинская страховка, покрывающая весь период пребывания."
        )
    elif "денег" in q or "деньги" in q or "бюджет" in q or "расход" in q or "стоимост" in q or "калькулятор" in q:
        reply = (
            "💰 **Планирование финансов**:\n\n"
            "Каждая страна требует определенного бюджета на проживание. Например, в Германии на блокированном счету "
            "необходимо иметь около 992€ в месяц. В Польше или Чехии стоимость жизни ниже (около 500-700€ в месяц).\n\n"
            "💡 Используйте наш встроенный **Калькулятор расходов**, чтобы рассчитать точный баланс доходов и затрат!"
        )
    elif "язык" in q or "английск" in q or "немецк" in q or "ielts" in q or "goethe" in q:
        reply = (
            "🗣️ **Языковые требования**:\n\n"
            "• **Немецкий (German)**: A2 достаточен для Au Pair и некоторых FSJ. B1-B2 требуется для Ausbildung и работы.\n"
            "• **Английский (English)**: Сдача IELTS (5.5 - 7.0) обязательна для обучения в Канаде, США и европейских англоязычных программах.\n\n"
            "Рекомендуем начать подготовку минимум за 6-9 месяцев до планируемого отъезда."
        )
    elif "канад" in q or "canada" in q:
        reply = (
            "🇨🇦 **Канада** предлагает прекрасные условия для иммиграции:\n\n"
            "• **Study Permit**: Обучение в канадских колледжах с правом работы 20 часов в неделю.\n"
            "• **Express Entry**: Балльная система для квалифицированных специалистов.\n"
            "• **Co-op Programs**: Стажировка с интеграцией в канадский рынок труда.\n\n"
            "Необходим хороший уровень английского (IELTS) или французского."
        )
    elif "сша" in q or "usa" in q or "америк" in q:
        reply = (
            "🇺🇸 **США** предоставляет следующие варианты:\n\n"
            "• **Au Pair**: Программа культурного обмена для молодежи с проживанием в американской семье.\n"
            "• **Work & Travel**: Для активных студентов вузов в летний период.\n"
            "• **Internships**: Профессиональные стажировки по визе J-1 для молодых специалистов."
        )
    elif "привет" in q or "hello" in q or "здравствуй" in q:
        reply = (
            "Привет! 🌍 Рад пообщаться. Я могу подробно ответить на твои вопросы о переезде за рубеж. "
            "Спроси меня про **Германию**, **Канаду**, **визовые требования**, **стоимость жизни** или **языки**!"
        )
    else:
        reply = (
            "Я записал твой вопрос! 🤖\n\n"
            "Для успешной иммиграции важно детально изучить программы и требования. "
            "Уточни, пожалуйста, в какую страну ты планируешь переезд (Германия, Канада, США или др.) "
            "или какую программу рассматриваешь (учеба, работа, волонтерство)?"
        )

    # Save assistant message
    assistant_msg = AIChatMessage(
        user_id=current_user.id,
        role="assistant",
        content=reply,
        chat_type="chat",
        session_id=req.session_id
    )
    db.add(assistant_msg)
    await db.flush()

    return ChatMessageResponse(
        id=assistant_msg.id,
        role=assistant_msg.role,
        content=assistant_msg.content,
        chat_type=assistant_msg.chat_type,
        session_id=assistant_msg.session_id,
        created_at=assistant_msg.created_at
    )


@router.post("/consultation", response_model=ChatMessageResponse)
async def ai_consultation_message(
    req: ChatMessageRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Sequential step-by-step interactive consultation. Persists and responds based on current stage."""
    # 1. Save user's answer
    user_msg = AIChatMessage(
        user_id=current_user.id,
        role="user",
        content=req.content,
        chat_type="consultation",
        session_id=req.session_id
    )
    db.add(user_msg)
    await db.flush()

    # 2. Get history to count steps
    stmt = select(AIChatMessage).where(
        AIChatMessage.user_id == current_user.id,
        AIChatMessage.chat_type == "consultation",
        AIChatMessage.session_id == req.session_id
    ).order_by(AIChatMessage.created_at.asc())
    
    result = await db.execute(stmt)
    history = result.scalars().all()

    # Count how many messages the USER sent
    user_replies = [m for m in history if m.role == "user"]
    step_num = len(user_replies)

    reply_content = ""

    if step_num == 1:
        reply_content = (
            "Отлично, возраст зафиксирован! 📝\n\n"
            "**Какое у тебя образование?**\n"
            "*(Напиши: Школа, Колледж, Бакалавриат, Магистратура или PhD)*"
        )
    elif step_num == 2:
        reply_content = (
            "Понял тебя. 🎓\n\n"
            "**Какой у тебя уровень владения языками?**\n"
            "*(Например: Английский B2, Немецкий A2, или напиши 'нет языков')*"
        )
    elif step_num == 3:
        reply_content = (
            "Отлично. Это очень важная деталь. 🗣️\n\n"
            "**Каков твой ориентировочный бюджет на переезд?**\n"
            "*(Напиши: До 1000€, 1000-3000€, или Более 3000€)*"
        )
    elif step_num == 4:
        reply_content = (
            "Принято! Финансы под контролем. 💰\n\n"
            "И последний вопрос:\n"
            "**В какую страну ты мечтаешь переехать?**\n"
            "*(Напиши: Германия, Франция, Бельгия, Швейцария, Австрия, Польша, Чехия, Канада, США или напиши 'Любая')*"
        )
    else:
        # Time to compute recommendations!
        # Let's extract values from history
        age = 22
        education = "bachelor"
        english_level = "b1"
        german_level = "none"
        budget = "medium"
        desired_country = "any"

        # Safe parsing from user messages
        try:
            # Step 1: Age
            age_text = user_replies[0].content
            age_digits = re.findall(r"\d+", age_text)
            if age_digits:
                age = int(age_digits[0])
        except Exception:
            pass

        try:
            # Step 2: Education
            edu_text = user_replies[1].content.lower()
            if "школ" in edu_text:
                education = "school"
            elif "колл" in edu_text or "tech" in edu_text:
                education = "college"
            elif "бак" in edu_text or "bach" in edu_text or "высш" in edu_text:
                education = "bachelor"
            elif "маг" in edu_text or "mast" in edu_text:
                education = "master"
            elif "ph" in edu_text or "докт" in edu_text:
                education = "phd"
        except Exception:
            pass

        try:
            # Step 3: Languages
            lang_text = user_replies[2].content.lower()
            # English extraction
            eng_match = re.search(r"(?:анг|en)[^\w]*(a1|a2|b1|b2|c1|c2)", lang_text)
            if eng_match:
                english_level = eng_match.group(1)
            elif "ielts" in lang_text or "toefl" in lang_text or "анг" in lang_text:
                english_level = "b2"

            # German extraction
            ger_match = re.search(r"(?:нем|de)[^\w]*(a1|a2|b1|b2|c1|c2)", lang_text)
            if ger_match:
                german_level = ger_match.group(1)
            elif "goethe" in lang_text or "нем" in lang_text:
                german_level = "b1"
        except Exception:
            pass

        try:
            # Step 4: Budget
            budget_text = user_replies[3].content.lower()
            if "до 1000" in budget_text or "низк" in budget_text or "low" in budget_text:
                budget = "low"
            elif "более 3000" in budget_text or "высок" in budget_text or "high" in budget_text or "3000" in budget_text and "более" in budget_text:
                budget = "high"
            else:
                budget = "medium"
        except Exception:
            pass

        try:
            # Step 5: Country
            country_text = user_replies[4].content.lower()
            country_map = {
                "герм": "de", "фран": "fr", "бель": "be", "швей": "ch", "авст": "at",
                "поль": "pl", "чех": "cz", "канад": "ca", "сша": "us", "usa": "us"
            }
            for key, code in country_map.items():
                if key in country_text:
                    desired_country = code
                    break
        except Exception:
            pass

        # Calculate reports
        report = generate_recommendations(age, education, english_level, german_level, budget, desired_country)
        
        # Build a beautiful Markdown report message
        rec_countries_str = "\n".join(
            [f"• {c.flag} **{c.name}** (Совместимость: {c.match_score}%) — *{c.reason}*. Популярные программы: {', '.join(c.top_programs)}"
            for c in report["recommended_countries"]]
        )
        
        next_steps_str = "\n".join(report["next_steps"])

        reply_content = (
            "✨ **Твой персональный отчет готов!** ✨\n\n"
            f"🎯 **Шансы на успешный переезд**: {report['success_chance']}%\n\n"
            f"**Рекомендуемые страны:**\n{rec_countries_str}\n\n"
            f"📋 **Рекомендуемые шаги:**\n{next_steps_str}\n\n"
            f"💡 **Резюме**: {report['summary']}\n\n"
            "Вы можете сбросить чат и пройти опрос заново в любое время."
        )

    # Save assistant message
    assistant_msg = AIChatMessage(
        user_id=current_user.id,
        role="assistant",
        content=reply_content,
        chat_type="consultation",
        session_id=req.session_id
    )
    db.add(assistant_msg)
    await db.flush()

    return ChatMessageResponse(
        id=assistant_msg.id,
        role=assistant_msg.role,
        content=assistant_msg.content,
        chat_type=assistant_msg.chat_type,
        session_id=assistant_msg.session_id,
        created_at=assistant_msg.created_at
    )


@router.delete("/reset")
async def reset_ai_chat(
    chat_type: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Deletes dialog history for the current user."""
    stmt = delete(AIChatMessage).where(
        AIChatMessage.user_id == current_user.id,
        AIChatMessage.chat_type == chat_type
    )
    await db.execute(stmt)
    return {"status": "success", "message": f"Dialogue history for '{chat_type}' has been successfully reset."}
