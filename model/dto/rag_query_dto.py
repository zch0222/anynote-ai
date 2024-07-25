from pydantic import BaseModel


class RagQueryDTO(BaseModel):
    file_hash: str
    prompt: str
    # 文件名称
    file_name: str
    # 作者
    author: str
    # 文档分类
    category: str
    # 描述
    description: str
