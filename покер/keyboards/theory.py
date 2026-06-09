"""Theory section keyboards."""

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from localization.texts import t


def theory_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    topics = [
        ("btn_theory_basics", "theory:basics"),
        ("btn_theory_preflop", "theory:preflop"),
        ("btn_theory_postflop", "theory:postflop"),
        ("btn_theory_bankroll", "theory:bankroll"),
        ("btn_theory_psychology", "theory:psychology"),
    ]
    for key, cb in topics:
        builder.button(text=t(key, lang), callback_data=cb)
    builder.button(text=t("btn_main_menu", lang), callback_data="menu:main")
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()
