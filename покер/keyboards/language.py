"""Language selection keyboard."""

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    languages = [
        ("🇷🇺 Русский", "lang:ru"),
        ("🇬🇧 English", "lang:en"),
        ("🇪🇸 Español", "lang:es"),
        ("🇧🇷 Português", "lang:pt"),
        ("🇫🇷 Français", "lang:fr"),
        ("🇩🇪 Deutsch", "lang:de"),
    ]
    for label, callback_data in languages:
        builder.button(text=label, callback_data=callback_data)
    builder.adjust(2)
    return builder.as_markup()
