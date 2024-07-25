from pydantic import BaseModel


class WhisperRunDTO(BaseModel):
    # 链接
    url: str
    # 语言
    language: str
