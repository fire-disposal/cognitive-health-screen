from fastapi import APIRouter

role_router = APIRouter(
    prefix="/role",
    tags=["role"]
)

@role_router.get("/")
async def get_roles():
    """
    获取所有角色列表
    """
    return {"roles": []}

@role_router.post("/")
async def create_role(role: dict):
    """
    创建新角色
    """
    return {"msg": "角色创建成功", "role": role}