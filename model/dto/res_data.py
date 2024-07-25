from dataclasses import dataclass
from pydantic import BaseModel
from typing import List, Any


@dataclass
class ResData:
    code: str
    msg: str
    data: object

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }

    @staticmethod
    def success(data: object):
        res_data = ResData("00000", "", data)
        return res_data.to_dict()

    @staticmethod
    def error(msg: str):
        res_data = ResData("A0001", msg, {})
        return res_data.to_dict()
