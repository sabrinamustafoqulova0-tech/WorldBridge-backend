#!/bin/bash
python -c "
import asyncio
from database import engine, Base
import models

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

asyncio.run(create_tables())
"
python seed_all.py
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4