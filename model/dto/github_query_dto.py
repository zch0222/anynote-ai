from pydantic import BaseModel


class GithubQueryDTO(BaseModel):
    owner: str
    repo: str
    branch: str
    prompt: str
