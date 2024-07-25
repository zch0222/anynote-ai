from pydantic import BaseModel

class ChatMessageBO(BaseModel):
    role: str
    content: str

    def to_dict(self):
        return {
            'role': self.role,
            'content': self.content
        }