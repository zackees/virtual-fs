# virtual-fs

Powerful Virtual File System abstraction api. Connects to any backrnd supported by Rclone. Drop in replacement for pathlib.Path.

```python

from virtual_fs import Vfs

def do_operation(cwd: FSPath):
    file = cwd / "info.json"
    text = file.read_text()
    out = cwd / "out.json"
    out.write_text(out)
    all_files = cwd.ls()
    print(f"Found {len(all_files)} files")
    assert 2 == len(all_files), f"Excpected 2 files, but had {len(all_files)}"

def unit_test():
  cwd = Vfs.begin("remote:bucket/my", config=None)
  do_operation(cwd)

def unit_test2():
  cwd = Vfs.begin("mydir")
  do_operation(cwd)

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



