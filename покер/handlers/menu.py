import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import database as db
from keyboards.language import language_keyboard
from keyboards.main_menu import main_menu_keyboard
from keyboards.poker_types import poker_types_keyboard
from keyboards.theory import theory_menu_keyboard
from keyboards.training import training_menu_keyboard
from localization.texts import t
from states.states import LanguageSelection

logger = logging.getLogger(__name__)
router = Router(name="menu")


async def _get_lang(user_id: int) -> str:
    return await db.get_user_lang(user_id)


@router.message(F.text)
async def menu_text_router(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    lang = await _get_lang(user_id)
    text = message.text

    if text == t("btn_theory", lang):
        await message.answer(
            t("theory_menu_title", lang),
            parse_mode="HTML",
            reply_markup=theory_menu_keyboard(lang),
        )
    elif text == t("btn_training", lang):
        await message.answer(
            t("training_menu_title", lang),
            parse_mode="HTML",
            reply_markup=training_menu_keyboard(lang),
        )
    elif text == t("btn_poker_types", lang):
        await message.answer(
            t("poker_types_title", lang),
            parse_mode="HTML",
            reply_markup=poker_types_keyboard(lang),
        )
    elif text == t("btn_progress", lang):
        from handlers.progress import show_progress

        await show_progress(message, lang)
    elif text == t("btn_play_real", lang):
        from handlers.affiliate import show_affiliate_menu

        await show_affiliate_menu(message, lang)
    elif text == t("btn_change_lang", lang):
        await state.set_state(LanguageSelection.choosing)
        await message.answer(
            t("choose_language", lang),
            reply_markup=language_keyboard(),
        )
    elif text in (t("btn_tips", lang), t("btn_quiz", lang)):
        await message.answer(t("coming_soon", lang), parse_mode="HTML")
    else:
        await message.answer(
            t("welcome", lang),
            parse_mode="HTML",
            reply_markup=main_menu_keyboard(lang),
        )


@router.callback_query(F.data == "menu:main")
async def back_to_main(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await _get_lang(callback.from_user.id)
    await state.clear()
    await callback.message.answer(
        text=t("welcome", lang),
        parse_mode="HTML",
        reply_markup=main_menu_keyboard(lang),
    )
    await callback.answer()
