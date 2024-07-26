from fastapi import FastAPI
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
from core.config import HOST
import redis
from core.executor import executor
from controller.chat_controller import chat_router
from fastapi.middleware.cors import CORSMiddleware




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

# @app.middleware("http")
# async def http_middleware(request: Request, call_next):
#     response = Response("Internal server error", status_code=500)
#     try:
#         x_token = request.headers["X-Token"]
#         if x_token not in fake_tokens_db:
#             raise HTTPException(status_code=401, detail="Invalid token")
#     except KeyError:
#         raise HTTPException(status_code=401, detail="Missing token")
#
#     # 继续处理请求
#     response = await call_next(request)
#     return response

# 全局异常处理
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger = get_logger()
    logger.exception("An error occurred while processing request")
    return JSONResponse(
        status_code=200,
        content=ResData.error("An error occurred while processing requests")
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
