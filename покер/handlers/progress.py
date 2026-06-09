import logging

from aiogram import Router
from aiogram.types import Message

import database as db
from keyboards.main_menu import main_menu_keyboard
from localization.texts import t

logger = logging.getLogger(__name__)
router = Router(name="progress")

_LEVEL_LABELS = {
    "beginner": {
        "ru": "Новичок",
        "en": "Beginner",
        "es": "Principiante",
        "pt": "Iniciante",
        "fr": "Débutant",
        "de": "Anfänger",
    },
    "intermediate": {
        "ru": "Средний",
        "en": "Intermediate",
        "es": "Intermedio",
        "pt": "Intermediário",
        "fr": "Intermédiaire",
        "de": "Mittel",
    },
    "advanced": {
        "ru": "Продвинутый",
        "en": "Advanced",
        "es": "Avanzado",
        "pt": "Avançado",
        "fr": "Avancé",
        "de": "Fortgeschritten",
    },
}


async def show_progress(message: Message, lang: str) -> None:
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    lessons = await db.count_completed_lessons(user_id)

    raw_level = user.get("level", "beginner") if user else "beginner"
    level_label = _LEVEL_LABELS.get(raw_level, {}).get(lang, raw_level.capitalize())

    await message.answer(
        text=(
            t("progress_title", lang)
            + "\n\n"
            + t(
                "progress_stats",
                lang,
                level=level_label,
                lessons=lessons,
                user_lang=lang.upper(),
            )
        ),
        parse_mode="HTML",
        reply_markup=main_menu_keyboard(lang),
    )
