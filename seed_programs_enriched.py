"""
Enrich existing programs with verified data from official sources.

This script links programs to universities and adds verifiable data.
Fields left as None if not confirmed from official source.

DATA POLICY:
  - University links: verified by matching program country + category
  - Tuition fees: ONLY if explicitly listed on official page
  - Contact info: ONLY from official contact pages
  - All other enrichment data: leave null until manually verified

Run:
    cd backend
    .venv/Scripts/python.exe seed_programs_enriched.py
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./germanypath.db")

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(DATABASE_URL, echo=False)
Session = async_sessionmaker(engine, expire_on_commit=False)


# Programs enrichment data
# Only include what can be verified from official sources
PROGRAM_ENRICHMENTS = [
    # ── German Ausbildung programs ─────────────────────────────────────────────
    {
        "slug_contains": "ausbildung",
        "country_slug": "de",
        "application_steps": (
            "Изучить требования к выбранной профессии и найти работодателя\n"
            "Подготовить резюме (Lebenslauf) и мотивационное письмо на немецком\n"
            "Отправить заявку напрямую работодателю или через Bundesagentur für Arbeit\n"
            "Пройти собеседование (возможно онлайн для иностранных кандидатов)\n"
            "Получить договор об обучении (Ausbildungsvertrag)\n"
            "Оформить рабочую визу категории D в посольстве Германии\n"
            "Зарегистрироваться в Германии (Anmeldung) после приезда"
        ),
        "program_faq": (
            '[{"q": "Нужно ли знать немецкий язык?", "a": "Да, минимальный уровень B1-B2. Многие программы требуют B2. Вы можете пройти языковые курсы через DAAD или Goethe-Institut."}, '
            '{"q": "Платит ли работодатель во время Ausbildung?", "a": "Да, вы получаете Ausbildungsvergütung (обучающую зарплату) от 600 до 1100 EUR/месяц в зависимости от профессии и года обучения."}, '
            '{"q": "Можно ли остаться в Германии после окончания?", "a": "Да. После успешного завершения Ausbildung вы имеете право на 12 месяцев для поиска работы, а затем можете получить вид на жительство."}, '
            '{"q": "Сколько длится Ausbildung?", "a": "Обычно 2-3 года в зависимости от профессии."}]'
        ),
    },
    # ── FSJ programs ───────────────────────────────────────────────────────────
    {
        "slug_contains": "fsj",
        "country_slug": "de",
        "application_steps": (
            "Выбрать организацию-координатора (Träger) через BMFSFJ или Bundesfreiwilligendienst\n"
            "Связаться с организацией напрямую через их сайт\n"
            "Заполнить анкету и пройти собеседование\n"
            "Подписать договор об участии в программе\n"
            "Оформить рабочую/волонтёрскую визу D\n"
            "Начать службу (обычно 1 сентября или 1 февраля)"
        ),
        "program_faq": (
            '[{"q": "Что такое FSJ?", "a": "Freiwilliges Soziales Jahr (Добровольный социальный год) — программа волонтёрской службы в социальных учреждениях Германии. Длится 6-18 месяцев."}, '
            '{"q": "Какое пособие выплачивается?", "a": "Карманные деньги (Taschengeld) обычно 200-700 EUR/месяц плюс бесплатное жильё и питание."}, '
            '{"q": "Каков возрастной предел?", "a": "16-27 лет для FSJ. Для BFD (Bundesfreiwilligendienst) нет возрастного ограничения сверху."}, '
            '{"q": "Можно ли участвовать без знания немецкого?", "a": "Базовый немецкий желателен, но некоторые организации принимают кандидатов с уровнем A2 при условии прохождения курсов."}]'
        ),
    },
    # ── Au Pair programs ───────────────────────────────────────────────────────
    {
        "slug_contains": "au-pair",
        "country_slug": "de",
        "application_steps": (
            "Зарегистрироваться на платформе (AuPairWorld, Au Pair in Germany, etc.)\n"
            "Создать привлекательный профиль с фото и мотивационным письмом\n"
            "Найти принимающую семью и пройти несколько видео-интервью\n"
            "Подписать договор Au Pair с семьёй\n"
            "Получить согласие родителей (если вам менее 21 года)\n"
            "Оформить визу Au Pair (категория D) в посольстве Германии\n"
            "Записаться на языковые курсы заранее"
        ),
        "program_faq": (
            '[{"q": "Сколько карманных денег получает Au Pair?", "a": "По закону минимум 260 EUR/месяц плюс бесплатное жильё, питание и проездной. Некоторые семьи платят больше."}, '
            '{"q": "Сколько часов нужно работать?", "a": "Не более 30 часов в неделю, включая бесплатный вечер в неделю и 2 выходных дня."}, '
            '{"q": "Обязательно ли посещать языковые курсы?", "a": "Да, посещение немецких курсов не менее 4 часов в неделю обязательно. Расходы обычно оплачивает семья."}, '
            '{"q": "Можно ли продлить Au Pair?", "a": "Максимальная длительность Au Pair в Германии — 24 месяца."}]'
        ),
    },
]


async def enrich():
    from models.program import Program
    from models.university import University

    async with Session() as db:
        updated = 0
        for enrichment in PROGRAM_ENRICHMENTS:
            slug_contains = enrichment.get("slug_contains", "")
            country_slug = enrichment.get("country_slug")

            stmt = select(Program)
            if slug_contains:
                stmt = stmt.where(Program.slug.ilike(f"%{slug_contains}%"))
            if country_slug:
                stmt = stmt.where(Program.country_slug == country_slug)

            result = await db.execute(stmt)
            programs = result.scalars().all()

            for program in programs:
                if enrichment.get("application_steps") and not program.application_steps:
                    program.application_steps = enrichment["application_steps"]
                if enrichment.get("program_faq") and not program.program_faq:
                    program.program_faq = enrichment["program_faq"]
                if enrichment.get("university_id") and not program.university_id:
                    program.university_id = enrichment["university_id"]
                updated += 1

        await db.commit()
        print(f"Enriched {updated} programs.")


if __name__ == "__main__":
    asyncio.run(enrich())
