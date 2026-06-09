"""Central configuration for Poker Academy Bot."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

_DATA_DIR = Path("/app/data")
if _DATA_DIR.exists():
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    _DEFAULT_DB_PATH = str(_DATA_DIR / "poker_academy.db")
    _DEFAULT_LOG_FILE = str(_DATA_DIR / "bot.log")
else:
    _DEFAULT_DB_PATH = "poker_academy.db"
    _DEFAULT_LOG_FILE = "bot.log"


def _get_bot_token() -> str:
    return (
        os.getenv("BOT_TOKEN")
        or os.getenv("TELEGRAM_BOT_TOKEN")
        or os.getenv("API_TOKEN")
        or "YOUR_BOT_TOKEN_HERE"
    )


BOT_TOKEN: str = _get_bot_token()

ADMIN_IDS: list[int] = [
    int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()
]

DB_PATH: str = (
    os.getenv("DB_PATH")
    or os.getenv("DATABASE_PATH")
    or _DEFAULT_DB_PATH
)

SUPPORTED_LANGUAGES: list[str] = ["ru", "en", "es", "pt", "fr", "de"]
DEFAULT_LANGUAGE: str = "en"

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE: str = os.getenv("LOG_FILE", _DEFAULT_LOG_FILE)

WEBHOOK_MODE: str = os.getenv("WEBHOOK_MODE", "auto").lower()
WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/webhook")
WEBHOOK_SECRET: str | None = os.getenv("WEBHOOK_SECRET") or None
DOMAIN: str = os.getenv("DOMAIN", "")
PORT: int = int(os.getenv("PORT", "8080"))
