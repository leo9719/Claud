import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import database as db
from config.affiliates import ROOM_DISPLAY_NAMES, get_link
from keyboards.affiliate import affiliate_menu_keyboard, quick_affiliate_keyboard
from localization.texts import t

logger = logging.getLogger(__name__)
router = Router(name="affiliate")


async def show_affiliate_menu(message: Message, lang: str) -> None:
    await message.answer(
        text=t("affiliate_intro", lang) + "\n\n" + t("affiliate_disclaimer", lang),
        parse_mode="HTML",
        reply_markup=affiliate_menu_keyboard(lang),
    )


@router.callback_query(F.data == "affiliate:_menu")
async def back_to_affiliate_menu(callback: CallbackQuery) -> None:
    lang = await db.get_user_lang(callback.from_user.id)
    await callback.message.edit_text(
        text=t("affiliate_intro", lang) + "\n\n" + t("affiliate_disclaimer", lang),
        parse_mode="HTML",
        reply_markup=affiliate_menu_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("affiliate:"))
async def affiliate_room_selected(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await db.get_user_lang(user_id)
    room = callback.data.split(":", 1)[1]

    url = get_link(room, user_id, lang)
    await db.log_affiliate_click(user_id, room, lang)

    room_name = ROOM_DISPLAY_NAMES.get(room, room.capitalize())
    logger.info("Affiliate click: user=%s room=%s lang=%s", user_id, room, lang)

    builder = InlineKeyboardBuilder()
    builder.button(text=f"🚀 {room_name} →", url=url)
    builder.button(text=t("btn_back", lang), callback_data="affiliate:_menu")
    builder.adjust(1)

    await callback.message.edit_text(
        text=(
            f"🎰 <b>{room_name}</b>\n\n"
            f"🔗 Нажми кнопку ниже, чтобы перейти на сайт рума.\n\n"
            + t("affiliate_disclaimer", lang)
        ),
        parse_mode="HTML",
        reply_markup=builder.as_markup(),
    )
    await callback.answer()


async def send_post_quiz_nudge(
    message: Message,
    lang: str,
    score: int,
    max_score: int,
) -> None:
    if max_score > 0 and (score / max_score) >= 0.6:
        await message.answer(
            text=t("affiliate_after_quiz", lang, score=score, max=max_score),
            parse_mode="HTML",
            reply_markup=quick_affiliate_keyboard(lang),
        )


async def send_post_lesson_nudge(message: Message, lang: str) -> None:
    await message.answer(
        text=t("affiliate_after_lesson", lang),
        parse_mode="HTML",
        reply_markup=quick_affiliate_keyboard(lang),
    )
