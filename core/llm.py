# from constants.chat_model_constants import CHAT_MODELS
# from llama_index.llms.openai import OpenAI
# from llama_index.llms.ollama import Ollama
#
#
# def get_llm(model_name: str):
#     if "gemma" == model_name:
#         return Ollama(model=model_name)
#     elif CHAT_MODELS["GEMMA2_WEB_SEARCH"] == model_name:
#         yield from self.gemma2_web_search(chat_dto)
#     elif CHAT_MODELS["GEMMA_WEB_SEARCH"] == model_name:
#         yield from self.gemma_web_search(chat_dto)
#     elif CHAT_MODELS["GPT_4_TURBO_PREVIEW_WEB_SEARCH"] == model_name:
#         yield from self.gpt4_turbo_preview_search(chat_dto)
#     elif CHAT_MODELS["GPT_4_TURBO_PREVIEW"] == model_name:
#         yield from self.gpt4_turbo_preview(chat_dto)
#     elif CHAT_MODELS["GPT_4_TURBO_PREVIEW_WEB_SEARCH_V2"] == model_name:
#         return
#     else:
#         yield from self.chat_ollama(chat_dto)
