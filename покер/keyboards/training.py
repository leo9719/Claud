"""Training section keyboards."""

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from localization.texts import t


def training_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    modes = [
        ("btn_train_hands", "train:hands"),
        ("btn_train_decisions", "train:decisions"),
        ("btn_train_equity", "train:equity"),
        ("btn_train_simulator", "train:simulator"),
        ("btn_train_quiz", "train:quiz"),
    ]
    for key, cb in modes:
        builder.button(text=t(key, lang), callback_data=cb)
    builder.button(text=t("btn_main_menu", lang), callback_data="menu:main")
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()


def quiz_answer_keyboard(
    options: list[str],
    question_id: int,
    lang: str,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i, option in enumerate(options):
        builder.button(text=option, callback_data=f"quiz_answer:{question_id}:{i}")
    builder.button(text=t("btn_main_menu", lang), callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()
