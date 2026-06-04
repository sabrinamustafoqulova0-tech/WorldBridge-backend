"""
utils/i18n.py — Backend localisation helpers.

Pattern: every localisable field FOO has optional companions FOO_en and FOO_tg.
The base field (FOO) stores the Russian content and acts as the ultimate fallback.

Fallback chain: FOO_{lang} → FOO_ru → FOO (base, which IS Russian)
"""

from typing import Any

SUPPORTED_LANGS = frozenset({"ru", "en", "tg"})


def normalize_lang(lang: str) -> str:
    return lang if lang in SUPPORTED_LANGS else "ru"


def get_localized(obj: Any, field: str, lang: str) -> Any:
    """
    Return the localized value for `field` on an ORM instance.

    Resolution order:
      1. {field}_{lang}  (e.g. title_en)
      2. {field}_ru      (explicit Russian column, if present)
      3. {field}         (base column — always the Russian content)
    """
    lang = normalize_lang(lang)

    if lang != "ru":
        val = getattr(obj, f"{field}_{lang}", None)
        if val:
            return val

    # Russian or fallback path
    val = getattr(obj, f"{field}_ru", None)
    if val:
        return val

    return getattr(obj, field, None)


def localize(obj: Any, lang: str, fields: list[str]) -> dict:
    """
    Convert an ORM instance to a plain dict with localised versions of *fields*.
    All other columns are included unchanged so Pydantic schemas get every
    required field.
    """
    from sqlalchemy import inspect as sa_inspect

    lang = normalize_lang(lang)

    try:
        mapper = sa_inspect(type(obj)).mapper
        result: dict = {col.key: getattr(obj, col.key) for col in mapper.column_attrs}
    except Exception:
        result = {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}

    for field in fields:
        result[field] = get_localized(obj, field, lang)

    return result


# Canonical lists of localisable fields per entity type
PROGRAM_I18N_FIELDS = [
    "title",
    "short_description",
    "description",
    "full_description",
]

ARTICLE_I18N_FIELDS = [
    "title",
    "excerpt",
    "content",
]

FAQ_I18N_FIELDS = [
    "question",
    "answer",
]

COUNTRY_I18N_FIELDS = [
    "name",
    "description",
]
