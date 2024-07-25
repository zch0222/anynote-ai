from typing import List

from pydantic import BaseModel


class ChatttsToWavDTO(BaseModel):
    texts: List[str]
