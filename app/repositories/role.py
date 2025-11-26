"""
角色和权限 Repository

封装角色和权限相关的数据库操作
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.permission import Permission
from app.models.role import Role
from app.repositories.base import BaseRepository


class PermissionRepository(BaseRepository[Permission]):
    """权限数据访问层"""

    def __init__(self, db: AsyncSession):
        super().__init__(Permission, db)

    async def get_by_code(self, code: str) -> Permission | None:
        """根据权限代码获取权限"""
        result = await self.db.execute(select(Permission).where(Permission.code == code, Permission.deleted == 0))
        return result.scalar_one_or_none()

    async def get_by_ids(self, ids: list[int]) -> list[Permission]:
        """根据ID列表获取权限"""
        if not ids:
            return []
        result = await self.db.execute(select(Permission).where(Permission.id.in_(ids), Permission.deleted == 0))
        return list(result.scalars().all())

    async def get_by_module(self, module: str) -> list[Permission]:
        """根据模块获取权限列表"""
        result = await self.db.execute(select(Permission).where(Permission.module == module, Permission.deleted == 0))
        return list(result.scalars().all())


class RoleRepository(BaseRepository[Role]):
    """角色数据访问层"""

    def __init__(self, db: AsyncSession):
        super().__init__(Role, db)

    async def get_by_code(self, code: str) -> Role | None:
        """根据角色代码获取角色"""
        result = await self.db.execute(
            select(Role).options(selectinload(Role.permissions)).where(Role.code == code, Role.deleted == 0)
        )
        return result.scalar_one_or_none()

    async def get_by_id_with_permissions(self, id: int) -> Role | None:
        """根据ID获取角色（包含权限）"""
        result = await self.db.execute(
            select(Role).options(selectinload(Role.permissions)).where(Role.id == id, Role.deleted == 0)
        )
        return result.scalar_one_or_none()

    async def get_by_ids(self, ids: list[int]) -> list[Role]:
        """根据ID列表获取角色"""
        if not ids:
            return []
        result = await self.db.execute(
            select(Role).options(selectinload(Role.permissions)).where(Role.id.in_(ids), Role.deleted == 0)
        )
        return list(result.scalars().all())

    async def get_all_with_permissions(self) -> list[Role]:
        """获取所有角色（包含权限）"""
        result = await self.db.execute(
            select(Role)
            .options(selectinload(Role.permissions))
            .where(Role.deleted == 0)
            .order_by(Role.create_time.desc())
        )
        return list(result.scalars().all())

    async def code_exists(self, code: str, exclude_id: int | None = None) -> bool:
        """检查角色代码是否已存在"""
        query = select(Role).where(Role.code == code, Role.deleted == 0)
        if exclude_id:
            query = query.where(Role.id != exclude_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None
