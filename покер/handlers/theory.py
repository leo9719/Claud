import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery

import database as db
from handlers.affiliate import send_post_lesson_nudge
from keyboards.theory import theory_menu_keyboard
from localization.texts import t

logger = logging.getLogger(__name__)
router = Router(name="theory")

_THEORY_CONTENT: dict[str, dict[str, str]] = {
    "basics": {
        "ru": (
            "🎴 <b>Основы покера</b>\n\n"
            "Покер — карточная игра с неполной информацией. "
            "Главная цель — выиграть банк, либо имея лучшую комбинацию карт, "
            "либо заставив всех соперников сбросить карты.\n\n"
            "<b>Старшинство комбинаций (от слабой к сильной):</b>\n"
            "1. Старшая карта\n2. Пара\n3. Две пары\n4. Тройка\n"
            "5. Стрит\n6. Флэш\n7. Фулл-хаус\n8. Каре\n"
            "9. Стрит-флэш\n10. Роял-флэш"
        ),
        "en": (
            "🎴 <b>Poker Basics</b>\n\n"
            "Poker is a card game of incomplete information. "
            "The goal is to win the pot either by having the best hand "
            "or making all opponents fold.\n\n"
            "<b>Hand rankings (weak → strong):</b>\n"
            "1. High Card\n2. One Pair\n3. Two Pair\n4. Three of a Kind\n"
            "5. Straight\n6. Flush\n7. Full House\n8. Four of a Kind\n"
            "9. Straight Flush\n10. Royal Flush"
        ),
    },
    "preflop": {
        "ru": (
            "🂡 <b>Префлоп стратегия</b>\n\n"
            "Префлоп — это действия до появления общих карт.\n\n"
            "<b>Сильные стартовые руки:</b>\n"
            "AA, KK, QQ, JJ, AKs — всегда поднимаем.\n\n"
            "<b>Позиция критична!</b> С поздней позиции "
            "(BTN, CO) можно играть значительно шире."
        ),
        "en": (
            "🂡 <b>Preflop Strategy</b>\n\n"
            "Preflop is all action before community cards are dealt.\n\n"
            "<b>Premium hands:</b>\n"
            "AA, KK, QQ, JJ, AKs — always raise.\n\n"
            "<b>Position is critical!</b> From late position "
            "(BTN, CO) you can open a much wider range."
        ),
    },
    "postflop": {
        "ru": "🃏 <b>Постфлоп</b>\n\n🚧 Подробный контент скоро...",
        "en": "🃏 <b>Postflop</b>\n\n🚧 Detailed content coming soon...",
    },
    "bankroll": {
        "ru": "💰 <b>Управление банкроллом</b>\n\n🚧 Подробный контент скоро...",
        "en": "💰 <b>Bankroll Management</b>\n\n🚧 Detailed content coming soon...",
    },
    "psychology": {
        "ru": "🧠 <b>Психология покера</b>\n\n🚧 Подробный контент скоро...",
        "en": "🧠 <b>Poker Psychology</b>\n\n🚧 Detailed content coming soon...",
    },
}


@router.callback_query(F.data.startswith("theory:"))
async def show_theory_topic(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await db.get_user_lang(user_id)
    topic = callback.data.split(":", 1)[1]

    content_map = _THEORY_CONTENT.get(topic, {})
    content = content_map.get(lang) or content_map.get("en", t("coming_soon", lang))

    await callback.message.edit_text(
        text=content,
        parse_mode="HTML",
        reply_markup=theory_menu_keyboard(lang),
    )
    await db.save_progress(user_id, f"theory_{topic}")
    await send_post_lesson_nudge(callback.message, lang)
    await callback.answer()
