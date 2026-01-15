"""
Token 相关的 Pydantic Schema

用于认证相关的数据验证和序列化
"""

from pydantic import BaseModel


class Token(BaseModel):
    """Token 响应数据"""

    id: int
    nickname: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """JWT Token 载荷数据"""

    exp: int  # 过期时间（Unix时间戳）
    sub: str | None = None
