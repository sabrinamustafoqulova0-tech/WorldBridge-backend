"""seed_programs_3.py — Turkey, China, Canada, USA programs."""
import asyncio
from database import AsyncSessionLocal, Base, engine
from models.program import Program, ProgramCategory, ProgramLevel
from sqlalchemy import select

PROGRAMS = [
    # ── TURKEY ──
    {"slug": "tr-turkiye-burslari", "country_slug": "tr", "title": "Türkiye Bursları — Государственная стипендия",
     "category": ProgramCategory.STUDIUM, "level": ProgramLevel.BEGINNER,
     "short_description": "Полная государственная стипендия Турции: обучение + жильё + 700-1000₺/мес + авиабилет.",
     "description": "Türkiye Bursları — самая щедрая государственная стипендия Турции для иностранцев. Покрывает всё.",
     "full_description": "Türkiye Bursları (YTB) — ежегодный конкурс для иностранцев. Включает: полное покрытие обучения, место в общежитии, ежемесячную стипендию (700₺ бакалавр / 950₺ магистр / 1400₺ PhD), медицинскую страховку, годовые курсы турецкого языка перед поступлением, авиабилет туда-обратно. Более 700 программ на турецком и английском языках. Срок: бакалавр до 21 года, магистр до 30 лет, PhD до 35 лет.",
     "min_age": 17, "max_age": 35, "duration_months": 48,
     "language_requirement": "B2 (турецкий после курсов) или IELTS 5.5+ (для англ. программ)",
     "salary_range": "Стипендия 700–1400 ₺/мес + жильё бесплатно",
     "cost": "Полностью бесплатно (включая авиабилет)",
     "documents": "Загранпаспорт, аттестат/диплом (апостиль), IELTS (для англ. программ), мотивационное письмо, 2 рекомендательных письма, медсправка",
     "deadline": "Заявки: февраль-март. Результаты: июнь-июль. Старт: октябрь",
     "official_url": "https://www.turkiyeburslari.gov.tr",
     "residence_permit": True,
     "pros": "Полностью бесплатно\nАвиабилет включён\nГод изучения турецкого\nМедицинская страховка\nПрестижная стипендия",
     "cons": "Очень высокий конкурс\nТурецкий обязателен после курсов\nСтипендия небольшая по меркам Европы\nОграничение по возрасту",
     "career_opportunities": "Диплом турецкого университета + знание турецкого языка открывают карьеру в турецко-язычных регионах и международных компаниях.",
     "is_published": True},

    {"slug": "tr-internship", "country_slug": "tr", "title": "Стажировка в Турции",
     "category": ProgramCategory.INTERNSHIP, "level": ProgramLevel.BEGINNER,
     "short_description": "Стажировки в отелях Анталии, Стамбула, Измира. Опыт в туризме и IT.",
     "description": "Турция предлагает стажировки в гостиничном бизнесе (Анталия) и IT (Стамбул) для молодёжи.",
     "full_description": "Стажировки в Турции популярны в гостиничном секторе (Antalya, Alanya, Bodrum), IT (Istanbul Tech Valley), туризме и ресторанном бизнесе. Официальные стажировки оформляются через компанию (рабочее разрешение). Оплата: 0-500$/мес (часто с жильём). Неофициальные стажировки по туристической визе — для краткосрочного опыта. Сезон: апрель-октябрь для туризма.",
     "min_age": 18, "max_age": 30, "duration_months": 6,
     "language_requirement": "B1 английский (турецкий приветствуется)",
     "salary_range": "0–500 $/мес (часто жильё и питание включены)",
     "cost": "Виза e-Visa ~50$, авиабилет ~200-400€",
     "documents": "Загранпаспорт, резюме, мотивационное письмо, диплом/справка с учёбы",
     "deadline": "Круглый год. Гостиничные стажировки — с марта по ноябрь",
     "official_url": "https://www.kariyer.net",
     "residence_permit": False,
     "pros": "Низкая стоимость жизни\nТёплый климат\nМного вакансий в туризме\nЛёгкая виза",
     "cons": "Маленькая зарплата\nЭкономическая нестабильность (инфляция)\nТурецкий язык полезен но сложен",
     "career_opportunities": "Стажировка в крупном турецком отеле или IT компании — хорошая строчка в резюме для международной карьеры в туризме.",
     "is_published": True},

    # ── CHINA ──
    {"slug": "cn-csc-scholarship", "country_slug": "cn", "title": "CSC Scholarship — Стипендия Китая",
     "category": ProgramCategory.STUDIUM, "level": ProgramLevel.INTERMEDIATE,
     "short_description": "Государственная стипендия Китая (CSC): покрывает обучение, жильё и 2500-3500 CNY/мес.",
     "description": "Chinese Government Scholarship (CSC) — полная стипендия от Министерства образования Китая.",
     "full_description": "Chinese Government Scholarship (CGS) выдаётся Министерством образования Китая. Покрывает: обучение, общежитие, медицинскую страховку и ежемесячное пособие (2500 CNY для бакалавров ≈ 320€, 3000 CNY для магистров ≈ 390€, 3500 CNY для PhD). Топ вузы: Tsinghua, Peking University, Fudan, Zhejiang. Программы на китайском и английском. Сначала — год курсов китайского для программ на мандарине.",
     "min_age": 18, "max_age": 35, "duration_months": 48,
     "language_requirement": "HSK 4+ (для кит. программ) или IELTS 6.0+ (для англ.)",
     "salary_range": "2500–3500 CNY/мес (~320-450€) + жильё бесплатно",
     "cost": "Полностью бесплатно. Авиабилет самостоятельно (~600-900€)",
     "documents": "Загранпаспорт, диплом (апостиль), языковой сертификат, мотивационное письмо, медсправка, 2 рекомендательных письма",
     "deadline": "Февраль-апрель (зависит от вуза). Старт: сентябрь",
     "official_url": "https://www.campuschina.org",
     "residence_permit": True,
     "pros": "Полная стипендия\nТоп вузы мира\nУникальный культурный опыт\nЗнание китайского — ценный актив",
     "cons": "Языковой барьер\nОтличается культура\nИнтернет-ограничения (VPN)\nДалеко от дома",
     "career_opportunities": "Знание китайского + степень из китайского вуза — высоко ценится в международных компаниях. Зарплаты в Шанхае и Пекине: 3000-8000$/мес в IT.",
     "is_published": True},

    {"slug": "cn-teaching-english", "country_slug": "cn", "title": "Преподавание английского в Китае",
     "category": ProgramCategory.ARBEIT, "level": ProgramLevel.BEGINNER,
     "short_description": "Работа учителем английского в китайских школах: 1500-3000$/мес + жильё + авиабилет.",
     "description": "Китай испытывает огромный спрос на носителей и владеющих английским. Жильё и перелёт от работодателя.",
     "full_description": "Рынок преподавания английского в Китае огромен. Требования: гражданство англоязычной страны (или диплом по образованию/английскому) + бакалавриат. Зарплата: 12000-22000 CNY/мес (1600-3000$). Работодатель обычно предоставляет жильё, авиабилет, медстраховку, помощь с Z-Визой. Популярные работодатели: New Oriental, EF, Wall Street English, государственные школы. Также работа в международных детских садах.",
     "min_age": 21, "max_age": 55, "duration_months": 12,
     "language_requirement": "Носитель английского или C1",
     "salary_range": "12000–22000 CNY/мес (1600–3000 $)",
     "cost": "Z-виза ~200$, медосмотр ~100$. Авиабилет — от работодателя",
     "documents": "Загранпаспорт, диплом о высшем образовании, сертификат TEFL/TESOL, справка об отсутствии судимости, медсправка",
     "deadline": "Круглый год. Новый учебный год: сентябрь",
     "official_url": "https://www.chinajobcenter.com",
     "residence_permit": True,
     "pros": "Высокая зарплата по китайским меркам\nЖильё от работодателя\nУникальный опыт\nМного сохранять (низкие расходы)",
     "cons": "Языковой барьер в быту\nКультурные различия\nИнтернет-ограничения\nНужен бакалавриат",
     "career_opportunities": "После 2-3 лет преподавания — путь в EdTech, менеджмент или международные компании. Знание китайского — бонус.",
     "is_published": True},

    # ── CANADA ──
    {"slug": "ca-express-entry", "country_slug": "ca", "title": "Express Entry — ПМЖ Канады",
     "category": ProgramCategory.IMMIGRATION, "level": ProgramLevel.ADVANCED,
     "short_description": "Система Express Entry даёт ПМЖ Канады за 6-12 месяцев для квалифицированных специалистов.",
     "description": "Express Entry — балльная система отбора квалифицированных иммигрантов. CRS балл от 400+ даёт ПМЖ.",
     "full_description": "Express Entry — это балльная система (Comprehensive Ranking System, CRS) для получения Permanent Residency Канады. Баллы начисляются за: возраст (макс. в 25-35 лет), образование, опыт работы, знание английского/французского (IELTS/CELPIP), наличие предложения о работе, адаптируемость. Проходной балл: 450-550 CRS. Приглашения (ITA) рассылаются каждые 2 недели. Три потока: Federal Skilled Worker (FSW), Federal Skilled Trades (FST), Canadian Experience Class (CEC).",
     "min_age": 18, "max_age": None, "duration_months": 12,
     "language_requirement": "IELTS General 6.0+ (CLB 7+)",
     "salary_range": "После ПМЖ: 3000–8000+ CAD/мес в зависимости от профессии",
     "cost": "Сбор за обработку: 1365 CAD (~950€) на человека",
     "documents": "Загранпаспорт, IELTS/CELPIP, диплом + ECA (оценка), трудовые справки, медосмотр, полицейская справка",
     "deadline": "Приглашения рассылаются каждые 2 недели. Процесс: 6-12 месяцев",
     "official_url": "https://www.canada.ca/express-entry",
     "residence_permit": True,
     "pros": "ПМЖ за 6-12 месяцев\nПрава как у гражданина\nПрезентативная система\nВысокий уровень жизни\nПуть к гражданству за 3 года",
     "cons": "Нужен высокий CRS балл\nВысокая стоимость жизни\nХолодный климат\nДорогой процесс",
     "career_opportunities": "ПМЖ Канады открывает работу в любой компании. IT-специалисты: 80000-150000 CAD/год. Гражданство через 3 года ПМЖ.",
     "is_published": True},

    # ── USA ──
    {"slug": "us-work-travel", "country_slug": "us", "title": "Work and Travel USA",
     "category": ProgramCategory.ARBEIT, "level": ProgramLevel.BEGINNER,
     "short_description": "Лето в США для студентов: работа + путешествия по J-1 визе. 1200-2500$/мес.",
     "description": "Work and Travel — 4 месяца работы и путешествий в США по программе J-1 для студентов очной формы.",
     "full_description": "Work and Travel USA — программа культурного обмена на J-1 визе для студентов очных форм обучения. Участники работают в курортных зонах, национальных парках, отелях, ресторанах США (май-сентябрь). Зарплата 10-20$/час (минимальная зарплата в США зависит от штата). После окончания рабочего периода — 30 дней на путешествия по США. Агентства-спонсоры: CIEE, InterExchange, CCI.",
     "min_age": 18, "max_age": 28, "duration_months": 5,
     "language_requirement": "B1 английский (разговорный)",
     "salary_range": "10–20 $/час (≈1200–2500 $/мес)",
     "cost": "Участие в программе 500-1000$, виза J-1 ~185$, авиабилет ~700-1200$",
     "documents": "Студенческий билет/справка, загранпаспорт, договор с агентством, DS-2019, SEVIS-сбор",
     "deadline": "Регистрация: ноябрь-март. Сезон: май-сентябрь",
     "official_url": "https://www.ciee.org/work-travel",
     "residence_permit": False,
     "pros": "Уникальный американский опыт\nАнглийский на практике\nМного вакансий\nПутешествия по США\nСтуденческая программа",
     "cons": "Ограничен студентами\nВысокие расходы на участие\nТолько лето\nНе даёт ВНЖ",
     "career_opportunities": "J-1 опыт в США — ценная строчка в резюме. Некоторые участники потом получают H-1B или возвращаются по другим визам.",
     "is_published": True},

    {"slug": "us-au-pair", "country_slug": "us", "title": "Au Pair USA",
     "category": ProgramCategory.AU_PAIR, "level": ProgramLevel.BEGINNER,
     "short_description": "Au Pair в американской семье: 195$/нед + проживание + университетские курсы на 500$.",
     "description": "Au Pair USA — J-1 виза на 1-2 года. Уход за детьми до 45 ч/нед, жильё, питание, 500$ на образование.",
     "full_description": "Au Pair USA — государственная программа культурного обмена по J-1 визе. Американская семья платит минимум 195.75$/нед, предоставляет комнату, 3-разовое питание и 500$ на обучение в местном колледже (обязательное условие программы). Нагрузка до 45 ч/нед (уход за детьми). Длительность: 12 месяцев с возможностью продления до 24 месяцев. Спонсоры: APIA, Cultural Care, Au Pair in America. Возраст: 18-26 лет.",
     "min_age": 18, "max_age": 26, "duration_months": 12,
     "language_requirement": "B1 английский",
     "salary_range": "195.75 $/нед (~850 $/мес) + жильё и питание",
     "cost": "Участие в программе 400-900$, виза J-1 ~185$, авиабилет ~700-1200$",
     "documents": "Загранпаспорт, мотивационное письмо, справки об опыте с детьми, видеозаявка, медсправка, сертификат первой помощи",
     "deadline": "Круглый год. Подбор семьи: 2-4 месяца",
     "official_url": "https://www.aupairinamerica.com",
     "residence_permit": False,
     "pros": "Жизнь в любом штате США\nАнглийский на практике\nОбразовательный компонент\nОпыт американской семьи",
     "cons": "Зависимость от семьи\nВысокие расходы на участие\nМного работы с детьми\nОграничение по возрасту",
     "career_opportunities": "После Au Pair USA многие поступают в американские колледжи или находят другую работу в США по другим визам (F-1, H-1B).",
     "is_published": True},
]

async def seed_programs_3():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as db:
        for data in PROGRAMS:
            exists = (await db.execute(select(Program).where(Program.slug == data["slug"]))).scalar_one_or_none()
            if not exists:
                db.add(Program(**data))
                print(f"✅ Program: {data['title']}")
            else:
                print(f"ℹ️  Program {data['slug']} exists")
        await db.commit()
    print("🎓 Programs batch 3 done!")

if __name__ == "__main__":
    asyncio.run(seed_programs_3())
