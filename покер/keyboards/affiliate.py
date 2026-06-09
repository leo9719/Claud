"""Affiliate keyboards."""

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.affiliates import ROOM_DISPLAY_NAMES
from localization.texts import t


def affiliate_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t("btn_best_room", lang), callback_data="affiliate:smartlink")
    for room in ["pokerok", "ggpoker", "pokerstars", "partypoker", "888poker"]:
        display = ROOM_DISPLAY_NAMES.get(room, room.capitalize())
        builder.button(text=display, callback_data=f"affiliate:{room}")
    builder.button(text=t("btn_main_menu", lang), callback_data="menu:main")
    builder.adjust(1, 2, 2, 1)
    return builder.as_markup()


def quick_affiliate_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t("btn_try_real_play", lang), callback_data="affiliate:smartlink")
    builder.button(text=t("btn_main_menu", lang), callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()
