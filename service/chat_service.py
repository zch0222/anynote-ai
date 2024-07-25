from model.dto import ChatDTO
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
import time
import json
from model.vo import ChatVO
from model.vo.chat_vo import Choice
from model.bo import ChatMessageBO
from constants.chat_model_constants import CHAT_MODELS
from llama_index.core import SummaryIndex
from llama_index.readers.web import SimpleWebPageReader
from duckduckgo_search import DDGS


class ChatService:

    def __init__(self):
        pass

    def yield_results(self, model: str, content: str):
        now = time.time()
        yield 'id: {}\nevent: message\ndata: {}\n\n'.format(now, json.dumps({
            "id": now,
            "created": now,
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "content": content
                    }
                }
            ]
        }))

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

    def build_web_search_documents_index(self, query):

        link_list = []
        with DDGS() as ddgs:
            search_res_list = ddgs.text(query, region='cn-zh', max_results=10)
            for search_res in search_res_list:
                print(search_res["href"])
                link_list.append(search_res["href"])
        print(0)
        print(link_list[0])

        documents = SimpleWebPageReader(html_to_text=True).load_data(
            link_list
        )
        index = SummaryIndex.from_documents(documents)
        return index

    def gemma2_web_search(self, chat_dto: ChatDTO):
        query = chat_dto.messages[len(chat_dto.messages)-1].content
        index = self.build_web_search_documents_index(query)
        query_engine = index.as_query_engine(llm=Ollama(model="gemma2", request_timeout=30.0))
        response = query_engine.query(query)
        yield from self.yield_results(chat_dto.model, str(response))

    def chat(self, chat_dto: ChatDTO):
        if "gemma" == chat_dto.model:
            yield from self.chat_gemma(chat_dto)
        elif CHAT_MODELS["GEMMA2_WEB_SEARCH"] == chat_dto.model:
            yield from self.gemma2_web_search(chat_dto)
        else:
            yield from self.chat_ollama(chat_dto)
