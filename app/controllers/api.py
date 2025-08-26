from typing import List
from fastapi.routing import APIRoute

from app.core.crud import CRUDBase
from app.log import logger
from app.models.admin import Api, User
from app.schemas.system.api import ApiCreate, ApiUpdate


class ApiController(CRUDBase[Api, ApiCreate, ApiUpdate]):
    def __init__(self):
        super().__init__(model=Api)

    async def get_all_apis(self) -> List[Api]:
        """获取所有API"""
        return await self.model.all()

    async def get_user_apis(self, user_obj: User) -> List[str]:
        """获取用户可访问的API列表"""
        if user_obj.is_superuser:
            api_objs = await self.get_all_apis()
            return [api.method.lower() + api.path for api in api_objs]
        
        role_objs = await user_obj.roles
        apis = []
        for role_obj in role_objs:
            api_objs = await role_obj.apis
            apis.extend([api.method.lower() + api.path for api in api_objs])
        return list(set(apis))

    async def refresh_api(self):
        from app import app

        # 删除废弃API数据
        all_api_list = []
        created_count = 0
        updated_count = 0
        deleted_count = 0
        
        for route in app.routes:
            # 只更新有鉴权的API
            if isinstance(route, APIRoute) and len(route.dependencies) > 0:
                all_api_list.append((list(route.methods)[0], route.path_format))
        
        # 处理需要删除的API
        delete_api = []
        for api in await Api.all():
            if (api.method, api.path) not in all_api_list:
                delete_api.append((api.method, api.path))
        
        for method, path in delete_api:
            try:
                await Api.filter(method=method, path=path).delete()
                deleted_count += 1
            except Exception as e:
                logger.error(f"<red>删除API失败 {method} {path}: {str(e)}</red>")

        # 处理需要创建或更新的API
        for route in app.routes:
            if isinstance(route, APIRoute) and len(route.dependencies) > 0:
                method = list(route.methods)[0]
                path = route.path_format
                summary = route.summary
                tags = list(route.tags)[0]
                try:
                    api_obj = await Api.filter(method=method, path=path).first()
                    if api_obj:
                        await api_obj.update_from_dict(dict(method=method, path=path, summary=summary, tags=tags)).save()
                        updated_count += 1
                    else:
                        await Api.create(**dict(method=method, path=path, summary=summary, tags=tags))
                        created_count += 1
                except Exception as e:
                    logger.error(f"创建/更新API失败 {method} {path}: {str(e)}")
        
        # 输出统计信息
        logger.info(f"API刷新完成: 创建 {created_count} 个, 更新 {updated_count} 个, 删除 {deleted_count} 个")


api_controller = ApiController()
