"""JWT 相关工具函数

包含 JWT token 的创建、解码、黑名单管理等功能。
"""

import jwt
from datetime import datetime, timezone
from typing import Dict, Set, Any

from app.schemas.auth import TokenData
from app.settings import settings

def create_access_token(*, data: TokenData) -> str:
    """创建 JWT access token
    
    Args:
        data: token数据对象
        
    Returns:
        str: 编码后的JWT token
    """
    payload = data.model_dump()
    encoded_jwt = jwt.encode(
        payload, 
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def decode_access_token(token: str) -> Dict[str, Any]:
    """解码并验证 JWT token
    
    Args:
        token: JWT token字符串
        
    Returns:
        Dict: 解码后的payload数据
        
    Raises:
        jwt.InvalidTokenError: token无效
        jwt.ExpiredSignatureError: token已过期
    """
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM]
    )

class TokenBlacklist:
    """Token黑名单管理
    
    用于管理已失效的token，支持：
    1. 用户主动登出时的token失效
    2. 刷新token时使旧token失效
    3. 定期清理过期token
    """
    def __init__(self):
        self._blacklist: Set[str] = set()
        
    async def add_token(self, token: str) -> None:
        """将token加入黑名单"""
        self._blacklist.add(token)
        await self._cleanup()
        
    async def is_blacklisted(self, token: str) -> bool:
        """检查token是否在黑名单中"""
        await self._cleanup()
        return token in self._blacklist
        
    async def _cleanup(self) -> None:
        """清理已过期的token"""
        current_time = datetime.now(timezone.utc)
        to_remove = set()
        
        for token in self._blacklist:
            try:
                payload = decode_access_token(token)
                exp = datetime.fromtimestamp(payload["exp"], timezone.utc)
                if current_time >= exp:
                    to_remove.add(token)
            except jwt.InvalidTokenError:
                to_remove.add(token)
                
        self._blacklist -= to_remove

# 全局token黑名单实例
token_blacklist = TokenBlacklist()

def decode_access_token(token: str) -> Dict[str, Any]:
    """
    解码并验证 JWT token
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        # 检查过期
        exp = payload.get("exp")
        if exp is not None:
            now = datetime.now(timezone.utc).timestamp()
            if now > exp:
                raise jwt.ExpiredSignatureError("Token已过期")
        # 检查必要字段
        for field in ["user_id", "username", "user_type"]:
            if field not in payload:
                raise jwt.InvalidTokenError(f"缺少字段: {field}")
        return payload
    except jwt.ExpiredSignatureError:
        raise
    except Exception as e:
        raise jwt.InvalidTokenError(f"Token无效: {e}")
