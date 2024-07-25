import pandas as pd
from llama_index.core.query_engine import PandasQueryEngine
from model.dto import PandasQueryDTO
from model.vo import PandasQueryVO
from utils import download_file
from constants.pandas_constants import PANDAS_DATA_PATH
from core.logger import get_logger
from exceptions.business_exception import BusinessException


class PandasService:

    def __init__(self):
        self.logger = get_logger()

    def query_csv(self, pandas_query_dto: PandasQueryDTO) -> PandasQueryVO:
        self.logger.info(f"PANDAS QUERY START url: {pandas_query_dto.url}, prompt: {pandas_query_dto.prompt}")
        file_download_dto = download_file(pandas_query_dto.url, PANDAS_DATA_PATH)
        if not file_download_dto:
            raise BusinessException("下载失败")
        df = pd.read_csv(file_download_dto.file_path)
        query_engine = PandasQueryEngine(df=df, verbose=True)
        response = query_engine.query(pandas_query_dto.prompt)
        self.logger.info(f"PANDAS QUERY END url: {pandas_query_dto.url}, prompt: {pandas_query_dto.prompt}， response: {str(response)}")
        return PandasQueryVO(message=str(response))
