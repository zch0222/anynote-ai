from pydantic import BaseModel


class RagQueryVO(BaseModel):
    message: str

    def to_dict(self):
        return {
            "message": self.message
        }
