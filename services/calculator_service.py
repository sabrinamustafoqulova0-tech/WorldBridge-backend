"""
CalculatorService — pure business logic for the relocation cost estimator.
No I/O: takes a CalculatorInput and returns a CalculatorResult synchronously.
Supports all 13 WorldBridge countries.
"""

from schemas.calculator import CalculatorInput, CalculatorResult

# Utility estimate if not included in rent (EUR/month, per person)
_UTILITIES_PER_PERSON = 80.0

# Kindergarten / childcare estimate per child
_CHILDCARE_PER_CHILD = 300.0

# City-specific rent multipliers per country
_CITY_MULTIPLIERS: dict[str, dict[str, float]] = {
    "de": {
        "münchen": 1.55, "munich": 1.55, "frankfurt": 1.35, "hamburg": 1.25,
        "berlin": 1.10, "köln": 1.05, "cologne": 1.05, "düsseldorf": 1.15,
        "stuttgart": 1.20, "leipzig": 0.85, "dresden": 0.80, "default": 1.00,
    },
    "fr": {
        "paris": 1.60, "lyon": 1.15, "marseille": 1.05, "bordeaux": 1.10,
        "toulouse": 1.08, "nice": 1.20, "default": 1.00,
    },
    "be": {
        "brussels": 1.30, "bruxelles": 1.30, "antwerp": 1.10, "ghent": 1.05,
        "liège": 1.00, "default": 1.00,
    },
    "ch": {
        "zürich": 1.30, "zurich": 1.30, "genf": 1.35, "geneva": 1.35,
        "basel": 1.15, "bern": 1.10, "lausanne": 1.20, "default": 1.00,
    },
    "at": {
        "wien": 1.25, "vienna": 1.25, "graz": 1.00, "salzburg": 1.10,
        "innsbruck": 1.05, "default": 1.00,
    },
    "pl": {
        "warsaw": 1.30, "warschau": 1.30, "krakow": 1.10, "kraków": 1.10,
        "wrocław": 1.10, "wroclaw": 1.10, "gdańsk": 1.05, "default": 1.00,
    },
    "cz": {
        "prague": 1.35, "prag": 1.35, "brno": 1.00, "ostrava": 0.90,
        "default": 1.00,
    },
    "se": {
        "stockholm": 1.40, "gothenburg": 1.15, "göteborg": 1.15,
        "malmö": 1.10, "default": 1.00,
    },
    "no": {
        "oslo": 1.35, "bergen": 1.15, "trondheim": 1.05,
        "stavanger": 1.20, "default": 1.00,
    },
    "fi": {
        "helsinki": 1.30, "tampere": 1.05, "turku": 1.00,
        "espoo": 1.25, "default": 1.00,
    },
    "tr": {
        "istanbul": 1.25, "ankara": 1.00, "izmir": 1.05,
        "antalya": 1.10, "default": 1.00,
    },
    "cn": {
        "beijing": 1.30, "shanghai": 1.35, "guangzhou": 1.15,
        "shenzhen": 1.20, "chengdu": 1.00, "default": 1.00,
    },
    "ca": {
        "toronto": 1.35, "vancouver": 1.40, "montreal": 1.10,
        "calgary": 1.15, "ottawa": 1.10, "default": 1.00,
    },
    "us": {
        "new york": 1.70, "los angeles": 1.55, "san francisco": 1.65,
        "chicago": 1.30, "miami": 1.25, "boston": 1.40,
        "seattle": 1.45, "austin": 1.20, "default": 1.00,
    },
}

# Country-specific tip appended at the end
_COUNTRY_TIPS: dict[str, str] = {
    "de": "Откройте немецкий банковский счёт (например N26 или DKB) до прилёта — это ускорит получение первой зарплаты.",
    "fr": "Зарегистрируйтесь в CAF (Caisse d'Allocations Familiales) после приезда — вы можете получить субсидию на жильё.",
    "be": "В Бельгии обязательно зарегистрируйтесь в коммуне (commune) по месту жительства в течение 8 дней после приезда.",
    "ch": "Швейцария дорогая, но зарплаты одни из самых высоких в Европе. Откройте счёт в местном банке (PostFinance, UBS) как можно раньше.",
    "at": "В Австрии обязательно пройдите регистрацию (Meldezettel) по месту жительства в течение 3 дней после заселения.",
    "pl": "Польша и Чехия — одни из самых доступных стран Европы. Воспользуйтесь этим для формирования финансовой подушки.",
    "cz": "Польша и Чехия — одни из самых доступных стран Европы. Воспользуйтесь этим для формирования финансовой подушки.",
    "se": "В Швеции зарегистрируйтесь в Skatteverket (налоговая служба) для получения personnummer — без него сложно открыть счёт и снять жильё.",
    "no": "В Норвегии оформите D-nummer (временный номер) или personnummer в налоговой службе Skatteetaten — он нужен для всех официальных операций.",
    "fi": "В Финляндии зарегистрируйтесь в DVV (цифровые и населённые услуги) для получения финского личного номера.",
    "tr": "Откройте турецкий банковский счёт (например Ziraat Bank) и оформите ИНН — это упростит аренду жилья и коммунальные платежи.",
    "cn": "Зарегистрируйтесь в местном полицейском участке в течение 24 часов после заселения — это требование китайского законодательства.",
    "ca": "Откройте банковский счёт до прилёта (Wise или Revolut) — переводы в первые месяцы будут дешевле. Оформите SIN (Social Insurance Number) в первые дни.",
    "us": "Откройте банковский счёт в первые дни (Chase, Bank of America) и оформите Social Security Number (SSN) или ITIN для финансовых операций.",
}


class CalculatorService:

    @staticmethod
    def calculate(data: CalculatorInput) -> CalculatorResult:
        country = getattr(data, "country", "de").lower().strip() or "de"
        city_key = data.city.lower().strip() if data.city else ""

        country_cities = _CITY_MULTIPLIERS.get(country, {})
        multiplier = country_cities.get(city_key, country_cities.get("default", 1.0))

        # ── One-time costs ────────────────────────────────────────────────────
        visa_docs = data.visa_fee + data.document_legalisation_cost
        flight_total = data.flight_cost * data.family_members
        one_time_total = visa_docs + flight_total

        # ── Monthly costs ─────────────────────────────────────────────────────
        housing = data.monthly_rent * multiplier
        if not data.utilities_included:
            housing += _UTILITIES_PER_PERSON * data.family_members
        if data.has_children:
            housing += _CHILDCARE_PER_CHILD

        lang_monthly = (
            data.language_course_price_per_month
            if data.language_course_months > 0
            else 0.0
        )
        misc = data.misc_monthly * data.family_members
        monthly_total = (
            housing
            + lang_monthly
            + data.health_insurance_monthly
            + misc
        )

        # ── Course & buffer totals ────────────────────────────────────────────
        lang_total = data.language_course_price_per_month * data.language_course_months
        savings_buffer = monthly_total * data.months_of_savings
        grand_total = one_time_total + lang_total + savings_buffer

        tips = CalculatorService._generate_tips(data, city_key, multiplier, country)

        return CalculatorResult(
            visa_and_documents=round(visa_docs, 2),
            flight_total=round(flight_total, 2),
            one_time_total=round(one_time_total, 2),
            housing_monthly=round(housing, 2),
            language_course_monthly=round(lang_monthly, 2),
            health_insurance_monthly=round(data.health_insurance_monthly, 2),
            misc_monthly=round(misc, 2),
            monthly_total=round(monthly_total, 2),
            language_course_total=round(lang_total, 2),
            savings_buffer=round(savings_buffer, 2),
            grand_total=round(grand_total, 2),
            tips=tips,
            city=data.city,
        )

    @staticmethod
    def _generate_tips(
        data: CalculatorInput, city_key: str, multiplier: float, country: str
    ) -> list[str]:
        tips: list[str] = []

        if multiplier > 1.3:
            tips.append(
                f"{data.city} — один из дорогих городов в этой стране. "
                "Рассмотрите пригороды или соседние города — аренда там на 20–30% ниже."
            )
        if data.language_course_months == 0:
            tips.append(
                "Даже базовый языковой курс (уровень A1–A2) значительно улучшит "
                "повседневную жизнь и перспективы трудоустройства."
            )
        if data.months_of_savings < 3:
            tips.append(
                "Финансовые советники рекомендуют иметь минимум 3 месяца расходов "
                "в качестве резервного буфера при переезде за рубеж."
            )
        if not data.utilities_included:
            tips.append(
                "Попробуйте найти жильё с включёнными коммунальными услугами — "
                "это упростит планирование бюджета и избавит от неожиданных счетов."
            )
        if data.family_members > 1:
            tips.append(
                "При переезде семьёй изучите доступные государственные субсидии "
                "на жильё и детские пособия в стране назначения."
            )
        if data.has_children:
            tips.append(
                "Уточните условия зачисления детей в школу заблаговременно — "
                "в большинстве стран это требует регистрации по месту жительства."
            )

        # Страно-специфичный совет
        country_tip = _COUNTRY_TIPS.get(country)
        if country_tip:
            tips.append(country_tip)

        if not tips:
            tips.append(
                "Хорошее планирование! Откройте счёт в местном банке заблаговременно "
                "— это сэкономит время и деньги при получении первого дохода."
            )

        return tips
