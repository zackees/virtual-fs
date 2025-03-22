from pathlib import Path
from typing import Union

from rclone_api import Config, FSPath, RealFS, RemoteFS  # Filesystem utilities

RcloneConfig = Union[str, Path, Config, None]


class Vfs:

    @staticmethod
    def begin(src: str | Path, rclone_conf: RcloneConfig = None) -> FSPath:
        """Begins a new session with the given path."""
        vfs: RemoteFS | RealFS
        if Vfs.looks_like_remote_path(src):
            vfs = Vfs.create_remote(src=src, rclone_conf=rclone_conf)
        else:
            vfs = Vfs.create_local(src=src)
        return vfs.cwd()

    @staticmethod
    def create_remote(src: str | Path, rclone_conf: RcloneConfig = None) -> RemoteFS:
        sanitized_path = Path(src).as_posix()
        fs: RemoteFS = RemoteFS.from_rclone_config(
            src=sanitized_path, rclone_conf=rclone_conf
        )
        return fs

    @staticmethod
    def create_local(src: str | Path) -> RemoteFS:
        fs = RealFS.from_path(src=src)
        return fs

    @staticmethod
    def looks_like_remote_path(path: str | Path) -> bool:
        import re

        path_str = Path(path).as_posix()
        return ":" in path_str and not re.match(r"^[a-zA-Z]:[/\\]", path_str)


__all__ = ["begin", "FSPath", "RemoteFS"]
