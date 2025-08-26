import jwt

from app.schemas.system.login import TokenData
from app.settings.config import settings


def create_access_token(*, data: TokenData):
    payload = data.model_dump().copy()
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
