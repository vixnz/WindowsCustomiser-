"""System utilities for Windows-specific operations."""

import ctypes
import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Tuple, List

logger = logging.getLogger(__name__)


def is_admin() -> bool:
    """Check if running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        logger.error(f"Failed to check admin status: {e}")
        return False


def request_admin_privileges() -> bool:
    """Request administrator privileges."""
    if is_admin():
        return True

    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        return True
    except Exception as e:
        logger.error(f"Failed to elevate privileges: {e}")
        return False


def get_windows_version() -> str:
    """Get Windows version."""
    try:
        result = subprocess.run(
            ["cmd", "/c", "ver"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception as e:
        logger.error(f"Failed to get Windows version: {e}")
        return "Unknown"


def get_system_drive() -> str:
    """Get system drive letter."""
    return os.environ.get("SystemDrive", "C:")


def get_common_folders() -> dict:
    """Get common Windows system folders."""
    import winreg

    folders = {
        "Desktop": str(Path.home() / "Desktop"),
        "Documents": str(Path.home() / "Documents"),
        "Downloads": str(Path.home() / "Downloads"),
        "Pictures": str(Path.home() / "Pictures"),
        "Programs": str(Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"),
        "All Users Programs": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    }
    return folders


def clear_icon_cache() -> bool:
    """Clear Windows icon cache."""
    try:
        icon_cache_path = Path.home() / "AppData" / "Local" / "IconCache.db"
        if icon_cache_path.exists():
            os.remove(icon_cache_path)
            logger.info("Icon cache cleared successfully")
            return True
    except Exception as e:
        logger.error(f"Failed to clear icon cache: {e}")
        return False


def refresh_shell_icons() -> bool:
    """Refresh shell icons."""
    try:
        subprocess.run(
            [
                "powershell",
                "-Command",
                "Remove-Item -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\.*' -Force -ErrorAction SilentlyContinue",
            ],
            check=False,
        )
        logger.info("Shell icons refreshed")
        return True
    except Exception as e:
        logger.error(f"Failed to refresh shell icons: {e}")
        return False


def restart_explorer() -> bool:
    """Restart Windows Explorer."""
    try:
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], check=False)
        subprocess.Popen("explorer.exe")
        logger.info("Explorer restarted")
        return True
    except Exception as e:
        logger.error(f"Failed to restart explorer: {e}")
        return False


def get_process_privileges_level() -> str:
    """Get current process privilege level."""
    return "Administrator" if is_admin() else "User"


def enable_long_paths() -> bool:
    """Enable long path support on Windows 10+."""
    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\FileSystem",
            0,
            winreg.KEY_WRITE,
        ) as key:
            winreg.SetValueEx(key, "LongPathsEnabled", 0, winreg.REG_DWORD, 1)
            logger.info("Long paths enabled")
            return True
    except Exception as e:
        logger.error(f"Failed to enable long paths: {e}")
        return False


def get_system_info() -> dict:
    """Get comprehensive system information."""
    info = {
        "windows_version": get_windows_version(),
        "is_admin": is_admin(),
        "system_drive": get_system_drive(),
        "privilege_level": get_process_privileges_level(),
    }
    return info
