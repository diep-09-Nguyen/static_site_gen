import os
import shutil


def copytree(source: str, dest: str):
    # if dest exists remove it and make it again
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    ls = os.listdir(source)
    # For each entry (source/entry)
    # attempts to copy to dest
    for entry in ls:
        entry_source = os.path.join(source, entry)
        if not os.path.isfile(entry_source):
            dest_source = os.path.join(dest, entry)
            copytree(entry_source, dest_source)
        else:
            shutil.copy(entry_source, dest)
