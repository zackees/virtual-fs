"""
Main entry point.
"""

import argparse
import sys
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Args:
    """Command line arguments."""

    src: str
    mount_dst: Path

    def __post_init__(self):
        """Post initialization validation."""
        assert isinstance(self.src, str), f"Expected str, but got {type(self.src)}"
        assert isinstance(
            self.mount_dst, Path
        ), f"Expected Path, but got {type(self.mount_dst)}"


def parse_args() -> Args:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Mount a remote filesystem.")
    parser.add_argument("src", help="The source path to mount.")
    parser.add_argument("mount_dst", help="The destination path to mount to.")
    args = parser.parse_args()
    return Args(src=args.src, mount_dst=Path(args.mount_dst))


def main() -> int:
    """Main entry point for the template_python_cmd package."""
    from virtual_fs import Vfs

    args = parse_args()
    print(f"Mounting {args.src} to {args.mount_dst}")
    with Vfs.mount(src=args.src, mount_dst=args.mount_dst):
        try:
            while True:

                time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
