from pydantic import BaseModel


class GithubIndexDTO(BaseModel):
    owner: str
    repo: str
    branch: str
