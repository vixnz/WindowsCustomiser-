"""Configuration management for Windows Icon Enhancer."""

import os
import json
from pathlib import Path
from typing import Any, Dict
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class AppConfig:
    """Application configuration."""

    theme: str = "dark"
    auto_backup: bool = True
    max_backups: int = 10
    check_updates: bool = True
    enable_logging: bool = True
    log_level: str = "INFO"
    window_width: int = 1200
    window_height: int = 800
    window_maximized: bool = False
    last_backup_path: str = ""
    icon_preview_size: int = 128


class ConfigManager:
    """Manages application configuration."""

    def __init__(self, config_dir: str = None):
        """Initialize configuration manager."""
        if config_dir is None:
            config_dir = str(Path.home() / ".windows_icon_enhancer")

        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()

    def _load_config(self) -> AppConfig:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    return AppConfig(**data)
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                return AppConfig()
        return AppConfig()

    def save_config(self) -> bool:
        """Save configuration to file."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(asdict(self.config), f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return getattr(self.config, key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        if hasattr(self.config, key):
            setattr(self.config, key, value)
            self.save_config()
        else:
            logger.warning(f"Unknown configuration key: {key}")

    def get_backup_dir(self) -> Path:
        """Get backup directory."""
        backup_dir = self.config_dir / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        return backup_dir

    def get_cache_dir(self) -> Path:
        """Get cache directory."""
        cache_dir = self.config_dir / "cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir

    def get_log_dir(self) -> Path:
        """Get log directory."""
        log_dir = self.config_dir / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir
