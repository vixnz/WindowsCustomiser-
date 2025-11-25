"""Backup and restore functionality."""

import shutil
import json
import logging
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime
from dataclasses import dataclass, asdict
import uuid

logger = logging.getLogger(__name__)


@dataclass
class BackupInfo:
    """Information about a backup."""

    backup_id: str
    name: str
    created_date: str
    description: str
    file_count: int
    size_bytes: int
    version: str = "1.0"

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


class BackupManager:
    """Manages backups and restores."""

    BACKUP_METADATA_FILE = "backup_metadata.json"
    BACKUP_VERSION = "1.0"

    def __init__(self, backup_dir: Path):
        """Initialize backup manager."""
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.backup_dir / self.BACKUP_METADATA_FILE

    def create_backup(
        self,
        files_to_backup: List[Path],
        name: str = "",
        description: str = "",
    ) -> Optional[str]:
        """Create a new backup."""
        try:
            backup_id = str(uuid.uuid4())
            if not name:
                name = f"Backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            backup_path = self.backup_dir / backup_id
            backup_path.mkdir(parents=True, exist_ok=True)

            # Copy files
            file_count = 0
            for file_path in files_to_backup:
                if file_path.exists():
                    relative_path = file_path.relative_to(file_path.anchor)
                    target_path = backup_path / relative_path

                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    if file_path.is_file():
                        shutil.copy2(file_path, target_path)
                        file_count += 1
                    elif file_path.is_dir():
                        shutil.copytree(file_path, target_path, dirs_exist_ok=True)
                        file_count += 1

            # Calculate size
            size_bytes = self._get_directory_size(backup_path)

            # Create backup info
            backup_info = BackupInfo(
                backup_id=backup_id,
                name=name,
                created_date=datetime.now().isoformat(),
                description=description,
                file_count=file_count,
                size_bytes=size_bytes,
            )

            # Save metadata
            self._save_backup_metadata(backup_info)

            logger.info(f"Backup created: {backup_id} - {name}")
            return backup_id

        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None

    def restore_backup(self, backup_id: str, target_dir: Path = None) -> bool:
        """Restore a backup."""
        try:
            backup_path = self.backup_dir / backup_id
            if not backup_path.exists():
                logger.error(f"Backup not found: {backup_id}")
                return False

            if target_dir is None:
                target_dir = Path(backup_path.anchor)

            # Copy files back
            for file_path in backup_path.rglob("*"):
                if file_path.is_file():
                    relative_path = file_path.relative_to(backup_path)
                    target_path = target_dir / relative_path

                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, target_path)

            logger.info(f"Backup restored: {backup_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to restore backup: {e}")
            return False

    def delete_backup(self, backup_id: str) -> bool:
        """Delete a backup."""
        try:
            backup_path = self.backup_dir / backup_id
            if backup_path.exists():
                shutil.rmtree(backup_path)
                self._remove_backup_metadata(backup_id)
                logger.info(f"Backup deleted: {backup_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete backup: {e}")
            return False

    def list_backups(self) -> List[BackupInfo]:
        """List all available backups."""
        try:
            backups = []
            metadata = self._load_all_metadata()

            for backup_info in metadata:
                backups.append(BackupInfo(**backup_info))

            return sorted(backups, key=lambda x: x.created_date, reverse=True)
        except Exception as e:
            logger.error(f"Failed to list backups: {e}")
            return []

    def get_backup_info(self, backup_id: str) -> Optional[BackupInfo]:
        """Get information about a specific backup."""
        try:
            metadata = self._load_all_metadata()
            for backup_info in metadata:
                if backup_info["backup_id"] == backup_id:
                    return BackupInfo(**backup_info)
            return None
        except Exception as e:
            logger.error(f"Failed to get backup info: {e}")
            return None

    def cleanup_old_backups(self, max_backups: int = 10) -> int:
        """Remove old backups to keep only the latest."""
        try:
            backups = self.list_backups()
            deleted_count = 0

            for backup in backups[max_backups:]:
                if self.delete_backup(backup.backup_id):
                    deleted_count += 1

            logger.info(f"Cleaned up {deleted_count} old backups")
            return deleted_count
        except Exception as e:
            logger.error(f"Failed to cleanup backups: {e}")
            return 0

    def _save_backup_metadata(self, backup_info: BackupInfo) -> bool:
        """Save backup metadata."""
        try:
            metadata = self._load_all_metadata()
            metadata.append(backup_info.to_dict())

            with open(self.metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)

            return True
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
            return False

    def _load_all_metadata(self) -> List[dict]:
        """Load all backup metadata."""
        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, "r") as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Failed to load metadata: {e}")
            return []

    def _remove_backup_metadata(self, backup_id: str) -> bool:
        """Remove backup metadata."""
        try:
            metadata = self._load_all_metadata()
            metadata = [m for m in metadata if m["backup_id"] != backup_id]

            with open(self.metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)

            return True
        except Exception as e:
            logger.error(f"Failed to remove metadata: {e}")
            return False

    def _get_directory_size(self, directory: Path) -> int:
        """Get total size of directory."""
        total = 0
        try:
            for path in directory.rglob("*"):
                if path.is_file():
                    total += path.stat().st_size
        except Exception as e:
            logger.error(f"Failed to calculate size: {e}")
        return total
