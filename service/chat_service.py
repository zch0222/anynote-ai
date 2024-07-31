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
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import ServiceContext
from llama_index.llms.openai import OpenAI
from core.config import HTTP_PROXY, HTTPS_PROXY
from core.logger import get_logger
from constants.prompt_constants import WEBSEARCH_PTOMPT_TEMPLATE
from llama_index.core.llms.llm import LLM
from typing import List


class ChatService:

    def __init__(self):
        self.logger = get_logger()

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

    def build_chat_message(self, chat_message_list: List[ChatMessageBO]):
        messages = []
        for message in chat_message_list:
            messages.append(ChatMessage(content=message.content, role=message.role))
        return messages

    def chat_openai(self, chat_dto: ChatDTO):
        openai_model = OpenAI(model=chat_dto.model)
        messages = []
        for message in chat_dto.messages:
            messages.append(ChatMessage(content=message.content, role=message.role))
        response = openai_model.stream_chat(messages)
        for r in response:
            yield from self.yield_results(chat_dto.model, r.delta)

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
        index = SummaryIndex.from_documents(documents, service_context=ServiceContext
                                            .from_defaults(
            embed_model=HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")))
        return index

    def add_source_numbers(self, lst, source_name="Source", use_source=True):
        if use_source:
            return [
                f'[{idx + 1}]\t "{item[0]}"\n{source_name}: {item[1]}'
                for idx, item in enumerate(lst)
            ]
        else:
            return [f'[{idx + 1}]\t "{item}"' for idx, item in enumerate(lst)]

    def generate(self, messages: [], llm: LLM, model_name: str):
        response = llm.stream_chat(messages)
        for r in response:
            yield from self.yield_results(model_name, r.delta)

    def web_search_chat(self, chat_dto: ChatDTO, llm: LLM):
        query = chat_dto.messages[len(chat_dto.messages) - 1].content
        proxies = None
        if HTTPS_PROXY is not None and HTTP_PROXY is not None:
            proxies = {
                "http": HTTP_PROXY,
                "https": HTTPS_PROXY
            }
        search_results = []
        # with DDGS(proxies=proxies) as ddgs:
        with DDGS(proxies=proxies) as ddgs:
            search_res_list = ddgs.text(query, max_results=10)
            for r in search_res_list:
                search_results.append(r)
        reference_results = []
        for idx, result in enumerate(search_results):
            self.logger.info(f"搜索结果{idx + 1}：{result}")
            reference_results.append([result["body"], result["href"]])
        reference_results = self.add_source_numbers(reference_results)
        prompt = (WEBSEARCH_PTOMPT_TEMPLATE
                  .replace("{query}", query)
                  .replace("{web_results}", "\n\n".join(reference_results))
                  .replace("{reply_language}", "Chinese"))
        self.logger.info(F"prompt:\n{prompt}")
        yield from self.generate(messages=[ChatMessage(content=prompt, role="user")],
                            llm=llm,
                            model_name=chat_dto.model)

    def gemma2_web_search(self, chat_dto: ChatDTO):
        query = chat_dto.messages[len(chat_dto.messages) - 1].content
        index = self.build_web_search_documents_index(query)
        query_engine = index.as_query_engine(llm=Ollama(model="gemma2", request_timeout=30.0))
        response = query_engine.query(query)
        yield from self.yield_results(chat_dto.model, str(response))

    def gemma_web_search(self, chat_dto: ChatDTO):
        print("BAAI/bge-small-zh-v1.5")
        # Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")
        query = chat_dto.messages[len(chat_dto.messages) - 1].content
        index = self.build_web_search_documents_index(query)
        print("start query")
        query_engine = index.as_query_engine(llm=Ollama(model="gemma"))
        print("start query open")
        response = query_engine.query(query)
        yield from self.yield_results(chat_dto.model, str(response))

    def gpt4_turbo_preview_search(self, chat_dto: ChatDTO):
        query = chat_dto.messages[len(chat_dto.messages) - 1].content
        index = self.build_web_search_documents_index(query)
        query_engine = index.as_query_engine(llm=OpenAI(model="gpt-4-turbo-preview"))
        response = query_engine.query(query)
        yield from self.yield_results(chat_dto.model, str(response))

    def gpt4_turbo_preview_search_v2(self, chat_dto: ChatDTO):
        llm = OpenAI(model="gpt-4-turbo-preview")
        yield from self.web_search_chat(chat_dto=chat_dto, llm=llm)

    def gpt4_turbo_preview(self, chat_dto: ChatDTO):
        yield from self.chat_openai(chat_dto)

    def chat(self, chat_dto: ChatDTO):
        print(chat_dto.model)
        # self.logger(F"{json.dumps(chat_dto)}")
        if "gemma" == chat_dto.model:
            yield from self.chat_gemma(chat_dto)
        elif CHAT_MODELS["GEMMA2"] == chat_dto.model:
            yield from self.chat_ollama(chat_dto)
        elif CHAT_MODELS["GEMMA2_WEB_SEARCH"] == chat_dto.model:
            yield from self.gemma2_web_search(chat_dto)
        elif CHAT_MODELS["GEMMA_WEB_SEARCH"] == chat_dto.model:
            yield from self.gemma_web_search(chat_dto)
        elif CHAT_MODELS["GPT_4_TURBO_PREVIEW_WEB_SEARCH"] == chat_dto.model:
            yield from self.gpt4_turbo_preview_search(chat_dto)
        elif CHAT_MODELS["GPT_4_TURBO_PREVIEW"] == chat_dto.model:
            yield from self.gpt4_turbo_preview(chat_dto)
        elif CHAT_MODELS["GPT_4_TURBO_PREVIEW_WEB_SEARCH_V2"] == chat_dto.model:
            yield from self.gpt4_turbo_preview_search_v2(chat_dto)
        else:
            yield from self.chat_openai(chat_dto)
