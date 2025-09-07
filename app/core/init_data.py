"""
数据库初始化数据模块
负责初始化用户、设备、健康档案等基础数据
"""

import logging
from typing import Dict
from app.models.users import AdminUser, AppUser
from app.models.health import HealthProfile, Device, Alert
from app.schemas.users import AdminUserCreate, AppUserCreate
from app.schemas.health import DeviceCreate
from app.utils.password import get_password_hash

logger = logging.getLogger(__name__)

# ================== 数据集中定义 ================== #

ADMIN_USERS = [
    {
        "username": "admin",
        "email": "admin@admin.com",
        "password": "admin123",
        "role": "superuser",
        "is_active": True,
    },
    {
        "username": "manager",
        "email": "manager@admin.com",
        "password": "manager123",
        "role": "admin",
        "is_active": True,
    }
]

APP_USERS = [
    {
        "username": "patient1",
        "email": "patient1@example.com",
        "password": "patient123",
        "phone": "13800138001",
        "is_active": True,
    },
    {
        "username": "patient2", 
        "email": "patient2@example.com",
        "password": "patient123",
        "phone": "13800138002",
        "is_active": True,
    }
]

PATIENTS = [
    {
        "name": "王强",
        "gender": "male",
        "birth_date": "1960-01-01",
        "user_id": 1,  # 关联 patient1
        "device": {
            "serial_number": "watch-1",
            "name": "智能手环A1",
            "device_type": "手环",
        }
    },
    {
        "name": "李丽",
        "gender": "female", 
        "birth_date": "1955-06-15",
        "user_id": 2,  # 关联 patient2
        "device": {
            "serial_number": "bp-1001",
            "name": "电子血压计BP-1001",
            "device_type": "血压计",
        }
    }
]

ALERTS = [
    {
        "patient_name": "王强",
        "device_sn": "watch-1",
        "alerts": [
            {
                "rule_name": "心率过高",
                "level": "warning",
                "message": "心率超过120次/分，建议休息并复查",
                "event_type": "heart_rate_high",
                "description": "心率异常事件",
                "status": "active",
                "extra": {"value": 130, "unit": "bpm"}
            },
        ]
    }
]

# ================== 初始化器类 ================== #

class DataInitializer:
    
    @staticmethod
    async def _create_admin_users():
        """创建管理员用户"""
        created = []
        updated = []
        try:
            for user_data in ADMIN_USERS:
                data = user_data.copy()  # 创建副本以避免修改原始数据
                password = data.pop("password")
                data["password_hash"] = get_password_hash(password)
                
                user = await AdminUser.get_or_none(username=data["username"])
                if not user:
                    user = await AdminUser.create(**data)
                    created.append(user.username)
                else:
                    await user.update_from_dict(data).save()
                    updated.append(user.username)
            
            if created:
                logger.info(f"创建了以下管理员用户: {', '.join(created)}")
            if updated:
                logger.info(f"更新了以下管理员用户: {', '.join(updated)}")
                
        except Exception as e:
            error_msg = f"创建管理员用户时发生错误: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    @staticmethod
    async def _create_app_users():
        """创建应用用户"""
        created = []
        updated = []
        try:
            for user_data in APP_USERS:
                data = user_data.copy()  # 创建副本以避免修改原始数据
                password = data.pop("password")
                data["password_hash"] = get_password_hash(password)
                
                user = await AppUser.get_or_none(username=data["username"])
                if not user:
                    user = await AppUser.create(**data)
                    created.append(user.username)
                else:
                    await user.update_from_dict(data).save()
                    updated.append(user.username)
            
            if created:
                logger.info(f"创建了以下应用用户: {', '.join(created)}")
            if updated:
                logger.info(f"更新了以下应用用户: {', '.join(updated)}")
                
        except Exception as e:
            error_msg = f"创建应用用户时发生错误: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    @staticmethod
    async def _create_patients_and_devices():
        """创建患者档案和设备"""
        for p in PATIENTS:
            device_data = p.pop("device")
            patient = await HealthProfile.get_or_none(name=p["name"])
            
            if not patient:
                patient = await HealthProfile.create(**p)
                logger.info(f"Created patient profile: {patient.name}")
            else:
                await patient.update_from_dict(p).save()
                logger.info(f"Updated patient profile: {patient.name}")

            # 创建或更新设备
            device = await Device.get_or_none(serial_number=device_data["serial_number"])
            if not device:
                device = await Device.create(**device_data)
                logger.info(f"Created device: {device.serial_number}")
            else:
                await device.update_from_dict(device_data).save()
                logger.info(f"Updated device: {device.serial_number}")

    @staticmethod
    async def _create_alerts():
        """创建告警数据"""
        for case in ALERTS:
            patient = await HealthProfile.get_or_none(name=case["patient_name"])
            device = await Device.get_or_none(serial_number=case["device_sn"])
            
            if not patient or not device:
                logger.error(f"Patient or device not found: {case['patient_name']}/{case['device_sn']}")
                continue
                
            for alert_data in case["alerts"]:
                alert_data["health_profile_id"] = patient.id
                alert_data["device_id"] = device.id
                
                alert = await Alert.create(**alert_data)
                logger.info(f"Created alert for patient {patient.name}")

    @classmethod
    async def initialize_basic_data(cls):
        """初始化所有基础数据"""
        logger.info("开始初始化基础数据...")
        
        steps = [
            ("Create admin users", cls._create_admin_users),
            ("Create app users", cls._create_app_users),
            ("Create patients and devices", cls._create_patients_and_devices),
            ("Create alerts", cls._create_alerts),
        ]

        failed_steps = []
        for label, func in steps:
            try:
                logger.debug(f"正在执行步骤: {label}")
                await func()
                logger.info(f"步骤 {label} 执行成功")
            except Exception as e:
                error_msg = f"步骤 {label} 执行失败: {str(e)}"
                logger.error(error_msg)
                failed_steps.append((label, str(e)))
                # 不立即退出，继续执行其他步骤
                continue

        if failed_steps:
            error_summary = "\n".join([f"- {label}: {error}" for label, error in failed_steps])
            raise RuntimeError(f"数据初始化过程中发生以下错误:\n{error_summary}")
        else:
            logger.info("所有基础数据初始化完成")
