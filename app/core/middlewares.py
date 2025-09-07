"""中间件模块

提供应用级别的中间件实现：
1. 基础中间件基类 
2. 后台任务中间件
"""

from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request

from .bgtask import BgTasks


class SimpleBaseMiddleware:
    """基础中间件基类
    
    提供请求前后处理的基础结构
    """
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)

        response = await self.before_request(request) or self.app
        await response(request.scope, request.receive, send)
        await self.after_request(request)

    async def before_request(self, request: Request):
        """请求前处理钩子"""
        return self.app

    async def after_request(self, request: Request):
        """请求后处理钩子"""
        return None


class BackGroundTaskMiddleware(SimpleBaseMiddleware):
    """后台任务中间件
    
    处理请求过程中产生的后台任务：
    1. 请求前初始化任务队列
    2. 请求后执行队列中的任务
    """
    async def before_request(self, request):
        """初始化后台任务队列"""
        await BgTasks.init_bg_tasks_obj()

    async def after_request(self, request):
        """执行后台任务"""
        await BgTasks.execute_tasks()
