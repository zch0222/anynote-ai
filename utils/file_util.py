import requests
import hashlib
import os
import uuid
from model.dto import FileDownloadDTO
from urllib.parse import urlparse, urlunparse

def remove_query_params(url):
    parsed_url = urlparse(url)
    # Remove the query by setting the query component to an empty string
    url_without_query = parsed_url._replace(query="")
    # Reconstruct the URL without query parameters
    cleaned_url = urlunparse(url_without_query)
    return cleaned_url


def download_file(url: str, dest_folder: str) -> FileDownloadDTO | None:
    try:
        # 确保目标文件夹存在
        os.makedirs(dest_folder, exist_ok=True)


        cleaned_url = remove_query_params(url)
        print(cleaned_url)
        # 从URL中提取文件名
        file_name = f"{uuid.uuid4()}.{cleaned_url.split('.')[-1]}"
        file_path = os.path.join(dest_folder, file_name)

        # 下载文件
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # 计算SHA-256哈希值
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        hash_value = sha256_hash.hexdigest()

        return FileDownloadDTO(file_path=file_path, hash_value=hash_value)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
