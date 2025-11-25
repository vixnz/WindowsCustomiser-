"""System context menu integration."""

import logging
import winreg
from typing import Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)


class ContextMenuManager:
    """Manages Windows shell context menus."""

    # Registry paths for context menus
    SHELL_CONTEXT_PATH = r"Software\Classes\*\shell\Windows Icon Enhancer"
    FOLDER_CONTEXT_PATH = r"Software\Classes\Folder\shell\Windows Icon Enhancer"

    def __init__(self):
        """Initialize context menu manager."""
        pass

    def add_file_context_menu(self, icon_path: Optional[Path] = None) -> bool:
        """Add context menu option to files."""
        try:
            context_path = self.SHELL_CONTEXT_PATH
            command_path = f"{context_path}\\command"

            # Create registry entries
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, context_path) as key:
                winreg.SetValueEx(
                    key, "", 0, winreg.REG_SZ, "Change Icon with Icon Enhancer"
                )

                if icon_path and icon_path.exists():
                    winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, str(icon_path))

            # Add command
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_path) as key:
                cmd = f'"{Path(__file__).parent.parent.parent / "main.py"}" --change-icon "%1"'
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, cmd)

            logger.info("File context menu added")
            return True
        except Exception as e:
            logger.error(f"Failed to add file context menu: {e}")
            return False

    def add_folder_context_menu(self, icon_path: Optional[Path] = None) -> bool:
        """Add context menu option to folders."""
        try:
            context_path = self.FOLDER_CONTEXT_PATH
            command_path = f"{context_path}\\command"

            # Create registry entries
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, context_path) as key:
                winreg.SetValueEx(
                    key, "", 0, winreg.REG_SZ, "Change Icon with Icon Enhancer"
                )

                if icon_path and icon_path.exists():
                    winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, str(icon_path))

            # Add command
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_path) as key:
                cmd = f'"{Path(__file__).parent.parent.parent / "main.py"}" --change-icon "%1"'
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, cmd)

            logger.info("Folder context menu added")
            return True
        except Exception as e:
            logger.error(f"Failed to add folder context menu: {e}")
            return False

    def remove_file_context_menu(self) -> bool:
        """Remove context menu option from files."""
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, self.SHELL_CONTEXT_PATH)
            logger.info("File context menu removed")
            return True
        except FileNotFoundError:
            logger.debug("File context menu not found")
            return True
        except Exception as e:
            logger.error(f"Failed to remove file context menu: {e}")
            return False

    def remove_folder_context_menu(self) -> bool:
        """Remove context menu option from folders."""
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, self.FOLDER_CONTEXT_PATH)
            logger.info("Folder context menu removed")
            return True
        except FileNotFoundError:
            logger.debug("Folder context menu not found")
            return True
        except Exception as e:
            logger.error(f"Failed to remove folder context menu: {e}")
            return False

    def is_context_menu_enabled(self) -> bool:
        """Check if context menu is enabled."""
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, self.SHELL_CONTEXT_PATH, 0, winreg.KEY_READ
            ):
                return True
        except FileNotFoundError:
            return False
        except Exception as e:
            logger.error(f"Failed to check context menu status: {e}")
            return False
