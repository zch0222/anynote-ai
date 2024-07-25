from pydantic import BaseModel


class PandasQueryDTO(BaseModel):
    url: str
    prompt: str
