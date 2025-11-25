"""Windows Registry management."""

import logging
import winreg
from typing import Optional, List, Tuple, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class RegistryManager:
    """Manages Windows Registry operations."""

    # Common registry hives
    HIVES = {
        "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
        "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
        "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
        "HKEY_USERS": winreg.HKEY_USERS,
        "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
    }

    # File type icon registry paths
    FILE_TYPE_ICON_PATHS = {
        ".txt": r"Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.txt\UserAssoc",
        ".doc": r"Software\Classes\.doc",
        ".docx": r"Software\Classes\.docx",
        ".pdf": r"Software\Classes\.pdf",
        ".xlsx": r"Software\Classes\.xlsx",
        ".pptx": r"Software\Classes\.pptx",
        ".jpg": r"Software\Classes\.jpg",
        ".png": r"Software\Classes\.png",
        ".mp4": r"Software\Classes\.mp4",
        ".zip": r"Software\Classes\.zip",
    }

    def __init__(self):
        """Initialize registry manager."""
        self.backup_data = {}

    def get_value(
        self,
        hive: str,
        path: str,
        value_name: str,
        default: Any = None,
    ) -> Optional[Any]:
        """Get registry value."""
        try:
            hive_handle = self.HIVES.get(hive)
            if not hive_handle:
                logger.error(f"Invalid hive: {hive}")
                return default

            with winreg.OpenKey(hive_handle, path, 0, winreg.KEY_READ) as key:
                value, _ = winreg.QueryValueEx(key, value_name)
                return value
        except FileNotFoundError:
            logger.debug(f"Registry path not found: {path}\\{value_name}")
            return default
        except Exception as e:
            logger.error(f"Failed to get registry value: {e}")
            return default

    def set_value(
        self,
        hive: str,
        path: str,
        value_name: str,
        value: Any,
        value_type: int = winreg.REG_SZ,
        backup_first: bool = True,
    ) -> bool:
        """Set registry value."""
        try:
            # Backup original value
            if backup_first:
                original = self.get_value(hive, path, value_name)
                backup_key = f"{hive}\\{path}\\{value_name}"
                self.backup_data[backup_key] = original

            hive_handle = self.HIVES.get(hive)
            if not hive_handle:
                logger.error(f"Invalid hive: {hive}")
                return False

            # Create key if it doesn't exist
            try:
                key = winreg.OpenKey(hive_handle, path, 0, winreg.KEY_WRITE)
            except FileNotFoundError:
                key = winreg.CreateKey(hive_handle, path)

            winreg.SetValueEx(key, value_name, 0, value_type, value)
            winreg.CloseKey(key)

            logger.info(f"Set registry value: {hive}\\{path}\\{value_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to set registry value: {e}")
            return False

    def delete_value(
        self,
        hive: str,
        path: str,
        value_name: str,
        backup_first: bool = True,
    ) -> bool:
        """Delete registry value."""
        try:
            # Backup original value
            if backup_first:
                original = self.get_value(hive, path, value_name)
                backup_key = f"{hive}\\{path}\\{value_name}"
                self.backup_data[backup_key] = original

            hive_handle = self.HIVES.get(hive)
            if not hive_handle:
                logger.error(f"Invalid hive: {hive}")
                return False

            with winreg.OpenKey(hive_handle, path, 0, winreg.KEY_WRITE) as key:
                winreg.DeleteValue(key, value_name)

            logger.info(f"Deleted registry value: {hive}\\{path}\\{value_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete registry value: {e}")
            return False

    def set_file_association_icon(
        self, file_extension: str, icon_path: Path
    ) -> bool:
        """Set icon for file type."""
        try:
            if not file_extension.startswith("."):
                file_extension = "." + file_extension

            if not icon_path.exists():
                logger.error(f"Icon file not found: {icon_path}")
                return False

            # Get or create file type
            file_type_path = fr"Software\Classes\{file_extension}"
            prog_id_path = fr"Software\Classes\{file_extension}\shell\open\command"

            # Set icon path
            icon_registry_path = fr"Software\Classes\{file_extension}\DefaultIcon"
            icon_value = str(icon_path)

            return self.set_value(
                "HKEY_CURRENT_USER",
                icon_registry_path,
                "",
                icon_value,
            )
        except Exception as e:
            logger.error(f"Failed to set file association icon: {e}")
            return False

    def set_folder_icon(self, icon_path: Path) -> bool:
        """Set icon for folders."""
        try:
            if not icon_path.exists():
                logger.error(f"Icon file not found: {icon_path}")
                return False

            folder_icon_path = r"Software\Classes\Folder\shell\open\command"
            icon_value = f'"{str(icon_path)}"'

            return self.set_value(
                "HKEY_CURRENT_USER",
                folder_icon_path,
                "Icon",
                icon_value,
            )
        except Exception as e:
            logger.error(f"Failed to set folder icon: {e}")
            return False

    def get_file_type_icon(self, file_extension: str) -> Optional[str]:
        """Get current icon for file type."""
        try:
            if not file_extension.startswith("."):
                file_extension = "." + file_extension

            icon_path = fr"Software\Classes\{file_extension}\DefaultIcon"
            icon_value = self.get_value(
                "HKEY_CURRENT_USER",
                icon_path,
                "",
            )

            return icon_value
        except Exception as e:
            logger.error(f"Failed to get file type icon: {e}")
            return None

    def restore_backup(self) -> int:
        """Restore all backed up registry values."""
        restored_count = 0

        try:
            for backup_key, original_value in self.backup_data.items():
                parts = backup_key.split("\\", 2)
                if len(parts) == 3:
                    hive, path, value_name = parts
                    if original_value is None:
                        self.delete_value(hive, path, value_name, backup_first=False)
                    else:
                        self.set_value(
                            hive, path, value_name, original_value, backup_first=False
                        )
                    restored_count += 1

            logger.info(f"Restored {restored_count} registry values")
            return restored_count
        except Exception as e:
            logger.error(f"Failed to restore backup: {e}")
            return 0

    def list_registry_keys(self, hive: str, path: str) -> List[str]:
        """List subkeys in registry path."""
        keys = []

        try:
            hive_handle = self.HIVES.get(hive)
            if not hive_handle:
                logger.error(f"Invalid hive: {hive}")
                return keys

            with winreg.OpenKey(hive_handle, path, 0, winreg.KEY_READ) as key:
                index = 0
                while True:
                    try:
                        subkey = winreg.EnumKey(key, index)
                        keys.append(subkey)
                        index += 1
                    except OSError:
                        break

            return keys
        except Exception as e:
            logger.error(f"Failed to list registry keys: {e}")
            return keys

    def validate_registry_path(self, hive: str, path: str) -> bool:
        """Validate if registry path exists."""
        try:
            hive_handle = self.HIVES.get(hive)
            if not hive_handle:
                return False

            winreg.OpenKey(hive_handle, path, 0, winreg.KEY_READ)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            logger.error(f"Failed to validate registry path: {e}")
            return False
