from app.schemas.system import (
    user, role, menu, dept, api, login
)

# 从子模块收集所有声明的导出内容
__all__ = []
modules = [user, role, menu, dept, api, login]
for module in modules:
    __all__.extend(module.__all__)
    # 将子模块中声明的所有内容导入到当前命名空间
    for name in module.__all__:
        globals()[name] = getattr(module, name)
