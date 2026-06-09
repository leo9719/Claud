"""Poker Academy Bot — entry point."""

from __future__ import annotations

import asyncio
import logging
import sys

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config.config import BOT_TOKEN, DOMAIN, PORT, WEBHOOK_MODE, WEBHOOK_PATH, WEBHOOK_SECRET
from database import init_db
from handlers import admin, affiliate, menu, poker_types, progress, start, theory, training
from utils.logger import setup_logging

logger = logging.getLogger(__name__)


def should_use_webhook() -> bool:
    if WEBHOOK_MODE == "polling":
        return False
    if WEBHOOK_MODE == "webhook":
        return True
    return bool(DOMAIN)


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(admin.router)
    dp.include_router(start.router)
    dp.include_router(affiliate.router)
    dp.include_router(theory.router)
    dp.include_router(training.router)
    dp.include_router(poker_types.router)
    dp.include_router(progress.router)
    dp.include_router(menu.router)
    return dp


def create_bot() -> Bot:
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("BOT_TOKEN is not set.")
        sys.exit(1)
    return Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def on_startup(bot: Bot, dp: Dispatcher) -> None:
    await init_db()
    if should_use_webhook():
        url = f"https://{DOMAIN.rstrip('/')}{WEBHOOK_PATH}"
        await bot.set_webhook(url=url, secret_token=WEBHOOK_SECRET, allowed_updates=dp.resolve_used_update_types())
        logger.info("Webhook: %s", url)


async def on_shutdown(bot: Bot) -> None:
    if should_use_webhook():
        await bot.delete_webhook(drop_pending_updates=False)
    await bot.session.close()


async def run_polling(bot: Bot, dp: Dispatcher) -> None:
    await on_startup(bot, dp)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await on_shutdown(bot)


async def run_webhook(bot: Bot, dp: Dispatcher) -> None:
    await on_startup(bot, dp)

    app = web.Application()
    app.router.add_get("/", lambda r: web.Response(text="OK"))
    app.router.add_get("/health", lambda r: web.Response(text="OK"))
    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    webhook_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", PORT).start()
    logger.info("Listening on 0.0.0.0:%s", PORT)

    try:
        await asyncio.Event().wait()
    finally:
        await on_shutdown(bot)


async def main() -> None:
    setup_logging()
    bot = create_bot()
    dp = create_dispatcher()
    if should_use_webhook():
        if not DOMAIN:
            sys.exit("DOMAIN is required for webhook mode")
        await run_webhook(bot, dp)
    else:
        await run_polling(bot, dp)


if __name__ == "__main__":
    asyncio.run(main())
