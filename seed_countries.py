"""seed_countries.py — Seed all 14 countries into the database."""
import asyncio
from database import AsyncSessionLocal, Base, engine
from models.country import Country
from sqlalchemy import select
COUNTRIES = [
    {"slug": "de", "name_ru": "Германия", "name_en": "Germany", "flag_emoji": "🇩🇪",
     "capital": "Берлин", "population": "84 млн", "languages": "Немецкий", "currency": "EUR €",
     "region": "Europe", "map_x": 52.0, "map_y": 33.0,
     "image_url": "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=800",
     "description_ru": "Германия — крупнейшая экономика Европы с высоким уровнем жизни.",
     "description_en": "Germany is Europe's largest economy with a high standard of living."},
    {"slug": "fr", "name_ru": "Франция", "name_en": "France", "flag_emoji": "🇫🇷",
     "capital": "Париж", "population": "68 млн", "languages": "Французский", "currency": "EUR €",
     "region": "Europe", "map_x": 47.0, "map_y": 40.0,
     "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800",
     "description_ru": "Франция — страна высокой культуры и сильной системы образования.",
     "description_en": "France offers world-class culture and a strong education system."},
    {"slug": "be", "name_ru": "Бельгия", "name_en": "Belgium", "flag_emoji": "🇧🇪",
     "capital": "Брюссель", "population": "11.6 млн", "languages": "Французский, Нидерландский, Немецкий", "currency": "EUR €",
     "region": "Europe", "map_x": 49.0, "map_y": 35.0,
     "image_url": "https://images.unsplash.com/photo-1559113513-d5406b089b8b?w=800",
     "description_ru": "Бельгия — центр Европейского союза с высокими зарплатами.",
     "description_en": "Belgium is the heart of the EU with high salaries."},
    {"slug": "ch", "name_ru": "Швейцария", "name_en": "Switzerland", "flag_emoji": "🇨🇭",
     "capital": "Берн", "population": "8.7 млн", "languages": "Немецкий, Французский, Итальянский", "currency": "CHF ₣",
     "region": "Europe", "map_x": 50.0, "map_y": 42.0,
     "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
     "description_ru": "Швейцария — одна из богатейших стран мира.",
     "description_en": "Switzerland is one of the world's wealthiest nations."},
    {"slug": "at", "name_ru": "Австрия", "name_en": "Austria", "flag_emoji": "🇦🇹",
     "capital": "Вена", "population": "9.1 млн", "languages": "Немецкий", "currency": "EUR €",
     "region": "Europe", "map_x": 54.0, "map_y": 39.0,
     "image_url": "https://images.unsplash.com/photo-1516550893923-42d28e5677af?w=800",
     "description_ru": "Австрия — немецкоязычная страна с высоким уровнем жизни.",
     "description_en": "Austria is a German-speaking country with a high quality of life."},
    {"slug": "pl", "name_ru": "Польша", "name_en": "Poland", "flag_emoji": "🇵🇱",
     "capital": "Варшава", "population": "38 млн", "languages": "Польский", "currency": "PLN zł",
     "region": "Europe", "map_x": 57.0, "map_y": 32.0,
     "image_url": "https://images.unsplash.com/photo-1519197924294-4ba991a11128?w=800",
     "description_ru": "Польша — самый простой путь в Евросоюз.",
     "description_en": "Poland is the easiest gateway to the EU."},
    {"slug": "cz", "name_ru": "Чехия", "name_en": "Czech Republic", "flag_emoji": "🇨🇿",
     "capital": "Прага", "population": "10.9 млн", "languages": "Чешский", "currency": "CZK Kč",
     "region": "Europe", "map_x": 54.0, "map_y": 35.0,
     "image_url": "https://images.unsplash.com/photo-1541849546-216549ae216d?w=800",
     "description_ru": "Чехия предлагает бесплатное образование на чешском языке.",
     "description_en": "Czech Republic offers free education for Czech-language programs."},
    {"slug": "se", "name_ru": "Швеция", "name_en": "Sweden", "flag_emoji": "🇸🇪",
     "capital": "Стокгольм", "population": "10.5 млн", "languages": "Шведский", "currency": "SEK kr",
     "region": "Europe", "map_x": 53.0, "map_y": 22.0,
     "image_url": "https://images.unsplash.com/photo-1509356843151-3e7d96241e11?w=800",
     "description_ru": "Швеция — скандинавская страна с высоким уровнем жизни.",
     "description_en": "Sweden is a Scandinavian country with a high living standard."},
    {"slug": "no", "name_ru": "Норвегия", "name_en": "Norway", "flag_emoji": "🇳🇴",
     "capital": "Осло", "population": "5.4 млн", "languages": "Норвежский", "currency": "NOK kr",
     "region": "Europe", "map_x": 49.0, "map_y": 20.0,
     "image_url": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=800",
     "description_ru": "Норвегия — одна из богатейших стран мира.",
     "description_en": "Norway is one of the world's wealthiest nations."},
    {"slug": "fi", "name_ru": "Финляндия", "name_en": "Finland", "flag_emoji": "🇫🇮",
     "capital": "Хельсинки", "population": "5.5 млн", "languages": "Финский, Шведский", "currency": "EUR €",
     "region": "Europe", "map_x": 58.0, "map_y": 19.0,
     "image_url": "https://images.unsplash.com/photo-1538332576228-eb5b4c4de6f5?w=800",
     "description_ru": "Финляндия предлагает сезонный сбор ягод, Au Pair и IT-вакансии.",
     "description_en": "Finland offers seasonal berry picking, Au Pair, and IT vacancies."},
    {"slug": "tr", "name_ru": "Турция", "name_en": "Turkey", "flag_emoji": "🇹🇷",
     "capital": "Анкара", "population": "85 млн", "languages": "Турецкий", "currency": "TRY ₺",
     "region": "Asia", "map_x": 62.0, "map_y": 44.0,
     "image_url": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=800",
     "description_ru": "Турция предлагает государственные стипендии Türkiye Bursları.",
     "description_en": "Turkey offers the Türkiye Bursları government scholarship."},
    {"slug": "cn", "name_ru": "Китай", "name_en": "China", "flag_emoji": "🇨🇳",
     "capital": "Пекин", "population": "1.4 млрд", "languages": "Китайский (мандарин)", "currency": "CNY ¥",
     "region": "Asia", "map_x": 78.0, "map_y": 45.0,
     "image_url": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800",
     "description_ru": "Китай — вторая экономика мира с CSC Scholarship.",
     "description_en": "China is the world's second-largest economy with the CSC Scholarship."},
    {"slug": "ca", "name_ru": "Канада", "name_en": "Canada", "flag_emoji": "🇨🇦",
     "capital": "Оттава", "population": "38 млн", "languages": "Английский, Французский", "currency": "CAD $",
     "region": "North America", "map_x": 22.0, "map_y": 28.0,
     "image_url": "https://images.unsplash.com/photo-1517935706615-2717063c2225?w=800",
     "description_ru": "Канада — одна из лучших стран для иммиграции.",
     "description_en": "Canada is one of the best immigration destinations."},
    {"slug": "us", "name_ru": "США", "name_en": "USA", "flag_emoji": "🇺🇸",
     "capital": "Вашингтон", "population": "335 млн", "languages": "Английский", "currency": "USD $",
     "region": "North America", "map_x": 22.0, "map_y": 42.0,
     "image_url": "https://images.unsplash.com/photo-1485738422979-f5c462d49f74?w=800",
     "description_ru": "США — крупнейшая экономика мира.",
     "description_en": "The USA is the world's largest economy."},
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
