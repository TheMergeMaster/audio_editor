import requests
import os


def download(src: str, dest_path: str, file_name: str):
    os.makedirs(dest_path)

    res = requests.get(src, stream=True)
    with open(f"{dest_path}/{file_name}", "wb") as file:
        for chunk in res.iter_content(chunk_size=8192):
            file.write(chunk)
