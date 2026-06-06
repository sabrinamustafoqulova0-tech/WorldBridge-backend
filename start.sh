#!/bin/bash
python -c "
import asyncio
from database import engine, Base
import models

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Add new columns if they don't exist
        new_columns = [
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS university_id INTEGER',
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS university_name VARCHAR',
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS city VARCHAR',
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS tuition_fee FLOAT',
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS tuition_currency VARCHAR',
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS accommodation_cost FLOAT',
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS language_course_cost FLOAT',
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS scholarship_available BOOLEAN',
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS scholarship_amount FLOAT',
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS contact_email VARCHAR',
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS contact_phone VARCHAR',
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS university_address VARCHAR',
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS program_page_url VARCHAR',
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS application_steps JSON',
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS program_faq JSON',
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS data_source VARCHAR',
            'ALTER TABLE programs ADD COLUMN IF NOT EXISTS last_synced_at TIMESTAMP',
        ]
        from sqlalchemy import text
        for sql in new_columns:
            try:
                await conn.execute(text(sql))
            except Exception:
                pass
    await engine.dispose()

asyncio.run(create_tables())
"
python seed_all.py
python seed_universities.py
python seed_programs_enriched.py
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4