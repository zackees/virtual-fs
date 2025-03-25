"""
Main entry point for the VFS command line tool.
"""

import argparse
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional


@dataclass
class MountArgs:
    """Mount command arguments."""

    src: str
    mount_dst: Path

    def __post_init__(self):
        """Post initialization validation."""
        assert isinstance(self.src, str), f"Expected str, but got {type(self.src)}"
        assert isinstance(
            self.mount_dst, Path
        ), f"Expected Path, but got {type(self.mount_dst)}"


@dataclass
class LsArgs:
    """List command arguments."""

    path: str

    def __post_init__(self):
        """Post initialization validation."""
        assert isinstance(self.path, str), f"Expected str, but got {type(self.path)}"


@dataclass
class Args:
    """Command line arguments container."""

    command: Literal["mount", "ls"]
    mount_args: Optional[MountArgs] = None
    ls_args: Optional[LsArgs] = None

    def __post_init__(self):
        """Validate that the appropriate args are set based on command."""
        if self.command == "mount":
            assert (
                self.mount_args is not None
            ), "mount_args must be set for mount command"
        elif self.command == "ls":
            assert self.ls_args is not None, "ls_args must be set for ls command"


def parse_args() -> Args:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Virtual File System (VFS) tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Mount command
    mount_parser = subparsers.add_parser("mount", help="Mount a remote filesystem")
    mount_parser.add_argument("src", help="The source path to mount")
    mount_parser.add_argument("mount_dst", help="The destination path to mount to")

    # List command
    ls_parser = subparsers.add_parser("ls", help="List contents of a path")
    ls_parser.add_argument("path", help="The path to list contents of")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "mount":
        return Args(
            command="mount",
            mount_args=MountArgs(src=args.src, mount_dst=Path(args.mount_dst)),
        )
    elif args.command == "ls":
        return Args(command="ls", ls_args=LsArgs(path=args.path))

    # This should never happen due to the sys.exit(1) above
    raise ValueError(f"Unknown command: {args.command}")


def mount_command(args: MountArgs) -> int:
    """Execute the mount command."""
    from virtual_fs import Vfs

    print(f"Mounting {args.src} to {args.mount_dst}")
    with Vfs.mount(src=args.src, mount_dst=args.mount_dst):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting...")
    return 0


def ls_command(args: LsArgs) -> int:
    """Execute the ls command."""
    from virtual_fs import Vfs

    print(f"Listing contents of {args.path}")
    with Vfs.begin(args.path) as cwd:
        files, dirs = cwd.ls()
        # print(f"Files: {files}")
        # print(f"Dirs: {dirs}")
        if dirs:
            print(f"Directories ({len(dirs)}):")
            for d in dirs:
                print(f"  {d}")
        if files:
            print(f"Files ({len(files)}):")
            for f in files:
                print(f"  {f}")
    return 0


def main() -> int:
    """Main entry point for the VFS tool."""
    args = parse_args()

    if args.command == "mount":
        assert args.mount_args is not None  # This helps the type checker
        return mount_command(args.mount_args)
    elif args.command == "ls":
        assert args.ls_args is not None  # This helps the type checker
        return ls_command(args.ls_args)

    return 1


if __name__ == "__main__":
    sys.argv.append("ls")
    sys.argv.append("dst:TorrentBooks")
    sys.exit(main())
