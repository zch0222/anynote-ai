from typing import List
from pydantic import BaseModel
from model.bo import ChatMessageBO

class ChatDTO(BaseModel):
    model: str
    messages: List[ChatMessageBO]