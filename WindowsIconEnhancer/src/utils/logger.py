"""Logging configuration for Windows Icon Enhancer."""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime


def setup_logger(log_dir: Path = None, log_level: str = "INFO") -> logging.Logger:
    """Set up application logger."""
    if log_dir is None:
        log_dir = Path.home() / ".windows_icon_enhancer" / "logs"

    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("windows_icon_enhancer")
    logger.setLevel(getattr(logging, log_level))

    # File handler
    log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setLevel(getattr(logging, log_level))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
