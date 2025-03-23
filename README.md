# virtual-fs

Powerful Virtual File abstraction api. Connects to any backend supported by Rclone. Drop in replacement for pathlib.Path. Works with both local and remote files. If you have an `rclone.conf` file in a default path then you can this api will allow you access paths like `remote:Bucket/path/file.txt`.

## Docker Users

This library is built for you. If you are trying to do a `/mount` and having problems because of privileges then this api will give you an escape hatch. Instead mounting a virtual file system, you use an api in python that will grant you `ls`, `read`, `write` and directory traversal.

To retro fit your code: Swap out `pathlib.Path` for `virtual_fs.FSPath` and apply minor fixes.


```python

from virtual_fs import Vfs

def unit_test():
  config = Path("rclone.config")  # Or use None to get a default.
  with Vfs.begin("remote:bucket/my", config=config) as cwd:
    do_test(cwd)

def unit_test2():
  with Vfs.begin("mydir") as cwd:
    do_test(cwd)

def do_test(cwd: FSPath):
    file = cwd / "info.json"
    text = file.read_text()
    out = cwd / "out.json"
    out.write_text(out)
    all_files = cwd.ls()
    print(f"Found {len(all_files)} files")
    assert 2 == len(all_files), f"Expected 2 files, but had {len(all_files)}"


```

![image](https://github.com/user-attachments/assets/0f9d5dbc-e0e5-4086-9c7a-fc8e08f57943)


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



