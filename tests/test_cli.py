"""
Unit test file.
"""

import os
import unittest

COMMAND = "virtual-vfs-mount --help"


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_help(self) -> None:
        """Test command line interface (CLI)."""
        rtn = os.system(COMMAND)
        self.assertEqual(0, rtn)


if __name__ == "__main__":
    unittest.main()
