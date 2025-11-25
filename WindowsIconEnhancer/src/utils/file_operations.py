"""File operations utilities."""

import os
import shutil
import stat
from pathlib import Path
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


def copy_file_with_backup(source: Path, destination: Path) -> bool:
    """Copy file and create backup of destination if it exists."""
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)

        if destination.exists():
            backup_path = destination.with_suffix(destination.suffix + ".backup")
            shutil.copy2(destination, backup_path)
            logger.info(f"Created backup: {backup_path}")

        shutil.copy2(source, destination)
        logger.info(f"Copied {source} to {destination}")
        return True
    except Exception as e:
        logger.error(f"Failed to copy file: {e}")
        return False


def remove_readonly(func, path, exc_info):
    """Error handler for readonly files."""
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR | stat.S_IREAD)
        func(path)
    else:
        raise


def delete_file(path: Path) -> bool:
    """Safely delete a file."""
    try:
        if path.exists():
            path.unlink()
            logger.info(f"Deleted file: {path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to delete file {path}: {e}")
        return False


def get_file_icon_path(file_path: Path) -> Optional[Path]:
    """Extract icon path from file."""
    # This would use Windows API to extract embedded icons
    # For now, returns the file itself if it's an icon
    try:
        if file_path.suffix.lower() in [".ico", ".cur"]:
            return file_path
    except Exception as e:
        logger.error(f"Failed to get icon path: {e}")

    return None


def is_file_locked(file_path: Path) -> bool:
    """Check if file is locked by another process."""
    try:
        with open(file_path, "rb"):
            return False
    except IOError:
        return True


def find_files_by_extension(
    directory: Path, extensions: List[str], recursive: bool = True
) -> List[Path]:
    """Find files by extension in directory."""
    try:
        pattern = "**/*" if recursive else "*"
        files = []

        for ext in extensions:
            if not ext.startswith("."):
                ext = "." + ext

            for file in directory.glob(f"{pattern}{ext}"):
                if file.is_file():
                    files.append(file)

        return sorted(files)
    except Exception as e:
        logger.error(f"Failed to find files: {e}")
        return []


def get_common_icon_locations() -> List[Path]:
    """Get common icon locations in Windows."""
    paths = [
        Path.home() / "AppData" / "Local" / "Programs",
        Path("C:\\Program Files"),
        Path("C:\\Program Files (x86)"),
        Path.home() / "Desktop",
        Path.home() / "Pictures",
    ]

    return [p for p in paths if p.exists()]


def create_shortcut_backup(shortcut_path: Path) -> Optional[Path]:
    """Create backup of shortcut properties."""
    try:
        backup_path = shortcut_path.with_suffix(shortcut_path.suffix + ".backup")
        shutil.copy2(shortcut_path, backup_path)
        logger.info(f"Created shortcut backup: {backup_path}")
        return backup_path
    except Exception as e:
        logger.error(f"Failed to backup shortcut: {e}")
        return None


def get_file_size_formatted(file_path: Path) -> str:
    """Get human-readable file size."""
    try:
        size = file_path.stat().st_size
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
    except Exception as e:
        logger.error(f"Failed to get file size: {e}")
        return "Unknown"


def get_directory_size(directory: Path) -> int:
    """Get total size of directory."""
    total = 0
    try:
        for path in directory.rglob("*"):
            if path.is_file():
                total += path.stat().st_size
    except Exception as e:
        logger.error(f"Failed to calculate directory size: {e}")
    return total
