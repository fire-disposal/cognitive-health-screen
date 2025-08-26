import logging

from fastapi import APIRouter, Query

from app.controllers.menu import menu_controller
from app.schemas.base import FailResponse, SuccessResponse, PaginatedResponse
from app.schemas.system.menu import MenuCreate, MenuUpdate, MenuResponse, MenuQuery, MenuType

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list", summary="查看菜单列表")
async def list_menu(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
):
    menu_tree = await menu_controller.get_menu_tree(page=page, page_size=page_size)
    return PaginatedResponse(data=menu_tree, total=len(menu_tree), page=page, page_size=page_size)


@router.get("/get", summary="查看菜单")
async def get_menu(
    menu_id: int = Query(..., description="菜单id"),
):
    result = await menu_controller.get(id=menu_id)
    return SuccessResponse(data=result)


@router.post("/create", summary="创建菜单")
async def create_menu(
    menu_in: MenuCreate,
):
    await menu_controller.create(obj_in=menu_in)
    return SuccessResponse(msg="Created Success")


@router.post("/update", summary="更新菜单")
async def update_menu(
    menu_in: MenuUpdate,
):
    await menu_controller.update(id=menu_in.id, obj_in=menu_in)
    return SuccessResponse(msg="Updated Success")


@router.delete("/delete", summary="删除菜单")
async def delete_menu(
    id: int = Query(..., description="菜单id"),
):
    if await menu_controller.has_children(id):
        return FailResponse(msg="Cannot delete a menu with child menus")
    await menu_controller.remove(id=id)
    return SuccessResponse(msg="Deleted Success")
