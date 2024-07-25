from fastapi import APIRouter, Depends, Request
from core.redis_server import RedisServer
from model.dto import ResData, GithubIndexDTO, GithubQueryDTO

from service.data_connect_service import DataConnectService

data_connect_router = APIRouter()


def get_data_connect_service(request: Request) -> DataConnectService:
    return DataConnectService(RedisServer(request.app.state.redis))


@data_connect_router.post("/api/github/index")
def github_index(request: Request, data: GithubIndexDTO,
                 service: DataConnectService = Depends(get_data_connect_service)):
    return ResData.success(service.index_github(data))


@data_connect_router.post("/api/github/query")
def github_query(request: Request, data: GithubQueryDTO,
                 service: DataConnectService = Depends(get_data_connect_service)):
    return ResData.success(service.query_github(data))
