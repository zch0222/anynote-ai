from fastapi import FastAPI, HTTPException
from core.logger import get_logger
from controller.rag_controller import rag_router
from controller.data_connect_controller import data_connect_router
from controller.pandas_controller import pandas_router
from controller.whisper_controller import whisper_router
from controller.chattts_controller import chattts_router
from starlette.requests import Request
from starlette.responses import JSONResponse
from model.dto import ResData
from exceptions import BusinessException
from core.redis import get_redis_pool
from core.config import HOST, TOKEN
import redis
from core.executor import executor
from controller.chat_controller import chat_router
from fastapi.middleware.cors import CORSMiddleware
import json
from starlette.responses import Response



app = FastAPI()


# 路由
app.include_router(rag_router)
app.include_router(pandas_router)
app.include_router(data_connect_router)
app.include_router(whisper_router)
app.include_router(chattts_router)
app.include_router(chat_router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 业务异常处理
@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    logger = get_logger()
    logger.exception("An error occurred while processing request")
    return JSONResponse(
        status_code=200,
        content=ResData.error(exc.message)
    )

@app.middleware("http")
async def log_middleware(request: Request, call_next):

    logger = get_logger()
    # 记录请求信息
    request_body = await request.body()
    try:
        request_json = json.loads(request_body.decode())
    except json.JSONDecodeError:
        request_json = "Unable to decode JSON"
    logger.info(f"Request path: {request.url.path}, Method: {request.method}, Body: {request_json}")

    response = await call_next(request)
    # # 记录响应信息
    # response_body = [chunk async for chunk in response.body_iterator]
    # response_body = b"".join(response_body)
    # try:
    #     response_json = json.loads(response_body.decode())
    # except json.JSONDecodeError:
    #     response_json = response_body.decode()
    # logger.info(f"Response status: {response.status_code}, Body: {response_json}")
    #
    # # 重新构建响应，因为响应体已经被读取
    # new_response = Response(content=response_body, status_code=response.status_code, headers=dict(response.headers))
    return response


@app.middleware("http")
async def http_middleware(request: Request, call_next):
    # response = Response("Internal server error", status_code=500)
    if request.method == "OPTIONS":
        response = await call_next(request)
        return response
    try:
        token = request.headers["Authorization"]
        print(token)
        print(token.split()[-1])
        if token.split()[-1] != TOKEN:
            raise HTTPException(status_code=401, detail="Invalid token")
    except KeyError:
        raise HTTPException(status_code=401, detail="Missing token")

    # 继续处理请求
    response = await call_next(request)
    return response

# 全局异常处理
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger = get_logger()
    logger.exception("An error occurred while processing request")

    # 检查异常是否为HTTPException
    if isinstance(exc, HTTPException):
        # 如果是HTTPException，返回异常指定的状态码
        return JSONResponse(
            status_code=exc.status_code,
            content=ResData.error(exc.detail)
        )
    # 对于非HTTPException异常，返回500内部服务器错误
    return JSONResponse(
        status_code=500,
        content=ResData.error("An internal server error occurred")
    )


@app.on_event("startup")
async def startup_event():
    logger = get_logger()
    app.state.redis: redis.Redis = get_redis_pool()
    logger.info("fastapi start")


@app.on_event("shutdown")
async def shutdown_event():
    logger = get_logger()
    app.state.redis.connection_pool.disconnect()
    logger.info("Redis disconnected")
    executor.shutdown()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="app:app", host=HOST, port=8000, workers=4)
