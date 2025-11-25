"""Utilities package."""

from .config import ConfigManager, AppConfig
from .logger import setup_logger
from .permission_manager import PermissionManager
from .system_utils import (
    is_admin,
    request_admin_privileges,
    get_windows_version,
    get_system_drive,
    clear_icon_cache,
    restart_explorer,
    get_system_info,
)
from .file_operations import (
    copy_file_with_backup,
    delete_file,
    find_files_by_extension,
    get_common_icon_locations,
    get_file_size_formatted,
    get_directory_size,
)
from .validators import (
    validate_file_path,
    validate_icon_file,
    validate_folder_path,
    validate_registry_path,
    sanitize_filename,
)

__all__ = [
    "ConfigManager",
    "AppConfig",
    "setup_logger",
    "PermissionManager",
    "is_admin",
    "request_admin_privileges",
    "get_windows_version",
    "get_system_drive",
    "clear_icon_cache",
    "restart_explorer",
    "get_system_info",
    "copy_file_with_backup",
    "delete_file",
    "find_files_by_extension",
    "get_common_icon_locations",
    "get_file_size_formatted",
    "get_directory_size",
    "validate_file_path",
    "validate_icon_file",
    "validate_folder_path",
    "validate_registry_path",
    "sanitize_filename",
]
