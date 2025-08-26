from typing import List, Optional, Dict, Any

from app.core.crud import CRUDBase
from app.models.admin import Menu, User, Role
from app.schemas.system.menu import MenuCreate, MenuUpdate


class MenuController(CRUDBase[Menu, MenuCreate, MenuUpdate]):
    def __init__(self):
        super().__init__(model=Menu)

    async def get_by_menu_path(self, path: str) -> Optional["Menu"]:
        return await self.model.filter(path=path).first()
    
    async def get_all_menus(self) -> List[Menu]:
        """获取所有菜单"""
        return await self.model.all()
    
    async def get_user_menus(self, user_obj: User) -> List[dict]:
        """获取用户菜单，包括层级结构"""
        menus: List[Menu] = []
        
        if user_obj.is_superuser:
            menus = await self.get_all_menus()
        else:
            role_objs: List[Role] = await user_obj.roles
            for role_obj in role_objs:
                menu = await role_obj.menus
                menus.extend(menu)
            menus = list(set(menus))
        
        # 构建菜单树结构
        parent_menus: List[Menu] = []
        for menu in menus:
            if menu.parent_id == 0:
                parent_menus.append(menu)
        
        result = []
        for parent_menu in parent_menus:
            parent_menu_dict = await parent_menu.to_dict()
            parent_menu_dict["children"] = []
            for menu in menus:
                if menu.parent_id == parent_menu.id:
                    parent_menu_dict["children"].append(await menu.to_dict())
            result.append(parent_menu_dict)
            
        return result
    
    async def get_menu_tree(self, page: int, page_size: int) -> List[Dict[str, Any]]:
        """获取完整的菜单树结构"""
        async def get_menu_with_children(menu_id: int) -> Dict[str, Any]:
            menu = await self.model.get(id=menu_id)
            menu_dict = {
                "id": menu.id,
                "name": menu.name,
                "path": menu.path,
                "component": menu.component,
                "redirect": menu.redirect,
                "parent_id": menu.parent_id,
                "icon": menu.icon,
                "order": menu.order,
                "is_hidden": menu.is_hidden,
                "menu_type": menu.menu_type,
                "keepalive": menu.keepalive,
                "remark": menu.remark
            }
            child_menus = await self.model.filter(parent_id=menu_id).order_by("order")
            menu_dict["children"] = [
                await get_menu_with_children(child.id) for child in child_menus
            ]
            return menu_dict

        parent_menus = await self.model.filter(parent_id=0).order_by("order")
        menu_tree = [await get_menu_with_children(menu.id) for menu in parent_menus]
        return menu_tree
    
    async def has_children(self, menu_id: int) -> bool:
        """检查菜单是否有子菜单"""
        return await self.model.filter(parent_id=menu_id).count() > 0


menu_controller = MenuController()
