import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import database as db
from config.config import ADMIN_IDS
from localization.texts import t

logger = logging.getLogger(__name__)
router = Router(name="admin")


@router.message(Command("admin"))
async def admin_panel(message: Message) -> None:
    user_id = message.from_user.id

    if user_id not in ADMIN_IDS:
        await message.answer(t("not_admin", "en"))
        return

    lang = await db.get_user_lang(user_id)
    total_users = await db.get_total_users()
    click_rows = await db.get_affiliate_stats()

    if click_rows:
        clicks_text = "\n".join(
            f"  {r['room']} [{r['lang']}]: <b>{r['clicks']}</b>" for r in click_rows
        )
    else:
        clicks_text = "  — no clicks yet —"

    await message.answer(
        text=t("admin_stats", lang, users=total_users, clicks=clicks_text),
        parse_mode="HTML",
    )
    logger.info("Admin panel accessed by user %s", user_id)
