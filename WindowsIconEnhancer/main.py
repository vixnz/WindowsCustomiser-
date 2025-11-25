#!/usr/bin/env python
"""Windows Icon Enhancer Pro - Main Application Entry Point."""

import sys
import logging
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils import setup_logger, ConfigManager, is_admin, request_admin_privileges
from PyQt5.QtWidgets import QApplication, QMessageBox
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

        # Check for admin privileges
        if not is_admin():
            reply = QMessageBox.warning(
                None,
                "Admin Privileges Required",
                "Windows Icon Enhancer Pro requires administrator privileges for full functionality.\n\n"
                "Would you like to restart with admin privileges?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                request_admin_privileges()
                sys.exit(0)
            else:
                QMessageBox.information(
                    None,
                    "Limited Mode",
                    "Running in limited mode. Some features may not work properly.",
                )

        # Create main window
        window = MainWindow()
        window.show()

        logger.info("Application started successfully")

        # Run application
        sys.exit(app.exec_())

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        QMessageBox.critical(
            None, "Error", f"Fatal error occurred:\n{e}\n\nCheck logs for details."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
