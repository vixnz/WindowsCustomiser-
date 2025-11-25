"""Integration tests for full workflows."""

import unittest
import tempfile
import shutil
from pathlib import Path
from src.core import (
    IconManager,
    BackupManager,
    TransactionalIconReplacer,
    BatchProcessor,
    BatchOperation,
    BatchOperationType,
)
from src.utils import PermissionManager


class TestIconReplacementWorkflow(unittest.TestCase):
    """Test complete icon replacement workflows."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.backup_manager = BackupManager(self.temp_dir / "backups")
        self.replacer = TransactionalIconReplacer(self.backup_manager)
        self.icon_manager = IconManager()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_folder_icon_replacement(self):
        """Test replacing folder icon."""
        # Create test folder
        test_folder = self.temp_dir / "test_folder"
        test_folder.mkdir()

        # Create test icon
        test_icon = self.temp_dir / "test.ico"
        test_icon.write_bytes(b"\x00\x00\x01\x00")  # Minimal ICO header

        # Replace icon
        success, msg, op = self.replacer.replace_folder_icon(test_folder, test_icon)
        self.assertTrue(success)
        self.assertIsNotNone(op)

    def test_transaction_rollback(self):
        """Test transaction rollback."""
        test_folder = self.temp_dir / "test_folder"
        test_folder.mkdir()

        test_icon = self.temp_dir / "test.ico"
        test_icon.write_bytes(b"\x00\x00\x01\x00")

        # Replace icon
        success, msg, op = self.replacer.replace_folder_icon(test_folder, test_icon)
        self.assertTrue(success)
        self.assertEqual(self.replacer.get_operation_count(), 1)

        # Rollback
        success, msg = self.replacer.rollback_last_operation()
        self.assertTrue(success)
        self.assertEqual(self.replacer.get_operation_count(), 0)

    def test_batch_folder_icons(self):
        """Test batch folder icon replacement."""
        # Create multiple folders
        folders = []
        for i in range(3):
            folder = self.temp_dir / f"folder_{i}"
            folder.mkdir()
            folders.append(folder)

        # Create test icon
        test_icon = self.temp_dir / "test.ico"
        test_icon.write_bytes(b"\x00\x00\x01\x00")

        # Replace icons one by one
        for folder in folders:
            success, msg, op = self.replacer.replace_folder_icon(folder, test_icon)
            self.assertTrue(success)

        self.assertEqual(self.replacer.get_operation_count(), 3)

    def test_backup_after_replacement(self):
        """Test backup creation after replacement."""
        test_folder = self.temp_dir / "test_folder"
        test_folder.mkdir()

        test_icon = self.temp_dir / "test.ico"
        test_icon.write_bytes(b"\x00\x00\x01\x00")

        # Replace icon
        success, msg, op = self.replacer.replace_folder_icon(test_folder, test_icon)
        self.assertTrue(success)

        # Commit should create backup
        success, msg = self.replacer.commit_operations()
        self.assertTrue(success)


class TestBatchOperations(unittest.TestCase):
    """Test batch operation processing."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.processor = BatchProcessor()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_batch_operation_creation(self):
        """Test creating batch operation."""
        files = [self.temp_dir / f"file_{i}.ico" for i in range(5)]
        for f in files:
            f.write_bytes(b"\x00\x00\x01\x00")

        operation = BatchOperation(
            operation_type=BatchOperationType.BACKUP_ITEMS,
            source_items=files,
        )

        self.assertEqual(operation.operation_type, BatchOperationType.BACKUP_ITEMS)
        self.assertEqual(len(operation.source_items), 5)

    def test_batch_processing_progress(self):
        """Test batch processing with progress callback."""
        progress_updates = []

        def progress_cb(current, total):
            progress_updates.append((current, total))

        self.processor.set_progress_callback(progress_cb)

        files = [self.temp_dir / f"file_{i}.ico" for i in range(3)]
        for f in files:
            f.write_bytes(b"\x00\x00\x01\x00")

        operation = BatchOperation(
            operation_type=BatchOperationType.BACKUP_ITEMS,
            source_items=files,
        )

        result = self.processor.process_batch(operation)

        self.assertEqual(result.total_items, 3)
        self.assertGreater(len(progress_updates), 0)

    def test_batch_error_handling(self):
        """Test batch processing with errors."""
        error_log = []

        def error_cb(path, msg):
            error_log.append((path, msg))

        self.processor.set_error_callback(error_cb)

        # Mix valid and invalid files
        files = [
            self.temp_dir / "valid.ico",
            self.temp_dir / "invalid.ico",
        ]
        files[0].write_bytes(b"\x00\x00\x01\x00")
        # files[1] not created (invalid)

        operation = BatchOperation(
            operation_type=BatchOperationType.BACKUP_ITEMS,
            source_items=files,
        )

        result = self.processor.process_batch(operation)

        self.assertEqual(result.total_items, 2)
        # At least one item should have failed or been skipped
        self.assertTrue(result.failed_items > 0 or result.skipped_items > 0)


class TestPermissionManagement(unittest.TestCase):
    """Test permission and elevation handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.perm_manager = PermissionManager()
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_admin_status_check(self):
        """Test admin status detection."""
        is_admin = self.perm_manager.is_admin
        self.assertIsInstance(is_admin, bool)

    def test_file_permission_check(self):
        """Test file permission checking."""
        test_file = self.temp_dir / "test.txt"
        test_file.write_text("test")

        can_access, msg = self.perm_manager.check_file_permissions(test_file)
        self.assertTrue(can_access)

    def test_nonexistent_file_permission_check(self):
        """Test permission check for nonexistent file."""
        test_file = self.temp_dir / "nonexistent.txt"

        can_access, msg = self.perm_manager.check_file_permissions(test_file)
        self.assertFalse(can_access)

    def test_privilege_level_info(self):
        """Test privilege level information."""
        info = self.perm_manager.get_required_privileges_info()
        self.assertIsInstance(info, str)
        self.assertIn("Administrator", info)

    def test_operation_permission_validation(self):
        """Test operation permission validation."""
        test_folder = self.temp_dir / "test_folder"
        test_folder.mkdir()

        can_proceed, msg, needs_elev = self.perm_manager.validate_operation_permissions(
            "replace_folder_icon", test_folder
        )

        self.assertIsInstance(can_proceed, bool)
        self.assertIsInstance(needs_elev, bool)


class TestCompleteWorkflow(unittest.TestCase):
    """Test complete end-to-end workflow."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.backup_manager = BackupManager(self.temp_dir / "backups")
        self.replacer = TransactionalIconReplacer(self.backup_manager)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_full_workflow(self):
        """Test complete workflow: create, replace, backup, rollback."""
        # Create test environment
        test_folder = self.temp_dir / "test_folder"
        test_folder.mkdir()

        test_icon = self.temp_dir / "test.ico"
        test_icon.write_bytes(b"\x00\x00\x01\x00")

        # Replace folder icon
        success, msg, op = self.replacer.replace_folder_icon(test_folder, test_icon)
        self.assertTrue(success)

        # Verify operation recorded
        self.assertEqual(self.replacer.get_operation_count(), 1)

        # Commit changes
        success, msg = self.replacer.commit_operations()
        self.assertTrue(success)

        # Verify operation cleared after commit
        self.assertEqual(self.replacer.get_operation_count(), 0)

        # Verify backup was created
        backups = self.backup_manager.list_backups()
        self.assertGreater(len(backups), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
