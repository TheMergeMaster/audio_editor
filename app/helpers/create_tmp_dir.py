from os import path, makedirs
from shutil import rmtree


def create_tmp_dir(dest_path: str):
    if path.exists(dest_path):
        # Need to delete the temporary files as they can grow big in size
        rmtree(dest_path)
    makedirs(dest_path)
