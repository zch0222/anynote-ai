from fastapi import APIRouter, Depends, Request

from service.rag_service import RagService
from model.dto import RagFileIndexDTO, ResData, RagQueryDTO, GithubQueryDTO
from core.redis_server import RedisServer
from fastapi.responses import StreamingResponse
import uuid

rag_router = APIRouter()


def get_rag_service(request: Request) -> RagService:
    return RagService(RedisServer(request.app.state.redis))


@rag_router.post("/api/rag/index")
def index(request: Request, data: RagFileIndexDTO, service: RagService = Depends(get_rag_service)):
    rag_file_index_vo = service.index_pdf(data)
    return ResData.success(rag_file_index_vo.to_dict())


@rag_router.post("/api/rag/github")
def query_github(request: Request, data: GithubQueryDTO, service: RagService = Depends(get_rag_service)):
    return ResData.success(service.query_github(data).to_dict())


@rag_router.post("/api/rag/github/index")
def github_index(request: Request, service: RagService = Depends(get_rag_service)):
    pass


@rag_router.post("/api/rag/query")
async def query(request: Request, data: RagQueryDTO, service: RagService = Depends(get_rag_service)):
    # rag_query_vo = service.query(data)
    task_id = uuid.uuid4().__str__()
    service.query(data, task_id)
    headers = {
        # 设置返回数据类型是SSE
        'Content-Type': 'text/event-stream;charset=UTF-8',
        # 保证客户端的数据是新的
        'Cache-Control': 'no-cache',
    }
    return StreamingResponse(service.get_rag_stream(task_id), headers=headers)


@rag_router.post("/api/rag/query/v2")
async def query_v2(request: Request, data: RagQueryDTO, service: RagService = Depends(get_rag_service)):
    # rag_query_vo = service.query(data)
    task_id = uuid.uuid4().__str__()
    # service.query(data, task_id)
    headers = {
        # 设置返回数据类型是SSE
        'Content-Type': 'text/event-stream;charset=UTF-8',
        # 保证客户端的数据是新的
        'Cache-Control': 'no-cache',
    }
    return StreamingResponse(service.query_v2(data, task_id), headers=headers)
