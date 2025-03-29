from pathlib import Path
from typing import Union

from rclone_api import Config, FSPath, Mount, RealFS, RemoteFS  # Filesystem utilities
from rclone_api.fs.walk_threaded_walker import FSWalker

RcloneConfig = Union[str, Path, Config, dict, None]


class Vfs:

    @staticmethod
    def begin(src: str | Path, rclone_conf: RcloneConfig = None) -> FSPath:
        """
        Begins a new session with the given path, with operator on this object to ensure proper cleanup.

        Example:
          with Vfs.begin("path/to/dir") as cwd:
              print(cwd.ls())
        """
        vfs: RemoteFS | RealFS
        rclone_conf = rclone_conf or Vfs.find_default_rclone_conf()
        if Vfs.looks_like_remote_path(src):
            vfs = Vfs.create_remote(src=src, rclone_conf=rclone_conf)
            return vfs.cwd()
        else:
            cwd = RealFS().from_path(src)
            return cwd
        raise ValueError("Should not be here.")

    @staticmethod
    def find_default_rclone_conf() -> Path | None:
        from rclone_api.config import find_conf_file

        conf_file: Path | None = find_conf_file(rclone=None)
        if isinstance(conf_file, Exception):
            raise conf_file
        return conf_file

    @staticmethod
    def create_remote(src: str | Path, rclone_conf: RcloneConfig = None) -> RemoteFS:
        sanitized_path = Path(src).as_posix()
        fs: RemoteFS = RemoteFS.from_rclone_config(
            src=sanitized_path, rclone_conf=rclone_conf
        )
        return fs

    @staticmethod
    def mount(
        src: str,
        mount_dst: Path,
        rclone_conf: RcloneConfig = None,
        allow_writes: bool | None = False,
        transfers: int | None = None,  # number of writes to perform in parallel
        use_links: bool | None = None,
        vfs_cache_mode: str | None = None,
        verbose: bool | None = None,
        cache_dir: Path | None = None,
        cache_dir_delete_on_exit: bool | None = None,
        log: Path | None = None,
        other_args: list[str] | None = None,
    ) -> Mount:
        from rclone_api import Rclone

        if isinstance(rclone_conf, str) or isinstance(rclone_conf, dict):
            rclone_conf = Config(text=rclone_conf)
        assert rclone_conf is not None
        mount: Mount = Rclone(rclone_conf).mount(
            src=src,
            outdir=mount_dst,
            allow_writes=allow_writes,
            transfers=transfers,
            use_links=use_links,
            vfs_cache_mode=vfs_cache_mode,
            verbose=verbose,
            cache_dir=cache_dir,
            cache_dir_delete_on_exit=cache_dir_delete_on_exit,
            log=log,
            other_args=other_args,
        )
        return mount

    @staticmethod
    def create_local() -> RealFS:
        fs = RealFS()
        return fs

    @staticmethod
    def looks_like_remote_path(path: str | Path) -> bool:
        import re

        path_str = Path(path).as_posix()
        return ":" in path_str and not re.match(r"^[a-zA-Z]:[/\\]", path_str)

    @staticmethod
    def find_conf_file() -> Path | None:
        from rclone_api.config import find_conf_file

        return find_conf_file()


__all__ = ["FSPath", "RemoteFS", "RealFS", "Vfs", "FSWalker", "Mount"]
