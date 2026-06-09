import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery

import database as db
from handlers.affiliate import send_post_lesson_nudge
from keyboards.poker_types import poker_types_keyboard
from localization.texts import t

logger = logging.getLogger(__name__)
router = Router(name="poker_types")

_POKER_CONTENT: dict[str, dict[str, str]] = {
    "holdem": {
        "ru": (
            "♠️ <b>Техасский Холдем</b>\n\n"
            "Самый популярный вид покера в мире.\n\n"
            "<b>Правила:</b> каждый игрок получает 2 карманные карты. "
            "На борд выкладывается 5 общих карт (флоп 3 + тёрн 1 + ривер 1).\n\n"
            "<b>Цель:</b> составить лучшую 5-карточную комбинацию из 7 карт."
        ),
        "en": (
            "♠️ <b>Texas Hold'em</b>\n\n"
            "The world's most popular poker variant.\n\n"
            "<b>Rules:</b> each player receives 2 hole cards. "
            "5 community cards are dealt (flop 3 + turn 1 + river 1).\n\n"
            "<b>Goal:</b> make the best 5-card hand from 7 cards."
        ),
    },
    "plo": {
        "ru": (
            "♦️ <b>Пот-Лимит Омаха</b>\n\n"
            "Второй по популярности вид покера.\n\n"
            "<b>Отличие от Холдема:</b> 4 карманные карты вместо 2. "
            "Необходимо использовать ровно 2 карты из руки и 3 с борда."
        ),
        "en": (
            "♦️ <b>Pot-Limit Omaha</b>\n\n"
            "The world's second most popular poker variant.\n\n"
            "<b>Key difference:</b> 4 hole cards instead of 2. "
            "You must use exactly 2 hole cards and 3 community cards."
        ),
    },
    "omaha_hilo": {
        "ru": "♣️ <b>Омаха Хай-Лоу</b>\n\n🚧 Подробный контент скоро...",
        "en": "♣️ <b>Omaha Hi-Lo</b>\n\n🚧 Detailed content coming soon...",
    },
    "stud": {
        "ru": "🂾 <b>Семёрка Стад</b>\n\n🚧 Подробный контент скоро...",
        "en": "🂾 <b>Seven Card Stud</b>\n\n🚧 Detailed content coming soon...",
    },
    "draw": {
        "ru": "🎴 <b>Пятикарточный Дро</b>\n\n🚧 Подробный контент скоро...",
        "en": "🎴 <b>Five Card Draw</b>\n\n🚧 Detailed content coming soon...",
    },
    "shortdeck": {
        "ru": "⚡ <b>Шорт-Дек Холдем</b>\n\n🚧 Подробный контент скоро...",
        "en": "⚡ <b>Short Deck Hold'em</b>\n\n🚧 Detailed content coming soon...",
    },
}


@router.callback_query(F.data.startswith("poker:"))
async def show_poker_variant(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await db.get_user_lang(user_id)
    variant = callback.data.split(":", 1)[1]

    content_map = _POKER_CONTENT.get(variant, {})
    content = content_map.get(lang) or content_map.get("en", t("coming_soon", lang))

    await callback.message.edit_text(
        text=content,
        parse_mode="HTML",
        reply_markup=poker_types_keyboard(lang),
    )
    await db.save_progress(user_id, f"poker_{variant}")
    await send_post_lesson_nudge(callback.message, lang)
    await callback.answer()
