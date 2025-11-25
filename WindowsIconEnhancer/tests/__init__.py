"""Test suite initialization."""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import all test modules
from tests.test_icon_manager import *  # noqa
from tests.test_backup_manager import *  # noqa
from tests.test_registry_manager import *  # noqa


def run_tests():
    """Run all tests."""
    unittest.main(module=None, exit=True, verbosity=2)


if __name__ == "__main__":
    run_tests()
