import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import database as db
from keyboards.language import language_keyboard
from keyboards.main_menu import main_menu_keyboard
from localization.texts import t
from states.states import LanguageSelection

logger = logging.getLogger(__name__)
router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    user = message.from_user
    await db.upsert_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
    )

    existing = await db.get_user(user.id)
    if existing and existing.get("lang"):
        lang = existing["lang"]
        await state.clear()
        await message.answer(
            text=t("welcome", lang),
            parse_mode="HTML",
            reply_markup=main_menu_keyboard(lang),
        )
    else:
        await state.set_state(LanguageSelection.choosing)
        await message.answer(
            text=t("choose_language", "en"),
            reply_markup=language_keyboard(),
        )


@router.callback_query(F.data.startswith("lang:"))
async def language_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    lang = callback.data.split(":")[1]
    user = callback.from_user

    await db.upsert_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        lang=lang,
    )
    await db.set_user_lang(user.id, lang)
    await state.clear()

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        text=t("welcome", lang),
        parse_mode="HTML",
        reply_markup=main_menu_keyboard(lang),
    )
    await callback.answer()
    logger.info("User %s selected language %s", user.id, lang)
