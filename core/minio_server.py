from minio import Minio
from core.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET, MINIO_BAST_PATH
from core.logger import get_logger

class MinioServer:

    def __init__(self):
        self.client = Minio(MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY,
                            secret_key=MINIO_SECRET_KEY, secure=False)
        self.bucket = MINIO_BUCKET
        self.base_path = MINIO_BAST_PATH
        self.log = get_logger()

    def upload(self, source_file_path: str, destination_file_path: str) -> str:
        destination = f"{self.base_path}/{destination_file_path}"
        self.client.fput_object(self.bucket, destination, source_file_path)
        # self.log.info(source_file_path, "successfully uploaded as object",
        #     f"{self.base_path}/{destination_file_path}", "to bucket", self.bucket,)
        url = self.client.presigned_get_object(self.bucket, destination)
        return url

