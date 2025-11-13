"""
用户管理API路由

提供用户的CRUD操作示例
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.base import BaseResponse, PageResponse
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=BaseResponse[PageResponse[dict]])
async def get_users(
    page_num: int = 1,
    page_size: int = 10,
    keyword: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """
    获取用户列表（分页）

    Args:
        page_num: 页码，从1开始
        page_size: 每页数量
        keyword: 搜索关键词（用户名或邮箱）
        db: 数据库会话
    """
    # 构建查询条件
    query = select(User).where(User.deleted == 0)

    # 关键词搜索
    if keyword:
        query = query.where(
            (User.username.like(f"%{keyword}%"))
            | (User.email.like(f"%{keyword}%"))
            | (User.nickname.like(f"%{keyword}%"))
        )

    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # 分页查询
    query = query.order_by(User.create_time.desc()).limit(page_size).offset((page_num - 1) * page_size)

    result = await db.execute(query)
    users = result.scalars().all()

    # 转换为字典（不包含密码）
    user_list = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "nickname": user.nickname,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "create_time": user.create_time.isoformat() if user.create_time else None,
            "update_time": user.update_time.isoformat() if user.update_time else None,
        }
        for user in users
    ]

    return BaseResponse(
        success=True,
        code=200,
        msg="获取用户列表成功",
        data=PageResponse(page_num=page_num, page_size=page_size, total=total, items=user_list),
    )


@router.get("/{user_id}", response_model=BaseResponse[dict])
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    获取单个用户详情

    Args:
        user_id: 用户ID
        db: 数据库会话
    """
    result = await db.execute(select(User).where(User.id == user_id, User.deleted == 0))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "nickname": user.nickname,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "create_time": user.create_time.isoformat() if user.create_time else None,
        "update_time": user.update_time.isoformat() if user.update_time else None,
    }

    return BaseResponse(success=True, code=200, msg="获取用户成功", data=user_data)


@router.post("", response_model=BaseResponse[dict], status_code=status.HTTP_201_CREATED)
async def create_user(
    username: str,
    email: str,
    nickname: str,
    password: str,
    is_active: bool = True,
    is_superuser: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """
    创建新用户

    Args:
        username: 用户名
        email: 邮箱
        nickname: 昵称
        password: 密码（实际应用中应该加密）
        is_active: 是否激活
        is_superuser: 是否超级管理员
        db: 数据库会话
    """
    # 检查用户名是否已存在
    result = await db.execute(select(User).where(User.username == username, User.deleted == 0))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")

    # 检查邮箱是否已存在
    result = await db.execute(select(User).where(User.email == email, User.deleted == 0))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已存在")

    # 创建用户（实际应用中应该使用密码哈希）
    new_user = User(
        username=username,
        email=email,
        nickname=nickname,
        hashed_password=password,  # 实际应该使用 hash_password(password)
        is_active=is_active,
        is_superuser=is_superuser,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    user_data = {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "nickname": new_user.nickname,
        "is_active": new_user.is_active,
        "is_superuser": new_user.is_superuser,
    }

    return BaseResponse(success=True, code=201, msg="创建用户成功", data=user_data)


@router.put("/{user_id}", response_model=BaseResponse[dict])
async def update_user(
    user_id: int,
    email: str | None = None,
    nickname: str | None = None,
    is_active: bool | None = None,
    is_superuser: bool | None = None,
    db: AsyncSession = Depends(get_db),
):
    """
    更新用户信息

    Args:
        user_id: 用户ID
        email: 邮箱
        nickname: 昵称
        is_active: 是否激活
        is_superuser: 是否超级管理员
        db: 数据库会话
    """
    result = await db.execute(select(User).where(User.id == user_id, User.deleted == 0))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    # 更新字段
    if email is not None:
        # 检查邮箱是否已被其他用户使用
        result = await db.execute(select(User).where(User.email == email, User.id != user_id, User.deleted == 0))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已被使用")
        user.email = email

    if nickname is not None:
        user.nickname = nickname

    if is_active is not None:
        user.is_active = is_active

    if is_superuser is not None:
        user.is_superuser = is_superuser

    await db.commit()
    await db.refresh(user)

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "nickname": user.nickname,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "update_time": user.update_time.isoformat() if user.update_time else None,
    }

    return BaseResponse(success=True, code=200, msg="更新用户成功", data=user_data)


@router.delete("/{user_id}", response_model=BaseResponse[None])
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    删除用户（逻辑删除）

    Args:
        user_id: 用户ID
        db: 数据库会话
    """
    result = await db.execute(select(User).where(User.id == user_id, User.deleted == 0))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    # 逻辑删除
    user.deleted = 1
    await db.commit()

    return BaseResponse(success=True, code=200, msg="删除用户成功", data=None)
