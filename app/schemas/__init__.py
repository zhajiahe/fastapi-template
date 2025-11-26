"""
Pydantic Schema 模块

用于 API 请求和响应的数据验证和序列化
"""

from app.schemas.role import (
    PermissionCreate,
    PermissionResponse,
    PermissionUpdate,
    RoleCreate,
    RoleResponse,
    RoleSimpleResponse,
    RoleUpdate,
)
from app.schemas.user import (
    LoginRequest,
    PasswordChange,
    RefreshTokenRequest,
    UserCreate,
    UserListQuery,
    UserResponse,
    UserUpdate,
)

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserListQuery",
    "PasswordChange",
    "LoginRequest",
    "RefreshTokenRequest",
    "RoleCreate",
    "RoleUpdate",
    "RoleResponse",
    "RoleSimpleResponse",
    "PermissionCreate",
    "PermissionUpdate",
    "PermissionResponse",
]
