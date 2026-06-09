"""Main reply keyboard."""

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from localization.texts import t


def main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [
        t("btn_theory", lang),
        t("btn_training", lang),
        t("btn_poker_types", lang),
        t("btn_progress", lang),
        t("btn_tips", lang),
        t("btn_quiz", lang),
        t("btn_change_lang", lang),
    ]
    for label in buttons:
        builder.button(text=label)
    builder.button(text=t("btn_play_real", lang))
    builder.adjust(2, 2, 2, 1, 1)
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Choose an option...",
    )
