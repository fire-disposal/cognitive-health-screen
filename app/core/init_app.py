"""应用初始化模块

负责FastAPI应用的初始化配置：
1. 中间件注册
2. 异常处理器注册
3. 路由注册
"""

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.exceptions import (
    DoesNotExist,
    DoesNotExistHandle,
    HTTPException,
    HttpExcHandle,
    IntegrityError,
    IntegrityHandle,
    RequestValidationError,
    RequestValidationHandle,
    ResponseValidationError,
    ResponseValidationHandle,
)
from app.settings.config import settings
from .middlewares import BackGroundTaskMiddleware

def make_middlewares() -> list[Middleware]:
    """注册中间件
    
    Returns:
        list[Middleware]: 中间件列表，按注册顺序执行
    """
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.CORS_ALLOW_METHODS,
            allow_headers=settings.CORS_ALLOW_HEADERS,
        ),
        Middleware(BackGroundTaskMiddleware),
    ]
    return middleware

def register_exceptions(app: FastAPI) -> None:
    """注册全局异常处理器
    
    Args:
        app: FastAPI 应用实例
    """
    app.add_exception_handler(DoesNotExist, DoesNotExistHandle)
    app.add_exception_handler(HTTPException, HttpExcHandle)
    app.add_exception_handler(IntegrityError, IntegrityHandle)
    app.add_exception_handler(RequestValidationError, RequestValidationHandle)
    app.add_exception_handler(ResponseValidationError, ResponseValidationHandle)

def register_routers(app: FastAPI, prefix: str = "/api") -> None:
    """注册路由
    
    Args:
        app: FastAPI 应用实例
        prefix: API前缀
    """
    app.include_router(api_router, prefix=prefix)
