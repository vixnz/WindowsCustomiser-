"""Icon management system."""

import os
import logging
from pathlib import Path
from typing import List, Optional, Tuple
from PIL import Image
from dataclasses import dataclass
import struct
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class IconInfo:
    """Information about an icon."""

    path: Path
    name: str
    size: int  # File size in bytes
    width: int = 0
    height: int = 0
    format: str = "unknown"
    is_embedded: bool = False
    created_date: str = ""

    def __post_init__(self):
        """Initialize additional fields."""
        if not self.created_date and self.path.exists():
            timestamp = self.path.stat().st_mtime
            self.created_date = datetime.fromtimestamp(timestamp).isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "path": str(self.path),
            "name": self.name,
            "size": self.size,
            "width": self.width,
            "height": self.height,
            "format": self.format,
            "is_embedded": self.is_embedded,
            "created_date": self.created_date,
        }


class IconManager:
    """Manages icon operations."""

    SUPPORTED_FORMATS = {".ico", ".cur", ".bmp", ".png", ".jpg", ".jpeg", ".gif"}
    MAX_ICON_SIZE = 50 * 1024 * 1024  # 50MB

    def __init__(self):
        """Initialize icon manager."""
        self.icon_cache = {}

    def get_icon_info(self, icon_path: Path) -> Optional[IconInfo]:
        """Get information about an icon."""
        try:
            if not icon_path.exists():
                logger.warning(f"Icon file does not exist: {icon_path}")
                return None

            if icon_path.suffix.lower() not in self.SUPPORTED_FORMATS:
                logger.warning(f"Unsupported icon format: {icon_path.suffix}")
                return None

            size = icon_path.stat().st_size
            if size > self.MAX_ICON_SIZE:
                logger.warning(f"Icon file too large: {size} bytes")
                return None

            # Get image dimensions
            width, height = 0, 0
            try:
                with Image.open(icon_path) as img:
                    width, height = img.size
            except Exception as e:
                logger.debug(f"Could not read image dimensions: {e}")

            icon_info = IconInfo(
                path=icon_path,
                name=icon_path.stem,
                size=size,
                width=width,
                height=height,
                format=icon_path.suffix.lower()[1:],  # Remove the dot
                is_embedded=self._is_embedded_icon(icon_path),
            )

            return icon_info
        except Exception as e:
            logger.error(f"Failed to get icon info: {e}")
            return None

    def validate_icon(self, icon_path: Path) -> Tuple[bool, str]:
        """Validate icon file."""
        try:
            if not icon_path.exists():
                return False, "Icon file does not exist"

            if icon_path.suffix.lower() not in self.SUPPORTED_FORMATS:
                return False, f"Unsupported format: {icon_path.suffix}"

            size = icon_path.stat().st_size
            if size > self.MAX_ICON_SIZE:
                return False, f"Icon too large: {size / 1024 / 1024:.2f}MB"

            # Try to open as image
            try:
                with Image.open(icon_path) as img:
                    if img.size[0] < 16 or img.size[1] < 16:
                        return False, "Icon resolution too small (minimum 16x16)"
            except Exception as e:
                return False, f"Invalid icon file: {e}"

            return True, ""
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False, str(e)

    def convert_icon(
        self, source_path: Path, target_path: Path, target_format: str = "ico"
    ) -> bool:
        """Convert icon to different format."""
        try:
            with Image.open(source_path) as img:
                # Convert RGBA to RGB if needed for JPG
                if target_format.lower() == "jpg" and img.mode == "RGBA":
                    rgb_img = Image.new("RGB", img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[3])
                    rgb_img.save(target_path, format=target_format.upper())
                else:
                    img.save(target_path, format=target_format.upper())

            logger.info(f"Icon converted: {source_path} -> {target_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to convert icon: {e}")
            return False

    def resize_icon(self, icon_path: Path, size: Tuple[int, int]) -> Optional[Image.Image]:
        """Resize icon to specified dimensions."""
        try:
            with Image.open(icon_path) as img:
                resized = img.resize(size, Image.Resampling.LANCZOS)
                return resized
        except Exception as e:
            logger.error(f"Failed to resize icon: {e}")
            return None

    def extract_icon_from_exe(
        self, exe_path: Path, icon_index: int = 0
    ) -> Optional[Path]:
        """Extract icon from executable file."""
        try:
            # This would require Windows API access
            # For now, return None to indicate not implemented
            logger.info(f"Icon extraction from {exe_path} not yet implemented")
            return None
        except Exception as e:
            logger.error(f"Failed to extract icon: {e}")
            return None

    def get_icon_colors(self, icon_path: Path) -> Optional[dict]:
        """Extract dominant colors from icon."""
        try:
            with Image.open(icon_path) as img:
                # Resize for faster processing
                img.thumbnail((100, 100))

                # Convert to RGB
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # Get colors (simplified)
                colors = img.getcolors(maxcolors=256)
                if colors:
                    dominant_color = max(colors, key=lambda x: x[0])[1]
                    return {"dominant": dominant_color, "total_unique": len(colors)}

            return None
        except Exception as e:
            logger.error(f"Failed to extract colors: {e}")
            return None

    def batch_convert_icons(
        self, source_dir: Path, target_dir: Path, target_format: str = "ico"
    ) -> Tuple[int, int]:
        """Convert multiple icons at once."""
        success_count = 0
        error_count = 0

        try:
            target_dir.mkdir(parents=True, exist_ok=True)

            for icon_file in source_dir.glob("*"):
                if icon_file.suffix.lower() in self.SUPPORTED_FORMATS:
                    target_path = target_dir / icon_file.with_suffix(f".{target_format}").name
                    if self.convert_icon(icon_file, target_path, target_format):
                        success_count += 1
                    else:
                        error_count += 1

            logger.info(f"Batch conversion: {success_count} succeeded, {error_count} failed")
            return success_count, error_count
        except Exception as e:
            logger.error(f"Batch conversion error: {e}")
            return success_count, error_count

    def search_icons(self, directory: Path, pattern: str = "") -> List[IconInfo]:
        """Search for icons in directory."""
        icons = []

        try:
            for file_path in directory.rglob("*"):
                if file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                    if pattern == "" or pattern.lower() in file_path.name.lower():
                        icon_info = self.get_icon_info(file_path)
                        if icon_info:
                            icons.append(icon_info)

            return sorted(icons, key=lambda x: x.name)
        except Exception as e:
            logger.error(f"Icon search error: {e}")
            return []

    def _is_embedded_icon(self, file_path: Path) -> bool:
        """Check if file has embedded icons."""
        try:
            # Check if file is an exe/dll with embedded resources
            if file_path.suffix.lower() in [".exe", ".dll"]:
                return True
            return False
        except Exception:
            return False

    def get_system_icons(self) -> List[IconInfo]:
        """Get system icon locations."""
        system_icon_paths = [
            Path("C:\\Windows\\System32"),
            Path("C:\\Windows\\SysWOW64"),
        ]

        icons = []
        for path in system_icon_paths:
            if path.exists():
                icons.extend(self.search_icons(path, ".ico"))

        return icons[:100]  # Limit to first 100
