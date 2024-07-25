from pydantic import BaseModel


class GithubQueryVO(BaseModel):
    message: str

    def to_dict(self):
        return {
            "message": self.message
        }