"""
Unit test file.
"""

import shutil
import tempfile
import unittest
from pathlib import Path

from virtual_fs import Vfs


class SimpleUsageTester(unittest.TestCase):
    """Main tester class."""

    def test_simple(self) -> None:
        """Test simple usage of the Vfs class."""
        # Create a temporary directory for testing

        temp_dir = tempfile.mkdtemp()
        try:
            # Create a test file
            test_path = Path(temp_dir)
            info_file = test_path / "info.json"
            info_file.write_text('{"test": "data"}')

            # Use Vfs to interact with the local filesystem
            cwd = Vfs.begin(temp_dir)
            file = cwd / "info.json"
            text = file.read_text()
            self.assertEqual(text, '{"test": "data"}')

            # Write a new file
            out = cwd / "out.json"
            out.write_text(
                text
            )  # Note: fixed from original code which wrote 'out' instead of 'text'

            # List files and verify count
            all_files = cwd.ls()
            self.assertEqual(
                2, len(all_files), f"Expected 2 files, but had {len(all_files)}"
            )
        finally:
            # Clean up
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    unittest.main()
