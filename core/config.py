from dotenv import load_dotenv
import os

load_dotenv()

ORIGINS = os.environ.get("ORIGINS").split(",")
DATA_PATH = os.environ.get("DATA_PATH")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
RAG_LLM_MODEL = os.environ.get("RAG_LLM_MODEL")
HOST = os.environ.get("HOST")
RAG_EMBEDDING_MODEL = os.environ.get("RAG_EMBEDDING_MODEL")
BASE_PROMPT = os.environ.get("BASE_PROMPT")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
CODE_EMBEDDING_MODEL = os.environ.get("CODE_EMBEDDING_MODEL")
WHISPER_MODEL = os.environ.get("WHISPER_MODEL")
MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
MINIO_BUCKET = os.environ.get("MINIO_BUCKET")
MINIO_BAST_PATH = os.environ.get("MINIO_BAST_PATH")
ROCKETMQ_TOPIC = os.environ.get("ROCKETMQ_TOPIC")
ROCKETMQ_NAMESERVER_ADDRESS = os.environ.get("ROCKETMQ_NAMESERVER_ADDRESS")
ROCKETMQ_ACCESS_KEY = os.environ.get("ROCKETMQ_ACCESS_KEY")
ROCKETMQ_ACCESS_SECRET = os.environ.get("ROCKETMQ_ACCESS_SECRET")
