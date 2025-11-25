"""Permission elevation and UAC handling."""

import logging
import ctypes
import os
import sys
import subprocess
from pathlib import Path
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class PermissionManager:
    """Manages permission elevation and privilege checks."""

    def __init__(self):
        """Initialize permission manager."""
        self.is_admin = self._check_admin_status()
        self.requires_elevation_paths = [
            Path("C:/Windows"),
            Path("C:/Program Files"),
            Path("C:/Program Files (x86)"),
        ]

    def _check_admin_status(self) -> bool:
        """Check if running with admin privileges."""
        try:
            return ctypes.windll.shell.IsUserAnAdmin() != 0
        except Exception as e:
            logger.error(f"Failed to check admin status: {e}")
            return False

    def is_admin_required(self, target_path: Path) -> bool:
        """Check if admin privileges are required for target."""
        try:
            target_path = Path(target_path).resolve()

            # Check if target is in system protected locations
            for protected_path in self.requires_elevation_paths:
                try:
                    target_path.relative_to(protected_path)
                    return True
                except ValueError:
                    continue

            # Try to write to target directory
            if target_path.is_dir():
                test_file = target_path / ".admin_check.tmp"
                try:
                    test_file.write_text("test")
                    test_file.unlink()
                    return False
                except PermissionError:
                    return True
                except Exception:
                    return False

            return False
        except Exception as e:
            logger.warning(f"Could not determine if admin required: {e}")
            return False

    def request_elevation(self, reason: str = "") -> bool:
        """Request UAC elevation to run as admin."""
        if self.is_admin:
            logger.info("Already running as admin")
            return True

        try:
            logger.info(f"Requesting UAC elevation: {reason}")

            # Build command to re-run current script with admin privileges
            script_path = sys.argv[0]
            args = " ".join(sys.argv[1:])

            # Run as admin using runas
            cmd = f'python "{script_path}" {args}'

            ctypes.windll.shell.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}" {args}', None, 1)

            # Current process should exit
            sys.exit(0)
        except Exception as e:
            logger.error(f"Failed to request elevation: {e}")
            return False

    def check_file_permissions(self, file_path: Path) -> Tuple[bool, str]:
        """Check if current process can modify file."""
        try:
            file_path = Path(file_path)

            if not file_path.exists():
                return False, "File does not exist"

            # Try to get file metadata
            file_path.stat()

            # For files, check if we can read and potentially write
            if file_path.is_file():
                # Try reading
                with open(file_path, "rb"):
                    pass

                # Try writing (without actually modifying)
                if file_path.stat().st_size > 0:
                    # File has content, try to create a backup
                    backup_path = file_path.with_suffix(file_path.suffix + ".perm_check")
                    try:
                        import shutil

                        shutil.copy2(file_path, backup_path)
                        backup_path.unlink()
                        return True, "Full read/write access"
                    except PermissionError:
                        return False, "Write permission denied"

            return True, "File accessible"

        except PermissionError:
            return False, "Permission denied"
        except Exception as e:
            return False, f"Error checking permissions: {str(e)}"

    def check_registry_permissions(self, hive: str, path: str) -> Tuple[bool, str]:
        """Check if current process can modify registry."""
        try:
            import winreg

            hives = {
                "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
                "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
            }

            hive_handle = hives.get(hive)
            if not hive_handle:
                return False, f"Unknown hive: {hive}"

            # Try to open key for writing
            try:
                key = winreg.OpenKey(hive_handle, path, 0, winreg.KEY_WRITE)
                winreg.CloseKey(key)
                return True, "Registry write access available"
            except FileNotFoundError:
                return True, "Registry path not found (but writable)"
            except PermissionError:
                return False, "Registry write permission denied"

        except Exception as e:
            return False, f"Error checking registry permissions: {str(e)}"

    def validate_operation_permissions(
        self, operation_type: str, target: Path
    ) -> Tuple[bool, str, bool]:
        """
        Validate if operation can proceed.

        Returns: (can_proceed, message, needs_elevation)
        """
        try:
            if operation_type == "replace_folder_icon":
                # Check folder access
                if not target.exists():
                    return False, "Target folder not found", False

                can_write, msg = self.check_file_permissions(target / "test.tmp")
                if not can_write:
                    needs_elev = self.is_admin_required(target)
                    return False, msg, needs_elev

                return True, "Permission check passed", False

            elif operation_type == "replace_file_type_icon":
                # Check registry access
                registry_path = rf"Software\Classes"
                can_write, msg = self.check_registry_permissions("HKEY_CURRENT_USER", registry_path)

                if not can_write:
                    return False, msg, not self.is_admin

                return True, "Permission check passed", False

            else:
                return True, "Operation type not restricted", False

        except Exception as e:
            logger.error(f"Permission validation failed: {e}")
            return False, f"Validation error: {str(e)}", False

    def prompt_for_elevation(self, reason: str) -> bool:
        """Prompt user for elevation with explanation."""
        logger.warning(f"Elevation required: {reason}")

        # In GUI context, this should be a dialog box
        # For CLI, just request elevation
        try:
            from PyQt5.QtWidgets import QMessageBox

            reply = QMessageBox.question(
                None,
                "Administrator Privileges Required",
                f"{reason}\n\nWould you like to restart with administrator privileges?",
                QMessageBox.Yes | QMessageBox.No,
            )

            return reply == QMessageBox.Yes
        except ImportError:
            # No GUI available, just request elevation
            return True

    def get_privilege_level(self) -> str:
        """Get current privilege level description."""
        return "Administrator" if self.is_admin else "User"

    def get_required_privileges_info(self) -> str:
        """Get info about required privileges."""
        return (
            "Administrator privileges are required for:\n"
            "- Changing system folder icons\n"
            "- Modifying file type icons\n"
            "- Registry modifications\n"
            "- System-wide icon cache operations\n\n"
            "Standard user operations:\n"
            "- User folder icons\n"
            "- Desktop/Personal documents\n"
            "- User-owned shortcuts"
        )
