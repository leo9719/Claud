"""Logging configuration for Poker Academy Bot."""

import logging
import sys
from pathlib import Path

from config.config import LOG_LEVEL, LOG_FILE


def setup_logging() -> None:
    fmt = "%(asctime)s  %(levelname)-8s  %(name)s  %(message)s"
    formatter = logging.Formatter(fmt)

    root = logging.getLogger()
    root.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    if root.handlers:
        return

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    log_path = Path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)
