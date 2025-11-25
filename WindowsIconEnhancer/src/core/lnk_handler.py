"""Windows shortcut (LNK) file manipulation using pywin32."""

import logging
from pathlib import Path
from typing import Optional, Tuple
import struct

logger = logging.getLogger(__name__)


class LNKShortcutHandler:
    """Handles Windows .lnk (shortcut) file operations using COM."""

    def __init__(self):
        """Initialize shortcut handler."""
        self._shell = None
        self._initialize_com()

    def _initialize_com(self) -> bool:
        """Initialize Windows COM connection."""
        try:
            import win32com.client

            self._shell = win32com.client.Dispatch("WScript.Shell")
            logger.info("Windows COM initialized for shortcut handling")
            return True
        except ImportError:
            logger.warning("pywin32 not available - shortcut COM operations will be unavailable")
            return False
        except Exception as e:
            logger.error(f"Failed to initialize COM: {e}")
            return False

    def read_shortcut(self, shortcut_path: Path) -> Optional[dict]:
        """Read shortcut properties."""
        try:
            if not shortcut_path.exists():
                logger.error(f"Shortcut not found: {shortcut_path}")
                return None

            if not self._shell:
                logger.error("COM not initialized")
                return None

            shortcut = self._shell.CreateShortcut(str(shortcut_path))

            return {
                "path": str(shortcut_path),
                "target": shortcut.TargetPath,
                "arguments": shortcut.Arguments,
                "working_directory": shortcut.WorkingDirectory,
                "icon_location": shortcut.IconLocation,
                "description": shortcut.Description,
                "window_style": shortcut.WindowStyle,
                "hotkey": shortcut.Hotkey,
            }
        except Exception as e:
            logger.error(f"Failed to read shortcut: {e}")
            return None

    def write_shortcut(
        self,
        shortcut_path: Path,
        target: Optional[str] = None,
        arguments: Optional[str] = None,
        working_directory: Optional[str] = None,
        icon_location: Optional[str] = None,
        description: Optional[str] = None,
    ) -> bool:
        """Write/update shortcut properties."""
        try:
            if not self._shell:
                logger.error("COM not initialized")
                return False

            shortcut = self._shell.CreateShortcut(str(shortcut_path))

            # Update properties if provided
            if target is not None:
                shortcut.TargetPath = target
            if arguments is not None:
                shortcut.Arguments = arguments
            if working_directory is not None:
                shortcut.WorkingDirectory = working_directory
            if icon_location is not None:
                shortcut.IconLocation = icon_location
            if description is not None:
                shortcut.Description = description

            shortcut.Save()
            logger.info(f"Shortcut updated: {shortcut_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to write shortcut: {e}")
            return False

    def set_shortcut_icon(
        self, shortcut_path: Path, icon_path: Path, icon_index: int = 0
    ) -> Tuple[bool, str]:
        """Set icon for shortcut."""
        try:
            if not shortcut_path.exists():
                return False, f"Shortcut not found: {shortcut_path}"
            if not icon_path.exists():
                return False, f"Icon not found: {icon_path}"

            # Format icon location as "path,index"
            icon_location = f"{icon_path},{icon_index}"

            success = self.write_shortcut(shortcut_path, icon_location=icon_location)
            if success:
                return True, f"Icon set: {icon_path}"
            else:
                return False, "Failed to update shortcut"

        except Exception as e:
            logger.error(f"Failed to set shortcut icon: {e}")
            return False, f"Error: {str(e)}"

    def create_shortcut(
        self,
        target_path: Path,
        shortcut_path: Path,
        arguments: str = "",
        working_directory: str = "",
        icon_path: Optional[Path] = None,
        description: str = "",
    ) -> Tuple[bool, str]:
        """Create a new shortcut."""
        try:
            if not target_path.exists():
                return False, f"Target not found: {target_path}"

            if not self._shell:
                return False, "COM not initialized"

            shortcut = self._shell.CreateShortcut(str(shortcut_path))
            shortcut.TargetPath = str(target_path)
            shortcut.Arguments = arguments
            shortcut.WorkingDirectory = working_directory or str(target_path.parent)
            shortcut.Description = description

            if icon_path and icon_path.exists():
                shortcut.IconLocation = str(icon_path)

            shortcut.Save()
            logger.info(f"Shortcut created: {shortcut_path}")
            return True, f"Shortcut created: {shortcut_path}"

        except Exception as e:
            logger.error(f"Failed to create shortcut: {e}")
            return False, f"Error: {str(e)}"

    def get_shortcut_target(self, shortcut_path: Path) -> Optional[str]:
        """Get the target path from a shortcut."""
        try:
            shortcut_data = self.read_shortcut(shortcut_path)
            if shortcut_data:
                return shortcut_data.get("target")
            return None
        except Exception as e:
            logger.error(f"Failed to get shortcut target: {e}")
            return None

    def resolve_shortcut(self, shortcut_path: Path) -> Optional[Path]:
        """Resolve shortcut to actual target path."""
        try:
            if not shortcut_path.exists():
                logger.error(f"Shortcut not found: {shortcut_path}")
                return None

            target = self.get_shortcut_target(shortcut_path)
            if target and Path(target).exists():
                return Path(target)

            return None
        except Exception as e:
            logger.error(f"Failed to resolve shortcut: {e}")
            return None

    def batch_set_icon(
        self, shortcut_paths: list, icon_path: Path
    ) -> Tuple[int, int]:
        """Set icon for multiple shortcuts."""
        success_count = 0
        error_count = 0

        for shortcut_path in shortcut_paths:
            success, msg = self.set_shortcut_icon(Path(shortcut_path), icon_path)
            if success:
                success_count += 1
            else:
                error_count += 1
                logger.warning(f"Failed for {shortcut_path}: {msg}")

        logger.info(f"Batch icon set: {success_count} succeeded, {error_count} failed")
        return success_count, error_count

    def is_available(self) -> bool:
        """Check if COM shortcut operations are available."""
        return self._shell is not None
