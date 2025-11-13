"""
用户管理API路由

提供用户的CRUD操作
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.base import BasePageQuery, BaseResponse, PageResponse
from app.models.user import User
from app.schemas.user import UserCreate, UserListQuery, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=BaseResponse[PageResponse[UserResponse]])
async def get_users(
    page_query: BasePageQuery = Depends(),
    query_params: UserListQuery = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    获取用户列表（分页）

    Args:
        page_query: 分页参数（page_num, page_size）
        query_params: 查询参数（keyword, is_active, is_superuser）
        db: 数据库会话
    """
    # 构建查询条件
    query = select(User).where(User.deleted == 0)

    # 关键词搜索
    if query_params.keyword:
        keyword = query_params.keyword
        query = query.where(
            (User.username.like(f"%{keyword}%"))
            | (User.email.like(f"%{keyword}%"))
            | (User.nickname.like(f"%{keyword}%"))
        )

    # 激活状态过滤
    if query_params.is_active is not None:
        query = query.where(User.is_active == query_params.is_active)

    # 超级管理员过滤
    if query_params.is_superuser is not None:
        query = query.where(User.is_superuser == query_params.is_superuser)

    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # 分页查询
    query = query.order_by(User.create_time.desc()).limit(page_query.limit).offset(page_query.offset)

    result = await db.execute(query)
    users = result.scalars().all()

    # 转换为响应模型
    user_list = [UserResponse.model_validate(user) for user in users]

    return BaseResponse(
        success=True,
        code=200,
        msg="获取用户列表成功",
        data=PageResponse(
            page_num=page_query.page_num,
            page_size=page_query.page_size,
            total=total,
            items=user_list,
        ),
    )


@router.get("/{user_id}", response_model=BaseResponse[UserResponse])
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

    return BaseResponse(
        success=True,
        code=200,
        msg="获取用户成功",
        data=UserResponse.model_validate(user),
    )


@router.post("", response_model=BaseResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    创建新用户

    Args:
        user_data: 用户创建数据
        db: 数据库会话
    """
    # 检查用户名是否已存在
    result = await db.execute(select(User).where(User.username == user_data.username, User.deleted == 0))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")

    # 检查邮箱是否已存在
    result = await db.execute(select(User).where(User.email == user_data.email, User.deleted == 0))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已存在")

    # 创建用户（使用密码哈希）
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        nickname=user_data.nickname,
        hashed_password=get_password_hash(user_data.password),
        is_active=user_data.is_active,
        is_superuser=user_data.is_superuser,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return BaseResponse(
        success=True,
        code=201,
        msg="创建用户成功",
        data=UserResponse.model_validate(new_user),
    )


@router.put("/{user_id}", response_model=BaseResponse[UserResponse])
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    更新用户信息

    Args:
        user_id: 用户ID
        user_data: 用户更新数据
        db: 数据库会话
    """
    result = await db.execute(select(User).where(User.id == user_id, User.deleted == 0))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    # 更新字段
    if user_data.email is not None:
        # 检查邮箱是否已被其他用户使用
        result = await db.execute(
            select(User).where(User.email == user_data.email, User.id != user_id, User.deleted == 0)
        )
        if result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已被使用")
        user.email = user_data.email

    if user_data.nickname is not None:
        user.nickname = user_data.nickname

    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    if user_data.is_superuser is not None:
        user.is_superuser = user_data.is_superuser

    await db.commit()
    await db.refresh(user)

    return BaseResponse(
        success=True,
        code=200,
        msg="更新用户成功",
        data=UserResponse.model_validate(user),
    )


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
