"""Poker variants keyboards."""

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from localization.texts import t


def poker_types_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    variants = [
        ("btn_holdem", "poker:holdem"),
        ("btn_plo", "poker:plo"),
        ("btn_omaha_hilo", "poker:omaha_hilo"),
        ("btn_stud", "poker:stud"),
        ("btn_draw", "poker:draw"),
        ("btn_shortdeck", "poker:shortdeck"),
    ]
    for key, cb in variants:
        builder.button(text=t(key, lang), callback_data=cb)
    builder.button(text=t("btn_main_menu", lang), callback_data="menu:main")
    builder.adjust(2, 2, 2, 1)
    return builder.as_markup()
