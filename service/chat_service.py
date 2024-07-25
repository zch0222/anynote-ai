from model.dto import ChatDTO
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
import time
import json
from model.vo import ChatVO
from model.vo.chat_vo import Choice
from model.bo import ChatMessageBO

class ChatService:

    def __init__(self):
        pass

    def chat_ollama(self, chat_dto: ChatDTO):
        print(chat_dto.model)
        chat_ollama = Ollama(model=chat_dto.model, request_timeout=30.0)
        messages = []
        for message in chat_dto.messages:
            messages.append(ChatMessage(content=message.content, role=message.role))
        # resp = chat_ollama.chat(messages)
        # print(resp)
        response = chat_ollama.stream_chat(messages)
        #
        for r in response:
            now = time.time()
            print(r.delta)
            yield 'id: {}\nevent: message\ndata: {}\n\n'.format(now, json.dumps({
                "id": now,
                "created": now,
                "model": chat_dto.model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "content": r.delta
                        }
                    }
                ]
            }))
        # for r in response:
        #     print(r.delta, end="")

    def chat_gemma(self, chat_dto: ChatDTO):
        yield from self.chat_ollama(chat_dto)

    def chat(self, chat_dto: ChatDTO):
        if "gemma" == chat_dto.model:
            yield from self.chat_gemma(chat_dto)
        else:
            yield from self.chat_ollama(chat_dto)
