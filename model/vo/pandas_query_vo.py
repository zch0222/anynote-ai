from pydantic import BaseModel


class PandasQueryVO(BaseModel):
    message: str

    def to_dict(self):
        return {
            "message": self.message
        }
