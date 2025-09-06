"""
数据库初始化数据模块
负责初始化用户、菜单、API、角色等基础数据
"""

from typing import Dict, List
from tortoise.expressions import Q
from app.log import logger

from app.models.admin import Api, Menu, Role, User
from app.controllers.api import api_controller
from app.controllers.user import UserCreate, user_controller
from app.schemas.system.menu import MenuType
from app.schemas.health.device import DeviceCreate
from app.controllers.health.device import device_controller

# ================== 数据集中定义 ================== #

ROLES = [
    {"name": "管理员", "desc": "管理员角色", "grant_all": True},
    {"name": "普通用户", "desc": "普通用户角色", "grant_all": False},
]

USERS = [
    {
        "username": "admin",
        "email": "admin@admin.com",
        "password": "admin123",
        "is_active": True,
        "is_superuser": True,
        "roles": ["管理员"]
    },
]


MENU_DEFINITIONS = [
    {
        "name": "系统管理",
        "parent_id": 0,
        "defaults": {
            "menu_type": MenuType.CATALOG,
            "path": "/system",
            "order": 1,
            "icon": "carbon:gui-management",
            "is_hidden": False,
            "component": "Layout",
            "keepalive": False,
            "redirect": "/system/user",
        },
        "children": [
            {"name": "用户管理", "path": "user", "order": 1, "icon": "material-symbols:person-outline-rounded", "component": "/system/user"},
            {"name": "角色管理", "path": "role", "order": 2, "icon": "carbon:user-role", "component": "/system/role"},
            {"name": "菜单管理", "path": "menu", "order": 3, "icon": "material-symbols:list-alt-outline", "component": "/system/menu"},
            {"name": "API管理", "path": "api", "order": 4, "icon": "ant-design:api-outlined", "component": "/system/api"},
            {"name": "部门管理", "path": "dept", "order": 5, "icon": "mingcute:department-line", "component": "/system/dept"},
            {"name": "审计日志", "path": "auditlog", "order": 6, "icon": "ph:clipboard-text-bold", "component": "/system/auditlog"},
        ]
    },
    {
        "name": "健康管理",
        "parent_id": 0,
        "defaults": {
            "menu_type": MenuType.CATALOG,
            "path": "/health",
            "order": 2,
            "icon": "mdi:heart-pulse",
            "is_hidden": False,
            "component": "Layout",
            "keepalive": False,
            "redirect": "/health/patient",
        },
        "children": [
            {"name": "病人管理", "path": "patient", "order": 1, "icon": "material-symbols:person-outline-rounded", "component": "/health/patient"},
            {"name": "设备管理", "path": "device", "order": 2, "icon": "carbon:user-role", "component": "/health/device"},
            {"name": "健康数据", "path": "health_data", "order": 3, "icon": "ant-design:api-outlined", "component": "/health/health_data"},
            {"name": "健康评估", "path": "assessment", "order": 4, "icon": "mdi:clipboard-check-multiple", "component": "/health/assessment"},
            {"name": "告警中心", "path": "alert", "order": 5, "icon": "mdi:bell-alert-outline", "component": "/health/alert"},
            {"name": "统计分析", "path": "analysis", "order": 7, "icon": "mdi:chart-line", "component": "/health/analysis"},
        ]
    },
    {
        "name": "数字孪生",
        "parent_id": 0,
        "defaults": {
            "menu_type": MenuType.MENU,
            "path": "/twinview",
            "order": 4,
            "icon": "material-symbols:view-in-ar",
            "is_hidden": False,
            "component": "/twinview",
            "keepalive": False,
        },
        "children": []
    }
]

PATIENTS = [
    {"name": "王强", "age": 65, "gender": "男", "device": {
        "device_id": "watch-1",
        "name": "智能手环A1",
        "description": "支持心率、步数监测，适合老年人",
        "model": "A1",
        "device_type": "手环",
        "data_types": ["heart_rate", "steps"],
    }},
    {"name": "李丽", "age": 72, "gender": "女", "device": {
        "device_id": "bp-1001",
        "name": "电子血压计BP-1001",
        "description": "高精度血压监测设备",
        "model": "BP-1001",
        "device_type": "血压计",
        "data_types": ["blood_pressure"],
    }},
    {"name": "张伟", "age": 58, "gender": "男", "device": {
        "device_id": "oximeter-01",
        "name": "血氧仪Oxi-01",
        "description": "便携式血氧仪，适合慢性病患者",
        "model": "Oxi-01",
        "device_type": "血氧仪",
        "data_types": ["blood_oxygen"],
    }},
]

ALERT_CASES = [
    {
        "patient_name": "王强",
        "device_id": "watch-1",
        "alerts": [
            {"rule_name": "心率过高", "level": "warning", "message": "王强心率超过120次/分，建议休息并复查。",
             "status": "active", "event_type": "abnormal", "description": "心率异常事件",
             "extra": {"value": 130, "unit": "bpm"}},
        ],
    }
]

# ================== 初始化器类 ================== #

class DataInitializer:

    @staticmethod
    async def _get_or_update_menu(name: str, parent_id: int, defaults: Dict) -> Menu:
        menu = await Menu.filter(name=name, parent_id=parent_id).first()
        if menu:
            await menu.update_from_dict(defaults).save()
            return menu
        return await Menu.create(name=name, parent_id=parent_id, **defaults)

    @classmethod
    async def _init_menu_tree(cls, menu_def: dict, parent_id: int = 0):
        menu = await cls._get_or_update_menu(menu_def["name"], parent_id, menu_def["defaults"])
        for child in menu_def.get("children", []):
            await cls._get_or_update_menu(
                name=child["name"],
                parent_id=menu.id,
                defaults={
                    "menu_type": MenuType.MENU,
                    "path": child["path"],
                    "order": child["order"],
                    "icon": child["icon"],
                    "is_hidden": False,
                    "component": child["component"],
                    "keepalive": False,
                }
            )

    @staticmethod
    async def _create_roles():
        """批量创建角色并赋予权限"""
        role_map = {}
        all_apis = await Api.all()
        all_menus = await Menu.all()
        basic_apis = await Api.filter(Q(method__in=["GET"]) | Q(tags="基础模块"))

        for r in ROLES:
            role, _ = await Role.get_or_create(name=r["name"], defaults={"desc": r["desc"]})
            role_map[r["name"]] = role

            if r["grant_all"]:
                if all_apis:
                    await role.apis.add(*all_apis)
                if all_menus:
                    await role.menus.add(*all_menus)
            else:
                if basic_apis:
                    await role.apis.add(*basic_apis)
                if all_menus:
                    await role.menus.add(*all_menus)

        logger.info(f"已初始化角色: {', '.join(role_map.keys())}")
        return role_map


    @staticmethod
    async def _create_users(role_map: dict):
        """批量创建初始用户并绑定角色"""
        for u in USERS:
            if not await User.exists(username=u["username"]):
                user_obj = await user_controller.create_user(UserCreate(**{
                    k: v for k, v in u.items() if k != "roles"
                }))
                logger.info(f"已创建用户: {u['username']}")
            else:
                user_obj = await User.get(username=u["username"])
                logger.debug(f"用户已存在: {u['username']}")

            # 绑定角色
            for role_name in u.get("roles", []):
                role = role_map.get(role_name)
                if role:
                    await user_obj.roles.add(role)
                    logger.info(f"已为用户 {u['username']} 绑定角色 {role_name}")


    @staticmethod
    async def _create_patients_and_devices():
        from app.models.health.patient import Patient
        from app.models.health.device import Device
        for p in PATIENTS:
            patient, _ = await Patient.get_or_create(
                name=p["name"], defaults={"age": p["age"], "gender": p["gender"]}
            )
            dev_info = p["device"]
            device = await Device.filter(device_id=dev_info["device_id"]).first()
            if not device:
                device = await device_controller.create(DeviceCreate(**dev_info))
                logger.info(f"已初始化测试设备: {device.device_id}")
            await device_controller.bind_patient(device.id, patient.id)
            logger.info(f"已将设备 {device.device_id} 绑定到患者 {patient.name}")

    @staticmethod
    async def _create_alerts():
        from app.models.health.patient import Patient
        from app.models.health.device import Device
        from app.models.health.alert import Alert
        for case in ALERT_CASES:
            patient = await Patient.filter(name=case["patient_name"]).first()
            device = await Device.filter(device_id=case["device_id"]).first()
            if not patient or not device:
                logger.error(f"患者或设备不存在: {case['patient_name']}/{case['device_id']}")
                continue
            for alert in case["alerts"]:
                await Alert.create(
                    device_id=device.id,
                    patient_id=patient.id,
                    **alert
                )
        logger.info("已初始化测试告警数据")

    @staticmethod
    async def _refresh_apis():
        await api_controller.refresh_api()

    @classmethod
    async def initialize_basic_data(cls):
        logger.info("开始初始化基础数据...")
        steps = [
            ("刷新 API", cls._refresh_apis),
            ("创建菜单 - 系统管理", lambda: cls._init_menu_tree(MENU_DEFINITIONS[0])),
            ("创建菜单 - 健康管理", lambda: cls._init_menu_tree(MENU_DEFINITIONS[1])),
            ("创建菜单 - 数字孪生", lambda: cls._init_menu_tree(MENU_DEFINITIONS[2])),
            ("创建患者及设备", cls._create_patients_and_devices),
            ("初始化告警数据", cls._create_alerts),
        ]

        # 角色与用户需要顺序执行
        try:
            logger.debug("执行步骤: 创建角色")
            role_map = await cls._create_roles()
            logger.debug("执行步骤: 创建用户")
            await cls._create_users(role_map)
        except Exception as e:
            logger.error(f"角色/用户初始化失败: {e}")

        # 其余步骤
        for label, func in steps:
            try:
                logger.debug(f"执行步骤: {label}")
                await func()
            except Exception as e:
                logger.error(f"{label}失败: {e}")

        logger.info("基础数据初始化完成")

