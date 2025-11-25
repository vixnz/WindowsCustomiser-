"""Tests for backup manager."""

import unittest
from pathlib import Path
import tempfile
import shutil
from src.core import BackupManager, BackupInfo


class TestBackupManager(unittest.TestCase):
    """Test cases for BackupManager."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.backup_manager = BackupManager(Path(self.temp_dir))

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_backup_manager_initialization(self):
        """Test backup manager initialization."""
        self.assertTrue(self.backup_manager.backup_dir.exists())

    def test_create_backup(self):
        """Test creating a backup."""
        test_file = Path(self.temp_dir) / "test_file.txt"
        test_file.write_text("test content")

        backup_id = self.backup_manager.create_backup([test_file], "Test Backup")
        self.assertIsNotNone(backup_id)

    def test_list_backups(self):
        """Test listing backups."""
        test_file = Path(self.temp_dir) / "test_file.txt"
        test_file.write_text("test content")

        self.backup_manager.create_backup([test_file], "Backup 1")
        self.backup_manager.create_backup([test_file], "Backup 2")

        backups = self.backup_manager.list_backups()
        self.assertEqual(len(backups), 2)

    def test_delete_backup(self):
        """Test deleting a backup."""
        test_file = Path(self.temp_dir) / "test_file.txt"
        test_file.write_text("test content")

        backup_id = self.backup_manager.create_backup([test_file], "Test Backup")
        self.assertTrue(self.backup_manager.delete_backup(backup_id))

        backups = self.backup_manager.list_backups()
        self.assertEqual(len(backups), 0)

    def test_cleanup_old_backups(self):
        """Test cleaning up old backups."""
        test_file = Path(self.temp_dir) / "test_file.txt"
        test_file.write_text("test content")

        # Create multiple backups
        for i in range(15):
            self.backup_manager.create_backup([test_file], f"Backup {i}")

        # Cleanup to keep only 5
        cleaned = self.backup_manager.cleanup_old_backups(max_backups=5)
        self.assertGreater(cleaned, 0)


class TestBackupInfo(unittest.TestCase):
    """Test cases for BackupInfo dataclass."""

    def test_backup_info_creation(self):
        """Test BackupInfo creation."""
        info = BackupInfo(
            backup_id="123",
            name="Test",
            created_date="2025-01-01",
            description="Test backup",
            file_count=10,
            size_bytes=1024,
        )

        self.assertEqual(info.backup_id, "123")
        self.assertEqual(info.name, "Test")
        self.assertEqual(info.file_count, 10)

    def test_backup_info_to_dict(self):
        """Test BackupInfo to_dict conversion."""
        info = BackupInfo(
            backup_id="123",
            name="Test",
            created_date="2025-01-01",
            description="Test backup",
            file_count=10,
            size_bytes=1024,
        )

        data = info.to_dict()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["backup_id"], "123")


if __name__ == "__main__":
    unittest.main()
