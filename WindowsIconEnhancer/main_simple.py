#!/usr/bin/env python
"""Windows Icon Enhancer Pro - Simpler Entry Point."""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils import setup_logger, ConfigManager
from PyQt5.QtWidgets import QApplication
from src.gui import MainWindow


def main():
    """Main application entry point."""
    # Setup logging
    config_manager = ConfigManager()
    logger = setup_logger(
        config_manager.get_log_dir(), config_manager.get("log_level", "INFO")
    )

    logger.info("=" * 80)
    logger.info("Windows Icon Enhancer Pro - Starting Application")
    logger.info("=" * 80)

    try:
        # Create QApplication
        app = QApplication(sys.argv)

        # Create main window
        window = MainWindow()
        window.show()

        logger.info("Application started successfully")

        # Run application
        sys.exit(app.exec_())

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
