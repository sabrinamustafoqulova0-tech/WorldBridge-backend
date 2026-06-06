"""Seed articles about studying and working abroad."""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./germanypath.db")

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database import Base, engine as db_engine

engine = create_async_engine(DATABASE_URL, echo=False)
Session = async_sessionmaker(engine, expire_on_commit=False)

ARTICLES = [
    {
        "slug": "kak-nayti-rabotu-v-germanii",
        "title": "Как найти работу в Германии в 2024 году",
        "title_en": "How to Find a Job in Germany in 2024",
        "excerpt": "Пошаговое руководство по поиску работы в Германии: где искать вакансии, как составить резюме и пройти собеседование.",
        "excerpt_en": "A step-by-step guide to finding a job in Germany: where to look for vacancies, how to write a resume and pass an interview.",
        "content": """Германия — одна из крупнейших экономик мира и страна с огромным спросом на квалифицированных специалистов. В этой статье мы расскажем, как найти работу в Германии шаг за шагом.

## Где искать вакансии

Основные платформы для поиска работы в Германии:
- **Indeed.de** — крупнейший агрегатор вакансий
- **StepStone.de** — популярная платформа для специалистов
- **LinkedIn** — международная профессиональная сеть
- **Xing** — немецкий аналог LinkedIn
- **Bundesagentur für Arbeit** — официальная биржа труда

## Как составить резюме

Немецкое резюме (Lebenslauf) имеет свои особенности:
- Фото обязательно
- Личные данные: дата рождения, гражданство
- Хронологический порядок (от последнего к первому)
- Максимум 2 страницы

## Знание языка

Для большинства позиций требуется немецкий B1-B2. Для IT и международных компаний достаточно английского.

## Виза

С 2024 года действует Chancenkarte — виза для поиска работы без предварительного оффера.""",
        "content_en": """Germany is one of the world's largest economies with huge demand for skilled workers. Here's how to find a job step by step.

## Where to Look for Jobs

Main job search platforms in Germany:
- **Indeed.de** — largest job aggregator
- **StepStone.de** — popular platform for professionals
- **LinkedIn** — international professional network
- **Xing** — German LinkedIn equivalent
- **Bundesagentur für Arbeit** — official employment agency

## Resume Tips

German CV (Lebenslauf) has specific features:
- Photo is mandatory
- Personal data: date of birth, citizenship
- Reverse chronological order
- Maximum 2 pages

## Language Requirements

Most positions require German B1-B2. For IT and international companies, English is sufficient.

## Visa

Since 2024, the Chancenkarte allows job seekers to enter Germany without a prior job offer.""",
        "cover_image_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800",
        "is_published": True,
    },
    {
        "slug": "ausbildung-chto-eto-takoe",
        "title": "Ausbildung: что это такое и как поступить",
        "title_en": "Ausbildung: What It Is and How to Apply",
        "excerpt": "Полное руководство по немецкой системе профессионального обучения Ausbildung: специальности, зарплаты, требования и процесс подачи заявки.",
        "excerpt_en": "Complete guide to the German Ausbildung vocational training system: specialties, salaries, requirements and application process.",
        "content": """Ausbildung — это уникальная немецкая система дуального профессионального образования, которая сочетает практику на предприятии и теорию в школе.

## Как работает система

3-4 дня в неделю студент работает на предприятии и получает зарплату, 1-2 дня учится в Berufsschule (профессиональной школе). Длительность: 2-3.5 года.

## Популярные специальности

- **Fachinformatiker** (IT-специалист) — 1000-1100€/мес
- **Pflegefachkraft** (медсестра/медбрат) — 900-1000€/мес
- **Mechatroniker** (мехатроник) — 750-900€/мес
- **Koch** (повар) — 600-800€/мес
- **Kaufmann** (менеджер) — 700-900€/мес

## Требования

- Возраст от 16 лет
- Немецкий язык B1-B2
- Аттестат об образовании (признанный в Германии)
- Мотивационное письмо на немецком

## Как подать заявку

1. Найти работодателя на ausbildung.de или make-it-in-germany.com
2. Отправить резюме и мотивационное письмо
3. Пройти собеседование
4. Подписать Ausbildungsvertrag
5. Оформить визу в посольстве Германии""",
        "content_en": """Ausbildung is Germany's unique dual vocational education system combining workplace practice and classroom theory.

## How the System Works

3-4 days per week students work at a company and receive a salary, 1-2 days they attend Berufsschule (vocational school). Duration: 2-3.5 years.

## Popular Specialties

- **Fachinformatiker** (IT specialist) — €1000-1100/month
- **Pflegefachkraft** (nurse) — €900-1000/month
- **Mechatroniker** (mechatronics) — €750-900/month
- **Koch** (chef) — €600-800/month
- **Kaufmann** (manager) — €700-900/month

## Requirements

- Age 16+
- German language B1-B2
- Educational certificate (recognized in Germany)
- Motivation letter in German

## How to Apply

1. Find employer on ausbildung.de or make-it-in-germany.com
2. Send resume and motivation letter
3. Pass interview
4. Sign Ausbildungsvertrag
5. Apply for visa at German embassy""",
        "cover_image_url": "https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=800",
        "is_published": True,
    },
    {
        "slug": "au-pair-v-evrope",
        "title": "Au Pair в Европе: полное руководство 2024",
        "title_en": "Au Pair in Europe: Complete Guide 2024",
        "excerpt": "Всё что нужно знать об Au Pair программах в Германии, Франции, Австрии и других странах Европы.",
        "excerpt_en": "Everything you need to know about Au Pair programs in Germany, France, Austria and other European countries.",
        "content": """Au Pair — это программа культурного обмена, при которой молодой человек живёт с принимающей семьёй, помогает с детьми и изучает язык страны.

## Условия программы

- **Возраст**: 18-26 лет (в Норвегии до 30)
- **Нагрузка**: до 30 часов в неделю
- **Длительность**: 6-24 месяца
- **Жильё и питание**: бесплатно от семьи

## Карманные деньги по странам

| Страна | Карманные деньги |
|--------|-----------------|
| Швейцария | 800 CHF/мес |
| Норвегия | 5900 NOK/мес (~530€) |
| Бельгия | 450€/мес |
| Франция | 380€/мес |
| Германия | 280€/мес |
| Австрия | 410€/мес |

## Как найти семью

- AuPairWorld.net
- AuPair.com
- GreatAuPair.com
- Через агентства

## Советы

1. Внимательно изучайте профиль семьи
2. Проведите несколько видеозвонков перед согласием
3. Уточните все условия в договоре
4. Убедитесь что оплата языковых курсов включена""",
        "content_en": """Au Pair is a cultural exchange program where a young person lives with a host family, helps with children and learns the country's language.

## Program Conditions

- **Age**: 18-26 years (Norway up to 30)
- **Workload**: up to 30 hours per week
- **Duration**: 6-24 months
- **Housing and meals**: free from family

## Pocket Money by Country

| Country | Pocket Money |
|---------|-------------|
| Switzerland | 800 CHF/month |
| Norway | 5900 NOK/month (~€530) |
| Belgium | €450/month |
| France | €380/month |
| Germany | €280/month |
| Austria | €410/month |

## How to Find a Family

- AuPairWorld.net
- AuPair.com
- GreatAuPair.com
- Through agencies

## Tips

1. Study the family profile carefully
2. Have several video calls before agreeing
3. Clarify all conditions in the contract
4. Make sure language course payment is included""",
        "cover_image_url": "https://images.unsplash.com/photo-1476703993599-0035a21b17a9?w=800",
        "is_published": True,
    },
    {
        "slug": "besplatnoe-obrazovanie-v-evrope",
        "title": "Бесплатное образование в Европе: где и как",
        "title_en": "Free Education in Europe: Where and How",
        "excerpt": "Обзор стран Европы с бесплатным или очень доступным высшим образованием для иностранных студентов.",
        "excerpt_en": "Overview of European countries with free or very affordable higher education for international students.",
        "content": """Многие не знают, что в Европе можно получить высококачественное образование практически бесплатно. Рассказываем о лучших вариантах.

## Германия

Государственные университеты Германии не берут плату за обучение ни с немцев, ни с иностранцев. Платится только семестровый взнос ~300€, который включает проездной.

**Требования**: немецкий B2/C1 или IELTS 6.0+ для англоязычных программ.

## Норвегия

Единственная страна Западной Европы с полностью бесплатным образованием для всех. Семестровый взнос ~600 NOK (~55€).

**Требования**: IELTS 6.0+ (большинство программ на английском).

## Чехия

Государственные вузы Чехии бесплатны для тех, кто учится на чешском языке. Год подготовительных курсов — 600-1500€.

## Польша

Бесплатно для студентов, поступивших на польскоязычные программы. Стипендия NAWA: 1250-1600 PLN/мес.

## Финляндия

Платное для граждан вне ЕС (8000-15000€/год), но обширные стипендии от Aalto University и Finland Scholarship Programme.

## Франция

Государственные вузы взимают символическую плату 170-380€/год. Стипендия Eiffel: 1181€/мес.""",
        "content_en": """Many don't know that in Europe you can get high-quality education almost for free. Here are the best options.

## Germany

German state universities charge no tuition fees for Germans or foreigners. Only a semester fee of ~€300 is paid, which includes a transit pass.

**Requirements**: German B2/C1 or IELTS 6.0+ for English programs.

## Norway

The only Western European country with completely free education for everyone. Semester fee ~600 NOK (~€55).

**Requirements**: IELTS 6.0+ (most programs in English).

## Czech Republic

State universities in Czech Republic are free for those studying in Czech. One year of preparatory courses: €600-1500.

## Poland

Free for students admitted to Polish-language programs. NAWA scholarship: 1250-1600 PLN/month.

## Finland

Paid for non-EU citizens (€8000-15000/year), but extensive scholarships from Aalto University and Finland Scholarship Programme.

## France

State universities charge a symbolic fee of €170-380/year. Eiffel scholarship: €1181/month.""",
        "cover_image_url": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
        "is_published": True,
    },
    {
        "slug": "kak-vyuchit-nemetskiy-yazyk",
        "title": "Как выучить немецкий язык с нуля до B2",
        "title_en": "How to Learn German from Scratch to B2",
        "excerpt": "Практическое руководство по изучению немецкого языка: лучшие ресурсы, методы и сроки.",
        "excerpt_en": "Practical guide to learning German: best resources, methods and timelines.",
        "content": """Немецкий язык открывает двери в Германию, Австрию и Швейцарию. Вот как эффективно его выучить.

## Сроки обучения

- A1-A2: 3-4 месяца (интенсив)
- B1: 6-8 месяцев
- B2: 12-15 месяцев

## Лучшие ресурсы

### Бесплатные
- **Deutsche Welle** (dw.com/learn-german) — официальный немецкий ресурс
- **Duolingo** — для начинающих
- **YouTube каналы**: Easy German, DaF Kanal
- **Anki** — для запоминания слов

### Платные
- **Goethe-Institut** — официальные курсы и экзамены
- **italki** — уроки с носителями
- **Lingoda** — онлайн курсы

## Сертификаты

Для Ausbildung и работы: **Goethe-Zertifikat B1/B2** или **telc Deutsch**.
Для университета: **DSH** или **TestDaF**.

## Советы

1. Занимайтесь каждый день хотя бы 30 минут
2. Смотрите немецкие сериалы с субтитрами
3. Найдите языкового партнёра
4. Практикуйте разговорный с первого дня""",
        "content_en": """German opens doors to Germany, Austria and Switzerland. Here's how to learn it effectively.

## Learning Timeline

- A1-A2: 3-4 months (intensive)
- B1: 6-8 months
- B2: 12-15 months

## Best Resources

### Free
- **Deutsche Welle** (dw.com/learn-german) — official German resource
- **Duolingo** — for beginners
- **YouTube channels**: Easy German, DaF Kanal
- **Anki** — for vocabulary memorization

### Paid
- **Goethe-Institut** — official courses and exams
- **italki** — lessons with native speakers
- **Lingoda** — online courses

## Certificates

For Ausbildung and work: **Goethe-Zertifikat B1/B2** or **telc Deutsch**.
For university: **DSH** or **TestDaF**.

## Tips

1. Study every day for at least 30 minutes
2. Watch German series with subtitles
3. Find a language partner
4. Practice speaking from day one""",
        "cover_image_url": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800",
        "is_published": True,
    },
    {
        "slug": "stipendii-dlya-inostrantsev",
        "title": "Топ-10 стипендий для иностранных студентов в 2024",
        "title_en": "Top 10 Scholarships for International Students in 2024",
        "excerpt": "Обзор лучших государственных и частных стипендий для студентов из СНГ: Türkiye Bursları, CSC, Fulbright, DAAD и другие.",
        "excerpt_en": "Overview of the best government and private scholarships for CIS students: Türkiye Bursları, CSC, Fulbright, DAAD and others.",
        "content": """Стипендии — лучший способ получить образование за рубежом без финансовых затрат. Вот самые доступные варианты.

## 1. Türkiye Bursları (Турция)
Полная стипендия: обучение + жильё + 700-1400 TRY/мес + авиабилет.
Дедлайн: февраль-март. Сайт: turkiyeburslari.gov.tr

## 2. CSC Scholarship (Китай)
Chinese Government Scholarship: обучение + жильё + 2500-3500 CNY/мес.
Дедлайн: март-апрель. Сайт: campuschina.org

## 3. Fulbright (США)
Самая престижная стипендия: обучение + 2000-2500$/мес + авиабилет.
Дедлайн: май-июль (через посольство США). Сайт: fulbrightonline.org

## 4. DAAD (Германия)
Немецкая служба академических обменов: стипендии для магистров и PhD.
Стипендия: 861-1200€/мес. Сайт: daad.de

## 5. Swedish Institute (Швеция)
SISGP: полное обучение + 11000 SEK/мес + авиабилет.
Дедлайн: февраль. Сайт: si.se

## 6. Eiffel (Франция)
Стипендия для магистров: 1181€/мес + обучение бесплатно.
Дедлайн: январь. Сайт: campusfrance.org

## 7. Swiss Excellence (Швейцария)
Правительственная стипендия: 1920 CHF/мес + обучение.
Дедлайн: ноябрь-декабрь. Сайт: sbfi.admin.ch

## 8. VLIR-UOS (Бельгия)
Для магистров из развивающихся стран: до 1200€/мес.
Сайт: vliruos.be

## 9. NAWA (Польша)
Польская стипендия: 1250-1600 PLN/мес.
Сайт: nawa.gov.pl

## 10. Finland Scholarship
Для исследователей: 1500€/мес на 3-12 месяцев.
Сайт: scholarships.fi""",
        "content_en": """Scholarships are the best way to study abroad without financial costs. Here are the most accessible options.

## 1. Türkiye Bursları (Turkey)
Full scholarship: tuition + housing + 700-1400 TRY/month + flight ticket.
Deadline: February-March. Website: turkiyeburslari.gov.tr

## 2. CSC Scholarship (China)
Chinese Government Scholarship: tuition + housing + 2500-3500 CNY/month.
Deadline: March-April. Website: campuschina.org

## 3. Fulbright (USA)
Most prestigious scholarship: tuition + $2000-2500/month + flight.
Deadline: May-July (through US Embassy). Website: fulbrightonline.org

## 4. DAAD (Germany)
German Academic Exchange Service: scholarships for masters and PhD.
Stipend: €861-1200/month. Website: daad.de

## 5. Swedish Institute (Sweden)
SISGP: full tuition + 11000 SEK/month + flight ticket.
Deadline: February. Website: si.se

## 6. Eiffel (France)
Masters scholarship: €1181/month + free tuition.
Deadline: January. Website: campusfrance.org

## 7. Swiss Excellence (Switzerland)
Government scholarship: 1920 CHF/month + tuition.
Deadline: November-December. Website: sbfi.admin.ch

## 8. VLIR-UOS (Belgium)
For masters from developing countries: up to €1200/month.
Website: vliruos.be

## 9. NAWA (Poland)
Polish scholarship: 1250-1600 PLN/month.
Website: nawa.gov.pl

## 10. Finland Scholarship
For researchers: €1500/month for 3-12 months.
Website: scholarships.fi""",
        "cover_image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
        "is_published": True,
    },
    {
        "slug": "zhizn-v-germanii-pervye-shagi",
        "title": "Жизнь в Германии: первые шаги после переезда",
        "title_en": "Life in Germany: First Steps After Moving",
        "excerpt": "Практическое руководство для тех, кто только переехал в Германию: регистрация, банк, страховка, транспорт.",
        "excerpt_en": "Practical guide for those who just moved to Germany: registration, bank, insurance, transport.",
        "content": """Первые недели в Германии могут быть стрессовыми. Вот что нужно сделать сразу после приезда.

## 1. Anmeldung (регистрация)

В течение 2 недель после приезда нужно зарегистрироваться в Einwohnermeldeamt (офис регистрации жителей). Нужны: паспорт, договор аренды, заполненная форма.

## 2. Банковский счёт

Без счёта в немецком банке жить практически невозможно.
- **N26** или **Revolut** — быстрое открытие онлайн
- **Deutsche Bank**, **Commerzbank** — традиционные банки
- **Sparkasse** — местный сберегательный банк

## 3. Krankenversicherung (медицинская страховка)

Обязательна для всех! Для работающих — от работодателя. Для студентов — ~100€/мес (TK, AOK, Barmer).

## 4. Steuer-ID (налоговый номер)

Приходит по почте автоматически после регистрации. Нужен для работы и налоговой декларации.

## 5. Транспорт

- Deutschlandticket — 49€/мес, проезд по всей Германии
- Для студентов часто включён в семестровый взнос

## 6. Мобильный телефон

- **Aldi Talk**, **Lidl Connect** — дешёвые предоплаченные тарифы
- **O2**, **Telekom**, **Vodafone** — контрактные тарифы

## Полезные приложения

- **DB Navigator** — расписание поездов
- **Google Maps** — навигация
- **REWE**, **Kaufland** приложения — скидки в магазинах""",
        "content_en": """The first weeks in Germany can be stressful. Here's what you need to do right after arriving.

## 1. Anmeldung (Registration)

Within 2 weeks of arrival you need to register at the Einwohnermeldeamt (residents registration office). You need: passport, rental contract, filled form.

## 2. Bank Account

It's nearly impossible to live without a German bank account.
- **N26** or **Revolut** — quick online opening
- **Deutsche Bank**, **Commerzbank** — traditional banks
- **Sparkasse** — local savings bank

## 3. Krankenversicherung (Health Insurance)

Mandatory for everyone! For employees — from employer. For students — ~€100/month (TK, AOK, Barmer).

## 4. Steuer-ID (Tax Number)

Comes by mail automatically after registration. Needed for work and tax returns.

## 5. Transport

- Deutschlandticket — €49/month, travel throughout Germany
- For students often included in semester fee

## 6. Mobile Phone

- **Aldi Talk**, **Lidl Connect** — cheap prepaid plans
- **O2**, **Telekom**, **Vodafone** — contract plans

## Useful Apps

- **DB Navigator** — train schedules
- **Google Maps** — navigation
- **REWE**, **Kaufland** apps — store discounts""",
        "cover_image_url": "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=800",
        "is_published": True,
    },
    {
        "slug": "rabota-v-polshe-dlya-nachinayuschikh",
        "title": "Работа в Польше для начинающих: полный гайд",
        "title_en": "Working in Poland for Beginners: Complete Guide",
        "excerpt": "Как найти работу в Польше, оформить визу и начать зарабатывать в ЕС без знания языка.",
        "excerpt_en": "How to find a job in Poland, get a visa and start earning in the EU without knowing the language.",
        "content": """Польша — самый доступный путь в Евросоюз для граждан СНГ. Минимум требований, быстрое оформление.

## Почему Польша

- Самая простая рабочая виза в ЕС
- Оформление за 2-4 недели
- Много вакансий без знания языка
- Низкая стоимость жизни
- Близко к дому

## Популярные вакансии

**Заводы и склады**
- Amazon, DHL, UPS — 4000-6000 PLN/мес
- Volkswagen, LG, Miele — стабильная работа
- Biedronka, IKEA — производство

**Строительство**
- Каменщик, сварщик, маляр
- 5000-8000 PLN/мес

**Сельское хозяйство**
- Сбор фруктов и овощей (апрель-октябрь)
- 3000-5000 PLN/мес

## Как найти работу

1. Агентства: Grafton, Adecco, ManpowerGroup
2. Сайты: pracuj.pl, jobs.pl, olx.pl
3. Через знакомых в Польше
4. Напрямую к работодателю

## Виза

Работодатель оформляет oświadczenie (заявление). С ним едете в консульство. Виза D/06 выдаётся за 2-4 недели.

## Минимальная зарплата

2024 год: 4242 PLN/мес (~1060€). Реально на заводах: 5000-7000 PLN с переработками.""",
        "content_en": """Poland is the most accessible path to the European Union for CIS citizens. Minimum requirements, fast processing.

## Why Poland

- Easiest work visa in the EU
- Processing in 2-4 weeks
- Many jobs without language knowledge
- Low cost of living
- Close to home

## Popular Jobs

**Factories and Warehouses**
- Amazon, DHL, UPS — 4000-6000 PLN/month
- Volkswagen, LG, Miele — stable work
- Biedronka, IKEA — manufacturing

**Construction**
- Bricklayer, welder, painter
- 5000-8000 PLN/month

**Agriculture**
- Fruit and vegetable picking (April-October)
- 3000-5000 PLN/month

## How to Find a Job

1. Agencies: Grafton, Adecco, ManpowerGroup
2. Websites: pracuj.pl, jobs.pl, olx.pl
3. Through acquaintances in Poland
4. Directly to the employer

## Visa

The employer processes oświadczenie (declaration). With it you go to the consulate. D/06 visa is issued in 2-4 weeks.

## Minimum Wage

2024: 4242 PLN/month (~€1060). In factories with overtime: 5000-7000 PLN.""",
        "cover_image_url": "https://images.unsplash.com/photo-1519197924294-4ba991a11128?w=800",
        "is_published": True,
    },
]


async def seed():
    from models.article import Article

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with Session() as db:
        created = 0
        updated = 0
        for data in ARTICLES:
            from sqlalchemy import select
            existing = (
                await db.execute(select(Article).where(Article.slug == data["slug"]))
            ).scalar_one_or_none()

            if existing:
                for k, v in data.items():
                    setattr(existing, k, v)
                updated += 1
                print(f"[~] Updated: {data['title']}")
            else:
                db.add(Article(**data))
                created += 1
                print(f"[+] Created: {data['title']}")

        await db.commit()
        print(f"\nArticles: {created} created, {updated} updated.")


if __name__ == "__main__":
    asyncio.run(seed())