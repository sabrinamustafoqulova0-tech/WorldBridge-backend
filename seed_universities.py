"""
Seed script for universities with real Unsplash photos.
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./germanypath.db")
engine = create_async_engine(DATABASE_URL, echo=False)
Session = async_sessionmaker(engine, expire_on_commit=False)


UNIVERSITIES = [
    # ── Germany ────────────────────────────────────────────────────────────────
    {
        "slug": "tu-muenchen",
        "name_ru": "Технический университет Мюнхена",
        "name_en": "Technical University of Munich",
        "name_tg": "Донишгоҳи техникии Мюнхен",
        "country_slug": "de",
        "city": "München",
        "website_url": "https://www.tum.de",
        "lat": 48.1497,
        "lon": 11.5681,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "description_ru": "Один из ведущих технических университетов Германии, основан в 1868 году.",
        "description_en": "One of Germany's top technical universities, founded in 1868.",
    },
    {
        "slug": "lmu-muenchen",
        "name_ru": "Мюнхенский университет Людвига-Максимилиана",
        "name_en": "Ludwig Maximilian University of Munich",
        "name_tg": "Донишгоҳи Мюнхен ба номи Людвиг-Максимилиан",
        "country_slug": "de",
        "city": "München",
        "website_url": "https://www.lmu.de",
        "lat": 48.1506,
        "lon": 11.5802,
        "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
        "description_ru": "Один из старейших и крупнейших университетов Германии, основан в 1472 году.",
        "description_en": "One of Germany's oldest and largest universities, founded in 1472.",
    },
    {
        "slug": "uni-heidelberg",
        "name_ru": "Гейдельбергский университет",
        "name_en": "Heidelberg University",
        "name_tg": "Донишгоҳи Гейделберг",
        "country_slug": "de",
        "city": "Heidelberg",
        "website_url": "https://www.uni-heidelberg.de",
        "lat": 49.4099,
        "lon": 8.7075,
        "image_url": "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "description_ru": "Старейший университет Германии, основан в 1386 году.",
        "description_en": "Germany's oldest university, founded in 1386.",
    },
    {
        "slug": "fu-berlin",
        "name_ru": "Свободный университет Берлина",
        "name_en": "Freie Universität Berlin",
        "name_tg": "Донишгоҳи озоди Берлин",
        "country_slug": "de",
        "city": "Berlin",
        "website_url": "https://www.fu-berlin.de",
        "lat": 52.4558,
        "lon": 13.2944,
        "image_url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "description_ru": "Один из ведущих университетов Берлина, основан в 1948 году.",
        "description_en": "One of Berlin's leading universities, founded in 1948.",
    },
    {
        "slug": "hu-berlin",
        "name_ru": "Берлинский университет Гумбольдта",
        "name_en": "Humboldt-Universität zu Berlin",
        "name_tg": "Донишгоҳи Гумболдти Берлин",
        "country_slug": "de",
        "city": "Berlin",
        "website_url": "https://www.hu-berlin.de",
        "lat": 52.5195,
        "lon": 13.3932,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
        "description_ru": "Один из старейших университетов Берлина, основан в 1810 году.",
        "description_en": "One of Berlin's oldest universities, founded in 1810.",
    },
    {
        "slug": "rwth-aachen",
        "name_ru": "Рейнско-Вестфальский технический университет Ахена",
        "name_en": "RWTH Aachen University",
        "name_tg": "Донишгоҳи техникии Ахен",
        "country_slug": "de",
        "city": "Aachen",
        "website_url": "https://www.rwth-aachen.de",
        "lat": 50.7774,
        "lon": 6.0769,
        "image_url": "https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "description_ru": "Один из крупнейших технических университетов Германии.",
        "description_en": "One of Germany's largest technical universities.",
    },
    {
        "slug": "uni-koeln",
        "name_ru": "Кёльнский университет",
        "name_en": "University of Cologne",
        "name_tg": "Донишгоҳи Кёлн",
        "country_slug": "de",
        "city": "Köln",
        "website_url": "https://www.uni-koeln.de",
        "lat": 50.9283,
        "lon": 6.9300,
        "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "description_ru": "Один из крупнейших университетов Германии, основан в 1388 году.",
        "description_en": "One of Germany's largest universities, founded in 1388.",
    },
    {
        "slug": "uni-hamburg",
        "name_ru": "Гамбургский университет",
        "name_en": "University of Hamburg",
        "name_tg": "Донишгоҳи Гамбург",
        "country_slug": "de",
        "city": "Hamburg",
        "website_url": "https://www.uni-hamburg.de",
        "lat": 53.5677,
        "lon": 9.9739,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
        "description_ru": "Крупнейший университет северной Германии, основан в 1919 году.",
        "description_en": "Northern Germany's largest university, founded in 1919.",
    },

    # ── France ─────────────────────────────────────────────────────────────────
    {
        "slug": "sorbonne-universite",
        "name_ru": "Университет Сорбонна",
        "name_en": "Sorbonne University",
        "name_tg": "Донишгоҳи Сорбонна",
        "country_slug": "fr",
        "city": "Paris",
        "website_url": "https://www.sorbonne-universite.fr",
        "lat": 48.8462,
        "lon": 2.3444,
        "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "description_ru": "Один из старейших и наиболее престижных университетов Франции, основан в 1253 году.",
        "description_en": "One of France's oldest and most prestigious universities, founded in 1253.",
    },
    {
        "slug": "sciences-po",
        "name_ru": "Институт политических наук Парижа (Sciences Po)",
        "name_en": "Sciences Po Paris",
        "name_tg": "Институти илмҳои сиёсии Париж",
        "country_slug": "fr",
        "city": "Paris",
        "website_url": "https://www.sciencespo.fr",
        "lat": 48.8553,
        "lon": 2.3286,
        "image_url": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "description_ru": "Ведущий французский университет в области политики и международных отношений.",
        "description_en": "France's leading university for political science and international relations.",
    },
    {
        "slug": "universite-paris-saclay",
        "name_ru": "Университет Пари-Сакле",
        "name_en": "Université Paris-Saclay",
        "name_tg": "Донишгоҳи Париж-Сакле",
        "country_slug": "fr",
        "city": "Gif-sur-Yvette",
        "website_url": "https://www.universite-paris-saclay.fr",
        "lat": 48.7096,
        "lon": 2.1629,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800",
        "description_ru": "Один из ведущих исследовательских университетов Франции.",
        "description_en": "One of France's leading research universities.",
    },

    # ── Sweden ─────────────────────────────────────────────────────────────────
    {
        "slug": "kth-stockholm",
        "name_ru": "Королевский технологический институт (KTH)",
        "name_en": "KTH Royal Institute of Technology",
        "name_tg": "Институти технологии шоҳии КТН",
        "country_slug": "se",
        "city": "Stockholm",
        "website_url": "https://www.kth.se",
        "lat": 59.3498,
        "lon": 18.0703,
        "image_url": "https://images.unsplash.com/photo-1509356843151-3e7d96241e11?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "description_ru": "Ведущий технологический университет Швеции, основан в 1827 году.",
        "description_en": "Sweden's leading technology university, founded in 1827.",
    },
    {
        "slug": "Uppsala-university",
        "name_ru": "Уппсальский университет",
        "name_en": "Uppsala University",
        "name_tg": "Донишгоҳи Упсала",
        "country_slug": "se",
        "city": "Uppsala",
        "website_url": "https://www.uu.se",
        "lat": 59.8555,
        "lon": 17.6319,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1509356843151-3e7d96241e11?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
        "description_ru": "Старейший университет Скандинавии, основан в 1477 году.",
        "description_en": "Scandinavia's oldest university, founded in 1477.",
    },

    # ── Switzerland ────────────────────────────────────────────────────────────
    {
        "slug": "eth-zurich",
        "name_ru": "Федеральная высшая техническая школа Цюриха (ETH Zurich)",
        "name_en": "ETH Zurich",
        "name_tg": "Мактаби олии техникии федералии Сюрих",
        "country_slug": "ch",
        "city": "Zürich",
        "website_url": "https://ethz.ch",
        "lat": 47.3769,
        "lon": 8.5481,
        "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "description_ru": "Один из лучших технических университетов мира, основан в 1855 году.",
        "description_en": "One of the world's top technical universities, founded in 1855.",
    },

    # ── Poland ─────────────────────────────────────────────────────────────────
    {
        "slug": "university-of-warsaw",
        "name_ru": "Варшавский университет",
        "name_en": "University of Warsaw",
        "name_tg": "Донишгоҳи Варшава",
        "country_slug": "pl",
        "city": "Warsaw",
        "website_url": "https://www.uw.edu.pl",
        "lat": 52.2394,
        "lon": 21.0176,
        "image_url": "https://images.unsplash.com/photo-1519197924294-4ba991a11128?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "description_ru": "Крупнейший и один из лучших университетов Польши, основан в 1816 году.",
        "description_en": "Poland's largest and one of its best universities, founded in 1816.",
    },
    {
        "slug": "agh-university",
        "name_ru": "Краковский горно-металлургический университет (AGH)",
        "name_en": "AGH University of Science and Technology",
        "name_tg": "Донишгоҳи илм ва технологияи AGH",
        "country_slug": "pl",
        "city": "Kraków",
        "website_url": "https://www.agh.edu.pl",
        "lat": 50.0674,
        "lon": 19.9138,
        "image_url": "https://images.unsplash.com/photo-1541849546-216549ae216d?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "description_ru": "Один из ведущих технических университетов Польши, основан в 1919 году.",
        "description_en": "One of Poland's leading technical universities, founded in 1919.",
    },

    # ── Czech Republic ─────────────────────────────────────────────────────────
    {
        "slug": "charles-university",
        "name_ru": "Карлов университет",
        "name_en": "Charles University",
        "name_tg": "Донишгоҳи Карл",
        "country_slug": "cz",
        "city": "Prague",
        "website_url": "https://cuni.cz",
        "lat": 50.0879,
        "lon": 14.4198,
        "image_url": "https://images.unsplash.com/photo-1541849546-216549ae216d?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
        "description_ru": "Старейший университет Центральной Европы, основан в 1348 году.",
        "description_en": "Central Europe's oldest university, founded in 1348.",
    },

    # ── Canada ─────────────────────────────────────────────────────────────────
    {
        "slug": "university-of-toronto",
        "name_ru": "Университет Торонто",
        "name_en": "University of Toronto",
        "name_tg": "Донишгоҳи Торонто",
        "country_slug": "ca",
        "city": "Toronto",
        "website_url": "https://www.utoronto.ca",
        "lat": 43.6629,
        "lon": -79.3957,
        "image_url": "https://images.unsplash.com/photo-1517935706615-2717063c2225?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "description_ru": "Один из лучших университетов Канады и мира, основан в 1827 году.",
        "description_en": "One of Canada's and the world's top universities, founded in 1827.",
    },
    {
        "slug": "mcgill-university",
        "name_ru": "Университет Макгилла",
        "name_en": "McGill University",
        "name_tg": "Донишгоҳи МакГилл",
        "country_slug": "ca",
        "city": "Montréal",
        "website_url": "https://www.mcgill.ca",
        "lat": 45.5048,
        "lon": -73.5772,
        "image_url": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1517935706615-2717063c2225?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "description_ru": "Ведущий исследовательский университет Канады, основан в 1821 году.",
        "description_en": "Canada's leading research university, founded in 1821.",
    },

    # ── Austria ────────────────────────────────────────────────────────────────
    {
        "slug": "uni-wien",
        "name_ru": "Венский университет",
        "name_en": "University of Vienna",
        "name_tg": "Донишгоҳи Вена",
        "country_slug": "at",
        "city": "Wien",
        "website_url": "https://www.univie.ac.at",
        "lat": 48.2132,
        "lon": 16.3567,
        "image_url": "https://images.unsplash.com/photo-1516550893923-42d28e5677af?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "description_ru": "Старейший университет немецкоязычного мира, основан в 1365 году.",
        "description_en": "The oldest university in the German-speaking world, founded in 1365.",
    },

    # ── Belgium ────────────────────────────────────────────────────────────────
    {
        "slug": "ku-leuven",
        "name_ru": "Католический университет Лёвена",
        "name_en": "KU Leuven",
        "name_tg": "Донишгоҳи католикии Лёвен",
        "country_slug": "be",
        "city": "Leuven",
        "website_url": "https://www.kuleuven.be",
        "lat": 50.8780,
        "lon": 4.7005,
        "image_url": "https://images.unsplash.com/photo-1559113513-d5406b089b8b?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "description_ru": "Один из старейших католических университетов мира, основан в 1425 году.",
        "description_en": "One of the world's oldest Catholic universities, founded in 1425.",
    },

    # ── Norway ─────────────────────────────────────────────────────────────────
    {
        "slug": "university-of-oslo",
        "name_ru": "Университет Осло",
        "name_en": "University of Oslo",
        "name_tg": "Донишгоҳи Осло",
        "country_slug": "no",
        "city": "Oslo",
        "website_url": "https://www.uio.no",
        "lat": 59.9396,
        "lon": 10.7215,
        "image_url": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "description_ru": "Старейший и крупнейший университет Норвегии, основан в 1811 году.",
        "description_en": "Norway's oldest and largest university, founded in 1811.",
    },

    # ── Finland ────────────────────────────────────────────────────────────────
    {
        "slug": "university-of-helsinki",
        "name_ru": "Хельсинкский университет",
        "name_en": "University of Helsinki",
        "name_tg": "Донишгоҳи Хелсинки",
        "country_slug": "fi",
        "city": "Helsinki",
        "website_url": "https://www.helsinki.fi",
        "lat": 60.1699,
        "lon": 24.9384,
        "image_url": "https://images.unsplash.com/photo-1538332576228-eb5b4c4de6f5?w=800",
        "image_url_2": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "image_url_3": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
        "description_ru": "Ведущий университет Финляндии, основан в 1640 году.",
        "description_en": "Finland's leading university, founded in 1640.",
    },
]


async def seed():
    from models.university import University

    async with engine.begin() as conn:
        from database import Base
        await conn.run_sync(Base.metadata.create_all)

    async with Session() as db:
        created = 0
        updated = 0
        for data in UNIVERSITIES:
            existing = (
                await db.execute(
                    select(University).where(University.slug == data["slug"])
                )
            ).scalar_one_or_none()

            if existing:
                for k, v in data.items():
                    setattr(existing, k, v)
                updated += 1
                print(f"[~] Updated: {data['name_en']}")
            else:
                db.add(University(**data))
                created += 1
                print(f"[+] Created: {data['name_en']}")

        await db.commit()
        print(f"\nUniversities: {created} created, {updated} updated.")


if __name__ == "__main__":
    asyncio.run(seed())