"""Input validation utilities."""

import re
from pathlib import Path
from typing import Tuple


def validate_file_path(path: str) -> Tuple[bool, str]:
    """Validate file path."""
    try:
        p = Path(path)
        if p.exists():
            return True, ""
        return False, "File does not exist"
    except Exception as e:
        return False, str(e)


def validate_icon_file(path: str) -> Tuple[bool, str]:
    """Validate icon file format."""
    try:
        p = Path(path)
        valid_extensions = {".ico", ".cur", ".bmp", ".png", ".jpg", ".jpeg"}
        if p.suffix.lower() in valid_extensions:
            return True, ""
        return False, f"Invalid icon format. Supported: {', '.join(valid_extensions)}"
    except Exception as e:
        return False, str(e)


def validate_folder_path(path: str) -> Tuple[bool, str]:
    """Validate folder path."""
    try:
        p = Path(path)
        if p.is_dir():
            return True, ""
        return False, "Path is not a valid directory"
    except Exception as e:
        return False, str(e)


def validate_registry_path(path: str) -> Tuple[bool, str]:
    """Validate Windows registry path."""
    pattern = r"^HKEY_[A-Z_]+\\[\\a-zA-Z0-9_]*$"
    if re.match(pattern, path):
        return True, ""
    return False, "Invalid registry path format"


def validate_shortcut_path(path: str) -> Tuple[bool, str]:
    """Validate shortcut path."""
    try:
        p = Path(path)
        if p.suffix.lower() in [".lnk"]:
            return True, ""
        return False, "File is not a valid shortcut (.lnk)"
    except Exception as e:
        return False, str(e)


def validate_batch_size(size: int) -> Tuple[bool, str]:
    """Validate batch size."""
    if 1 <= size <= 10000:
        return True, ""
    return False, "Batch size must be between 1 and 10000"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    invalid_chars = r'<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename
