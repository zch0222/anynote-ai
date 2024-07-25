from pydantic import BaseModel
from model.bo import ChatMessageBO
from typing import List

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    def to_dict(self):
        return {
            'prompt_tokens': self.prompt_tokens,
            'completion_tokens': self.completion_tokens,
            'total_tokens': self.total_tokens
        }

class Choice(BaseModel):
    index: int
    message: ChatMessageBO
    logprobs: object | None
    finish_reason: str | None

    def to_dict(self):
        return {
            'index': self.index,
            'message': self.message.to_dict(),
            'logprobs': self.logprobs,
            'finish_reason': self.finish_reason
        }

class ChatVO(BaseModel):
    id: str
    object: str | None
    created: int
    model: str
    system_fingerprint: str | None
    choices: List[Choice]
    usage: Usage | None

    def get_choices(self):
        choice_dict_list = []
        for choice in self.choices:
            choice_dict_list.append(choice.to_dict())
        return choice_dict_list


    def to_dict(self):
        return {
            "id": self.id,
            "object": self.object,
            "created": self.created,
            "model": self.model,
            "system_fingerprint": self.system_fingerprint,
            "choices": self.get_choices(),
            "usage": self.usage.to_dict()
        }
