from helpers.download import download
from helpers.extract import extract


def download_and_extract(src: str, download_dest_path: str, download_dest_name: str, extract_dest: str) -> None:
    download(src, download_dest_path, download_dest_name)
    print("Downloading completed")
    extract(f"{download_dest_path}/{download_dest_name}", extract_dest)
    print("Extraction completed")
