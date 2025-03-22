# virtual-fs

Powerful Virtual File System abstraction api. Drop in replacement for pathlib.Path.

![image](https://github.com/user-attachments/assets/f72d8c45-3ad0-4378-98f5-77b1fd0da88d)

This abstraction is made possible thanks to [rclone](https://rclone.org) and my python api bindings called [rclone-api](https://github.com/zackees/rclone-api).

Easily convert your pathlib.Path into a FSPath, which can either be the remote fileobject, or a local one, under the hood

  * Operations supported
    * ls
    * cwd
    * read
    * write
    * exists
    * is file
    * is dir
    * parent
    * /


# Example

```python

from virtual_fs import Vfs

def unit_test():
    cwd = Vfs.begin("remote:bucket/my", config=None)
    file = cwd / "info.json"
    text = file.read_text()
    out = cwd / "out.json"
    out.write_text(out)
    all_files = cwd.ls()
    print(f"Found {len(all_files)} files")
    assert 2 == len(all_files), f"Excpected 2 files, but had {len(all_files)}"

```
