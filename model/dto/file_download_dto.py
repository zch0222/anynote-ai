from pydantic import BaseModel


class FileDownloadDTO(BaseModel):
    file_path: str
    hash_value: str
