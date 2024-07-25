from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, Depends, Request, BackgroundTasks
from service.whisper_service import WhisperService
from model.dto import WhisperRunDTO, ResData
from fastapi.responses import StreamingResponse

whisper_router = APIRouter()


def get_whisper_service() -> WhisperService:
    return WhisperService()


@whisper_router.post('/api/whisper')
async def whisper(request: Request, data: WhisperRunDTO, background_tasks: BackgroundTasks,
                  service: WhisperService = Depends(get_whisper_service)):
    headers = {
        # 设置返回数据类型是SSE
        'Content-Type': 'text/event-stream;charset=UTF-8',
        # 保证客户端的数据是新的
        'Cache-Control': 'no-cache',
    }
    return StreamingResponse(service.whisper(data, background_tasks), headers=headers)


@whisper_router.post("/api/whisper/submit")
async def whisper_submit(request: Request, data: WhisperRunDTO, service: WhisperService = Depends(get_whisper_service)):
    res = await service.submit_whisper_task(data)
    return ResData.success(res.to_dict())

@whisper_router.get("/api/whisper/{task_id}")
async def whisper_get_task(request: Request, task_id: str, service: WhisperService = Depends(get_whisper_service)):
    headers = {
        # 设置返回数据类型是SSE
        'Content-Type': 'text/event-stream;charset=UTF-8',
        # 保证客户端的数据是新的
        'Cache-Control': 'no-cache',
    }
    return StreamingResponse(service.get_whisper_task_status(task_id), headers=headers)

