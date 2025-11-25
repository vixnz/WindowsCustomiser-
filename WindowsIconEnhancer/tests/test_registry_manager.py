"""Tests for registry manager."""

import unittest
from src.core import RegistryManager


class TestRegistryManager(unittest.TestCase):
    """Test cases for RegistryManager."""

    def setUp(self):
        """Set up test fixtures."""
        self.registry_manager = RegistryManager()

    def test_registry_manager_initialization(self):
        """Test registry manager initialization."""
        self.assertIsNotNone(self.registry_manager)

    def test_hives_available(self):
        """Test that registry hives are available."""
        hives = self.registry_manager.HIVES
        self.assertIn("HKEY_CURRENT_USER", hives)
        self.assertIn("HKEY_LOCAL_MACHINE", hives)

    def test_get_nonexistent_value(self):
        """Test getting nonexistent registry value."""
        result = self.registry_manager.get_value(
            "HKEY_CURRENT_USER",
            r"Software\NonExistent\Path",
            "NonExistentValue",
            default="default",
        )
        self.assertEqual(result, "default")

    def test_validate_registry_path(self):
        """Test registry path validation."""
        # Valid path
        result = self.registry_manager.validate_registry_path(
            "HKEY_CURRENT_USER", r"Software\Microsoft"
        )
        self.assertIsInstance(result, bool)

    def test_file_type_icon_paths(self):
        """Test file type icon registry paths."""
        paths = self.registry_manager.FILE_TYPE_ICON_PATHS
        self.assertIn(".txt", paths)
        self.assertIn(".pdf", paths)


if __name__ == "__main__":
    unittest.main()
