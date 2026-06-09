# database.py
"""
Async SQLite database layer for Poker Academy Bot.
Uses aiosqlite for non-blocking I/O compatible with asyncio/aiogram.

Tables:
  users            – profile, language, registration timestamp
  user_progress    – lessons completed, quiz scores, level
  affiliate_clicks – every time a user follows an affiliate link
"""

import aiosqlite
import logging
from datetime import datetime
from config.config import DB_PATH

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Schema
# ─────────────────────────────────────────────────────────────────────────────
_DDL = """
CREATE TABLE IF NOT EXISTS users (
    user_id         INTEGER PRIMARY KEY,
    username        TEXT,
    first_name      TEXT,
    lang            TEXT    NOT NULL DEFAULT 'en',
    level           TEXT    NOT NULL DEFAULT 'beginner',
    registered_at   TEXT    NOT NULL,
    last_active     TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS user_progress (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id             INTEGER NOT NULL REFERENCES users(user_id),
    lesson_key          TEXT    NOT NULL,   -- e.g. 'theory_preflop', 'quiz_hands'
    completed_at        TEXT    NOT NULL,
    score               INTEGER DEFAULT 0,  -- for quizzes: correct answers
    max_score           INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS affiliate_clicks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    room        TEXT    NOT NULL,   -- 'smartlink', 'pokerok', etc.
    lang        TEXT    NOT NULL,
    source      TEXT    NOT NULL DEFAULT 'telegram_bot',
    clicked_at  TEXT    NOT NULL
);
"""


async def init_db() -> None:
    """Create all tables if they don't exist. Call once on bot startup."""
    from pathlib import Path

    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(_DDL)
        await db.commit()
    logger.info("Database initialised at %s", DB_PATH)


# ─────────────────────────────────────────────────────────────────────────────
# User operations
# ─────────────────────────────────────────────────────────────────────────────

async def upsert_user(
    user_id: int,
    username: str | None,
    first_name: str | None,
    lang: str = "en",
) -> None:
    """Insert a new user or update last_active timestamp."""
    now = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO users (user_id, username, first_name, lang, registered_at, last_active)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username    = excluded.username,
                first_name  = excluded.first_name,
                last_active = excluded.last_active
            """,
            (user_id, username, first_name, lang, now, now),
        )
        await db.commit()


async def get_user(user_id: int) -> dict | None:
    """Return a user row as dict, or None if not found."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def set_user_lang(user_id: int, lang: str) -> None:
    """Update the language preference for a user."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id)
        )
        await db.commit()


async def get_user_lang(user_id: int) -> str:
    """Return user's language code, defaulting to 'en'."""
    user = await get_user(user_id)
    return user["lang"] if user else "en"


async def set_user_level(user_id: int, level: str) -> None:
    """Update skill level: 'beginner', 'intermediate', 'advanced'."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET level = ? WHERE user_id = ?", (level, user_id)
        )
        await db.commit()


# ─────────────────────────────────────────────────────────────────────────────
# Progress operations
# ─────────────────────────────────────────────────────────────────────────────

async def save_progress(
    user_id: int,
    lesson_key: str,
    score: int = 0,
    max_score: int = 0,
) -> None:
    """Record that a user completed a lesson or quiz."""
    now = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO user_progress (user_id, lesson_key, completed_at, score, max_score)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, lesson_key, now, score, max_score),
        )
        await db.commit()


async def get_progress(user_id: int) -> list[dict]:
    """Return all progress records for a user."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM user_progress WHERE user_id = ? ORDER BY completed_at DESC",
            (user_id,),
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]


async def count_completed_lessons(user_id: int) -> int:
    """Count unique lessons completed by user."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT COUNT(DISTINCT lesson_key) FROM user_progress WHERE user_id = ?",
            (user_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0


# ─────────────────────────────────────────────────────────────────────────────
# Affiliate click tracking
# ─────────────────────────────────────────────────────────────────────────────

async def log_affiliate_click(user_id: int, room: str, lang: str) -> None:
    """Record when a user taps an affiliate link."""
    now = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO affiliate_clicks (user_id, room, lang, source, clicked_at)
            VALUES (?, ?, ?, 'telegram_bot', ?)
            """,
            (user_id, room, lang, now),
        )
        await db.commit()


async def get_affiliate_stats() -> list[dict]:
    """Admin: aggregate clicks per room."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """
            SELECT room, lang, COUNT(*) as clicks
            FROM affiliate_clicks
            GROUP BY room, lang
            ORDER BY clicks DESC
            """,
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]


async def get_total_users() -> int:
    """Admin: total registered users."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0