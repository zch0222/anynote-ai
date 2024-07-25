from pydantic import BaseModel


class RagFileIndexDTO(BaseModel):
    file_path: str
