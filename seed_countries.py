"""seed_countries.py — Seed all 14 countries into the database."""
import asyncio
from database import AsyncSessionLocal, Base, engine
from models.country import Country
from sqlalchemy import select

COUNTRIES = [
    {"slug": "de", "name_ru": "Германия", "name_en": "Germany", "flag_emoji": "🇩🇪",
     "capital": "Берлин", "population": "84 млн", "languages": "Немецкий", "currency": "EUR €",
     "region": "Europe", "map_x": 52.0, "map_y": 33.0,
     "description_ru": "Германия — крупнейшая экономика Европы с высоким уровнем жизни. Предлагает бесплатное образование в государственных вузах, систему Ausbildung и активный найм иностранных специалистов.",
     "description_en": "Germany is Europe's largest economy with a high standard of living, free public university education, the Ausbildung dual training system, and active recruitment of foreign skilled workers."},
    {"slug": "fr", "name_ru": "Франция", "name_en": "France", "flag_emoji": "🇫🇷",
     "capital": "Париж", "population": "68 млн", "languages": "Французский", "currency": "EUR €",
     "region": "Europe", "map_x": 47.0, "map_y": 40.0,
     "description_ru": "Франция — страна высокой культуры, сильной системы образования и развитой социальной защиты. Программы Au Pair, Erasmus+ и сезонная работа очень популярны среди иностранцев.",
     "description_en": "France offers world-class culture, a strong education system, and robust social protection. Au Pair, Erasmus+, and seasonal work programs are very popular among internationals."},
    {"slug": "be", "name_ru": "Бельгия", "name_en": "Belgium", "flag_emoji": "🇧🇪",
     "capital": "Брюссель", "population": "11.6 млн", "languages": "Французский, Нидерландский, Немецкий", "currency": "EUR €",
     "region": "Europe", "map_x": 49.0, "map_y": 35.0,
     "description_ru": "Бельгия — центр Европейского союза с высокими зарплатами. Минимальная зарплата ~1800€/мес. Востребованы IT, инженерия и медицина. Три официальных языка.",
     "description_en": "Belgium is the heart of the EU with high salaries (~€1800/mo minimum). IT, engineering and healthcare are in demand. Three official languages open diverse opportunities."},
    {"slug": "ch", "name_ru": "Швейцария", "name_en": "Switzerland", "flag_emoji": "🇨🇭",
     "capital": "Берн", "population": "8.7 млн", "languages": "Немецкий, Французский, Итальянский", "currency": "CHF ₣",
     "region": "Europe", "map_x": 50.0, "map_y": 42.0,
     "description_ru": "Швейцария — одна из богатейших стран мира. Средняя зарплата 6000-8000 CHF/мес. Развитая гостиничная и финансовая отрасли. Стоимость жизни высокая.",
     "description_en": "Switzerland is one of the world's wealthiest nations. Average salary CHF 6000-8000/mo. Leading hospitality and finance sectors. High cost of living."},
    {"slug": "at", "name_ru": "Австрия", "name_en": "Austria", "flag_emoji": "🇦🇹",
     "capital": "Вена", "population": "9.1 млн", "languages": "Немецкий", "currency": "EUR €",
     "region": "Europe", "map_x": 54.0, "map_y": 39.0,
     "description_ru": "Австрия — немецкоязычная страна с высоким уровнем жизни. Похожа на Германию, но менее конкурентна. Ausbildung, Au Pair и сезонная работа в туризме — главные направления.",
     "description_en": "Austria is a German-speaking country with a high quality of life, similar to Germany but less competitive. Ausbildung, Au Pair, and tourism seasonal work are the main pathways."},
    {"slug": "pl", "name_ru": "Польша", "name_en": "Poland", "flag_emoji": "🇵🇱",
     "capital": "Варшава", "population": "38 млн", "languages": "Польский", "currency": "PLN zł",
     "region": "Europe", "map_x": 57.0, "map_y": 32.0,
     "description_ru": "Польша — самый простой путь в Евросоюз. Рабочая виза оформляется быстро. Минимальная зарплата ~730€/мес. Популярны заводы, склады и строительство.",
     "description_en": "Poland is the easiest gateway to the EU. Work visas process quickly. Minimum wage ~€730/mo. Factories, warehouses, and construction are most popular."},
    {"slug": "cz", "name_ru": "Чехия", "name_en": "Czech Republic", "flag_emoji": "🇨🇿",
     "capital": "Прага", "population": "10.9 млн", "languages": "Чешский", "currency": "CZK Kč",
     "region": "Europe", "map_x": 54.0, "map_y": 35.0,
     "description_ru": "Чехия предлагает бесплатное образование для тех, кто обучается на чешском языке. Низкая стоимость жизни, высокий спрос на иностранных рабочих.",
     "description_en": "Czech Republic offers free education for Czech-language programs. Low cost of living and high demand for foreign workers make it an accessible destination."},
    {"slug": "se", "name_ru": "Швеция", "name_en": "Sweden", "flag_emoji": "🇸🇪",
     "capital": "Стокгольм", "population": "10.5 млн", "languages": "Шведский", "currency": "SEK kr",
     "region": "Europe", "map_x": 53.0, "map_y": 22.0,
     "description_ru": "Швеция — скандинавская страна с высоким уровнем жизни. IT-сектор и исследования активно набирают иностранцев. Обучение в магистратуре на английском языке.",
     "description_en": "Sweden is a Scandinavian country with a high living standard. The IT and research sectors actively recruit internationals. Master's programs taught in English."},
    {"slug": "no", "name_ru": "Норвегия", "name_en": "Norway", "flag_emoji": "🇳🇴",
     "capital": "Осло", "population": "5.4 млн", "languages": "Норвежский", "currency": "NOK kr",
     "region": "Europe", "map_x": 49.0, "map_y": 20.0,
     "description_ru": "Норвегия — одна из богатейших стран мира. Рыбная промышленность и сезонная работа дают доход 2500-4000€/мес. Высокий уровень жизни.",
     "description_en": "Norway is one of the world's wealthiest nations. Fish industry and seasonal work pay €2500-4000/mo. Very high standard of living."},
    {"slug": "fi", "name_ru": "Финляндия", "name_en": "Finland", "flag_emoji": "🇫🇮",
     "capital": "Хельсинки", "population": "5.5 млн", "languages": "Финский, Шведский", "currency": "EUR €",
     "region": "Europe", "map_x": 58.0, "map_y": 19.0,
     "description_ru": "Финляндия предлагает сезонный сбор ягод (3-5€/кг), Au Pair и IT-вакансии. Государство активно приглашает иностранных специалистов.",
     "description_en": "Finland offers seasonal berry picking (€3-5/kg), Au Pair, and IT vacancies. The government actively invites foreign specialists."},
    {"slug": "tr", "name_ru": "Турция", "name_en": "Turkey", "flag_emoji": "🇹🇷",
     "capital": "Анкара", "population": "85 млн", "languages": "Турецкий", "currency": "TRY ₺",
     "region": "Asia", "map_x": 62.0, "map_y": 44.0,
     "description_ru": "Турция предлагает государственные стипендии Türkiye Bursları, покрывающие всё обучение + проживание + стипендию. Низкая стоимость жизни. Развитые туризм и образование.",
     "description_en": "Turkey offers the Türkiye Bursları government scholarship covering full tuition + accommodation + stipend. Low cost of living, strong tourism and education sectors."},
    {"slug": "cn", "name_ru": "Китай", "name_en": "China", "flag_emoji": "🇨🇳",
     "capital": "Пекин", "population": "1.4 млрд", "languages": "Китайский (мандарин)", "currency": "CNY ¥",
     "region": "Asia", "map_x": 78.0, "map_y": 45.0,
     "description_ru": "Китай — вторая экономика мира. CSC Scholarship полностью покрывает обучение. Спрос на учителей английского языка очень высокий. Уникальный культурный опыт.",
     "description_en": "China is the world's second-largest economy. The CSC Scholarship covers full tuition. Demand for English teachers is very high. Unique cultural experience."},
    {"slug": "ca", "name_ru": "Канада", "name_en": "Canada", "flag_emoji": "🇨🇦",
     "capital": "Оттава", "population": "38 млн", "languages": "Английский, Французский", "currency": "CAD $",
     "region": "North America", "map_x": 22.0, "map_y": 28.0,
     "description_ru": "Канада — одна из лучших стран для иммиграции. Express Entry позволяет получить ПМЖ за 6-12 месяцев. Высокий спрос на квалифицированных специалистов.",
     "description_en": "Canada is one of the best immigration destinations. Express Entry allows permanent residency in 6-12 months. High demand for skilled professionals."},
    {"slug": "us", "name_ru": "США", "name_en": "USA", "flag_emoji": "🇺🇸",
     "capital": "Вашингтон", "population": "335 млн", "languages": "Английский", "currency": "USD $",
     "region": "North America", "map_x": 22.0, "map_y": 42.0,
     "description_ru": "США — крупнейшая экономика мира. Work & Travel, Au Pair и Camp America популярны для молодёжи. Green Card Lottery — шанс для всех. Самые высокие зарплаты.",
     "description_en": "The USA is the world's largest economy. Work & Travel, Au Pair, and Camp America are popular for youth. Green Card Lottery is open to everyone. Highest salaries globally."},
]

async def seed_countries():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as db:
        for data in COUNTRIES:
            exists = (await db.execute(select(Country).where(Country.slug == data["slug"]))).scalar_one_or_none()
            if not exists:
                db.add(Country(**data))
                print(f"[+] Created: {data['name_en']}")
            else:
                # Always update all fields so re-running fixes stale data (e.g. wrong flag_emoji)
                for key, value in data.items():
                    setattr(exists, key, value)
                print(f"[~] Updated: {data['name_en']}")
        await db.commit()
    print("[OK] Countries seeded!")

if __name__ == "__main__":
    asyncio.run(seed_countries())
