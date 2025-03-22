# virtual-fs

Powerful Virtual File System abstraction. Drop in replacement for pathlib.Path.

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
