# virtual-fs

![image](https://github.com/user-attachments/assets/0f9d5dbc-e0e5-4086-9c7a-fc8e08f57943)

Powerful Virtual File abstraction api. Works without `FUSE`. Run in unprivileged docker container. Connects to any backend supported by Rclone. Drop in replacement for pathlib.Path. Works with both local and remote files. If you have an `rclone.conf` file in a default path then this api will allow you access to paths like `remote:Bucket/path/file.txt`.


## ENVS

  * RCLONE_CONFIG
    * path string of the rclone.conf text file

  * RCLONE_CONFIG_JSON
    * string content of rclone config.json
   
## Vs others

  * fsspec - good alternative, but weakly typed.
  * libfuse - this is a mount, virtual-fs is not a mount but an api and therefore can run in docker for unprivileged runtimes.

## Docker Users

This library is built for you. If you are trying to do a `/mount` and having problems because of privileges then this api will give you an escape hatch. Instead of mounting a virtual file system, you use an api in python that will grant you `ls`, `read`, `write` and directory traversal.

To retro fit your code: Swap out `pathlib.Path` for `virtual_fs.FSPath` and apply minor fixes.


```python

from virtual_fs import Vfs

def unit_test():
  config = Path("rclone.config")  # Or use None to get a default.
  cwd = Vfs.begin("remote:bucket/my", config=config)
  do_test(cwd)

def unit_test2():
  with Vfs.begin("mydir") as cwd:  # Closes filesystem when done on cwd.
    do_test(cwd)

def do_test(cwd: FSPath):
    file = cwd / "info.json"
    text = file.read_text()
    out = cwd / "out.json"
    out.write_text(out)
    files, dirs  = cwd.ls()
    print(f"Found {len(files)} files")
    assert 2 == len(files), f"Expected 2 files, but had {len(files)}"
    assert 0 == len(dirs), f"Expected 0 dirs, but had {len(dirs)}"


```



This abstraction is made possible thanks to [rclone](https://rclone.org) and my python api bindings called [rclone-api](https://github.com/zackees/rclone-api).

Easily convert your `pathlib.Path` into an `FSPath`, which will either operate on a local file object, or one on a remote.



```python
class FSPath:
    def __init__(self, fs: FS, path: str) -> None:
        self.fs: FS = fs
        self.path: str = path
        self.fs_holder: FS | None = None

    def set_owner(self) -> None:
        self.fs_holder = self.fs

    def is_real_fs(self) -> bool:
        return isinstance(self.fs, RealFS)
    
    def lspaths(self) -> "tuple[list[FSPath], list[FSPath]]":
        filenames, dirnames = self.ls()
        fpaths: list[FSPath] = [self / name for name in filenames]
        dpaths: list[FSPath] = [self / name for name in dirnames]
        return fpaths, dpaths

    def ls(self) -> tuple[list[str], list[str]]:
        filenames: list[str]
        dirnames: list[str]
        filenames, dirnames = self.fs.ls(self.path)
        return filenames, dirnames

    def mkdir(self, parents=True, exist_ok=True) -> None:
        self.fs.mkdir(self.path, parents=parents, exist_ok=exist_ok)

    def read_text(self) -> str:
        data = self.read_bytes()
        return data.decode("utf-8")

    def read_bytes(self) -> bytes:
        data: bytes | None = None
        try:
            data = self.fs.read_bytes(self.path)
            return data
        except Exception as e:
            raise FileNotFoundError(f"File not found: {self.path}, because of {e}")

    def exists(self) -> bool:
        return self.fs.exists(self.path)

    def __str__(self) -> str:
        return self.path

    def __repr__(self) -> str:
        return f"FSPath({self.path})"

    def __enter__(self) -> "FSPath":
        if self.fs_holder is not None:
            warnings.warn("This operation is reserved for the cwd returned by FS")
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.fs_holder is not None:
            self.fs_holder.dispose()
            self.fs_holder = None



    def write_text(self, data: str, encoding: str | None = None) -> None:
        if encoding is None:
            encoding = "utf-8"
        self.write_bytes(data.encode(encoding))

    def write_bytes(self, data: bytes) -> None:
        self.fs.write_binary(self.path, data)

    def rmtree(self, ignore_errors=False) -> None:
        assert self.exists(), f"Path does not exist: {self.path}"
        # check fs is RealFS
        assert isinstance(self.fs, RealFS)
        shutil.rmtree(self.path, ignore_errors=ignore_errors)



    @property
    def name(self) -> str:
        return Path(self.path).name

    @property
    def parent(self) -> "FSPath":
        parent_path = Path(self.path).parent
        parent_str = parent_path.as_posix()
        return FSPath(self.fs, parent_str)

    def __truediv__(self, other: str) -> "FSPath":
        new_path = Path(self.path) / other
        return FSPath(self.fs, new_path.as_posix())

    # hashable
    def __hash__(self) -> int:
        return hash(f"{repr(self.fs)}:{self.path}")
```
