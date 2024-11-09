from pyunpack import Archive


def extract(src: str, dest: str):
    Archive(src).extractall(dest)
