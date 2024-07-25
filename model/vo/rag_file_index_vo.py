from pydantic import BaseModel


class RagFileIndexVO(BaseModel):
    hash: str

    def to_dict(self):
        return {
            "hash": self.hash
        }
