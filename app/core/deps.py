"""
依赖注入模块

提供常用的依赖注入函数，用于路由中获取数据库会话、当前用户等
"""

from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import verify_access_token
from app.models.user import User

# HTTP Bearer 认证方案
security = HTTPBearer()

# 类型别名
DBSession = Annotated[AsyncSession, Depends(get_db)]
TokenCredentials = Annotated[HTTPAuthorizationCredentials, Depends(security)]


async def get_current_user(
    db: DBSession,
    credentials: TokenCredentials,
) -> User:
    """
    获取当前登录用户（包含角色和权限信息）

    Args:
        db: 数据库会话
        credentials: Token 凭证

    Returns:
        User: 当前用户对象

    Raises:
        HTTPException: 认证失败时抛出 401 错误
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="认证失败，请重新登录",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 验证 token 并获取用户ID
    token = credentials.credentials
    user_id = verify_access_token(token, credentials_exception)

    # 从数据库获取用户（包含角色和权限）
    result = await db.execute(
        select(User)
        .options(
            selectinload(User.roles).selectinload("permissions")  # 加载角色和权限
        )
        .where(User.id == user_id, User.deleted == 0)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用",
        )

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    获取当前激活的用户

    Args:
        current_user: 当前用户

    Returns:
        User: 当前用户对象

    Raises:
        HTTPException: 用户未激活时抛出 403 错误
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户未激活",
        )
    return current_user


def require_permission(permission_code: str) -> Callable:
    """
    权限检查依赖工厂

    Args:
        permission_code: 需要的权限代码

    Returns:
        依赖函数

    Usage:
        @router.get("/users")
        async def get_users(user: CurrentUser = Depends(require_permission("user:read"))):
            ...
    """

    async def permission_checker(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        if not current_user.has_permission(permission_code):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"权限不足，需要权限: {permission_code}",
            )
        return current_user

    return permission_checker


def require_role(role_code: str) -> Callable:
    """
    角色检查依赖工厂

    Args:
        role_code: 需要的角色代码

    Returns:
        依赖函数

    Usage:
        @router.get("/admin")
        async def admin_page(user: CurrentUser = Depends(require_role("admin"))):
            ...
    """

    async def role_checker(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        if not current_user.has_role(role_code):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"权限不足，需要角色: {role_code}",
            )
        return current_user

    return role_checker


def require_any_permission(*permission_codes: str) -> Callable:
    """
    任一权限检查依赖工厂

    Args:
        permission_codes: 权限代码列表（满足任一即可）

    Returns:
        依赖函数
    """

    async def permission_checker(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        user_permissions = current_user.get_all_permissions()
        if not any(p in user_permissions for p in permission_codes):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"权限不足，需要权限之一: {', '.join(permission_codes)}",
            )
        return current_user

    return permission_checker


# 类型别名（用于路由中）
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentActiveUser = Annotated[User, Depends(get_current_active_user)]

# 管理员权限检查（替代原来的 is_superuser）
CurrentAdmin = Annotated[User, Depends(require_role("admin"))]
