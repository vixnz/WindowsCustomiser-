"""Tests for icon manager."""

import unittest
from pathlib import Path
from src.core import IconManager, IconInfo


class TestIconManager(unittest.TestCase):
    """Test cases for IconManager."""

    def setUp(self):
        """Set up test fixtures."""
        self.icon_manager = IconManager()

    def test_supported_formats(self):
        """Test supported icon formats."""
        supported = self.icon_manager.SUPPORTED_FORMATS
        self.assertIn(".ico", supported)
        self.assertIn(".cur", supported)
        self.assertIn(".png", supported)

    def test_max_icon_size(self):
        """Test maximum icon size."""
        max_size = self.icon_manager.MAX_ICON_SIZE
        self.assertEqual(max_size, 50 * 1024 * 1024)

    def test_validate_icon_nonexistent_file(self):
        """Test validation of nonexistent icon."""
        result, message = self.icon_manager.validate_icon(Path("nonexistent.ico"))
        self.assertFalse(result)
        self.assertIn("does not exist", message)

    def test_get_icon_info_nonexistent_file(self):
        """Test get info for nonexistent icon."""
        result = self.icon_manager.get_icon_info(Path("nonexistent.ico"))
        self.assertIsNone(result)

    def test_search_icons_nonexistent_directory(self):
        """Test search in nonexistent directory."""
        result = self.icon_manager.search_icons(Path("nonexistent_dir"))
        self.assertEqual(result, [])


class TestIconInfo(unittest.TestCase):
    """Test cases for IconInfo dataclass."""

    def test_icon_info_creation(self):
        """Test IconInfo creation."""
        info = IconInfo(
            path=Path("test.ico"),
            name="test",
            size=1024,
            width=64,
            height=64,
            format="ico",
        )

        self.assertEqual(info.name, "test")
        self.assertEqual(info.size, 1024)
        self.assertEqual(info.width, 64)
        self.assertEqual(info.height, 64)

    def test_icon_info_to_dict(self):
        """Test IconInfo to_dict conversion."""
        info = IconInfo(
            path=Path("test.ico"),
            name="test",
            size=1024,
        )

        data = info.to_dict()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "test")
        self.assertEqual(data["size"], 1024)


if __name__ == "__main__":
    unittest.main()
