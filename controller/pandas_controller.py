from fastapi import APIRouter, Depends, Request
from model.dto import PandasQueryDTO, ResData
from service.pandas_service import PandasService

pandas_router = APIRouter()


@pandas_router.post("/api/pandas/query/csv")
async def pandas_query(request: Request, data: PandasQueryDTO, service: PandasService = Depends()):
    pandas_query_vo = service.query_csv(data)
    return ResData.success(pandas_query_vo.to_dict())
