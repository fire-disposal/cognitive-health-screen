from typing import Any, Optional, Dict, List, TypeVar, Generic
from pydantic import BaseModel
from fastapi.responses import JSONResponse

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    """
    通用响应模型
    """
    code: int = 200
    msg: str = "OK"
    data: Optional[T] = None

class PaginatedResponseModel(ResponseModel[List[T]]):
    """
    分页响应模型
    """
    total: int = 0
    page: int = 1
    page_size: int = 20

class SuccessResponse(JSONResponse):
    """
    成功响应
    """
    def __init__(
        self,
        code: int = 200,
        msg: Optional[str] = "OK",
        data: Optional[Any] = None,
        **kwargs,
    ):
        content = {"code": code, "msg": msg, "data": data}
        content.update(kwargs)
        super().__init__(content=content, status_code=code)

class FailResponse(JSONResponse):
    """
    失败响应
    """
    def __init__(
        self,
        code: int = 400,
        msg: Optional[str] = "操作失败",
        data: Optional[Any] = None,
        **kwargs,
    ):
        content = {"code": code, "msg": msg, "data": data}
        content.update(kwargs)
        super().__init__(content=content, status_code=code)

class PaginatedResponse(JSONResponse):
    """
    分页响应
    """
    def __init__(
        self,
        code: int = 200,
        msg: Optional[str] = "OK",
        data: Optional[Any] = None,
        total: int = 0,
        page: int = 1,
        page_size: int = 20,
        **kwargs,
    ):
        content = {
            "code": code,
            "msg": msg,
            "data": data,
            "total": total,
            "page": page,
            "page_size": page_size,
        }
        content.update(kwargs)
        super().__init__(content=content, status_code=code)