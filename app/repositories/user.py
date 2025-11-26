"""
用户 Repository

封装用户相关的数据库操作
"""

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """用户数据访问层"""

    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_id_with_roles(self, id: int) -> User | None:
        """根据 ID 获取用户（包含角色）"""
        result = await self.db.execute(
            select(User).options(selectinload(User.roles)).where(User.id == id, User.deleted == 0)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        """根据用户名获取用户"""
        result = await self.db.execute(select(User).where(User.username == username, User.deleted == 0))
        return result.scalar_one_or_none()

    async def get_by_username_with_roles(self, username: str) -> User | None:
        """根据用户名获取用户（包含角色和权限）"""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.roles).selectinload("permissions"))
            .where(User.username == username, User.deleted == 0)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """根据邮箱获取用户"""
        result = await self.db.execute(select(User).where(User.email == email, User.deleted == 0))
        return result.scalar_one_or_none()

    async def search(
        self,
        *,
        keyword: str | None = None,
        is_active: bool | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[User], int]:
        """搜索用户（支持关键词、状态过滤和分页）"""
        # 基础查询
        query = select(User).options(selectinload(User.roles)).where(User.deleted == 0)
        count_query = select(User).where(User.deleted == 0)

        # 关键词搜索
        if keyword:
            keyword_filter = or_(
                User.username.like(f"%{keyword}%"),
                User.email.like(f"%{keyword}%"),
                User.nickname.like(f"%{keyword}%"),
            )
            query = query.where(keyword_filter)
            count_query = count_query.where(keyword_filter)

        # 激活状态过滤
        if is_active is not None:
            query = query.where(User.is_active == is_active)
            count_query = count_query.where(User.is_active == is_active)

        # 获取总数
        count_result = await self.db.execute(select(func.count()).select_from(count_query.subquery()))
        total = count_result.scalar() or 0

        # 分页查询
        query = query.order_by(User.create_time.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        users = list(result.scalars().all())

        return users, total

    async def username_exists(self, username: str, exclude_id: int | None = None) -> bool:
        """检查用户名是否已存在"""
        query = select(User).where(User.username == username, User.deleted == 0)
        if exclude_id:
            query = query.where(User.id != exclude_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    async def email_exists(self, email: str, exclude_id: int | None = None) -> bool:
        """检查邮箱是否已存在"""
        query = select(User).where(User.email == email, User.deleted == 0)
        if exclude_id:
            query = query.where(User.id != exclude_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None
