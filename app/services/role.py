"""
角色和权限服务

处理角色和权限相关的业务逻辑
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestException, NotFoundException
from app.models.permission import Permission
from app.models.role import Role
from app.repositories.role import PermissionRepository, RoleRepository
from app.schemas.role import PermissionCreate, PermissionUpdate, RoleCreate, RoleUpdate


class PermissionService:
    """权限服务类"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.permission_repo = PermissionRepository(db)

    async def get_permission(self, permission_id: int) -> Permission:
        """获取单个权限"""
        permission = await self.permission_repo.get_by_id(permission_id)
        if not permission:
            raise NotFoundException(msg="权限不存在")
        return permission

    async def get_permissions(self) -> list[Permission]:
        """获取所有权限"""
        return await self.permission_repo.get_all()

    async def create_permission(self, data: PermissionCreate) -> Permission:
        """创建权限"""
        # 检查权限代码是否已存在
        existing = await self.permission_repo.get_by_code(data.code)
        if existing:
            raise BadRequestException(msg="权限代码已存在")

        permission = await self.permission_repo.create(data.model_dump())
        return permission

    async def update_permission(self, permission_id: int, data: PermissionUpdate) -> Permission:
        """更新权限"""
        permission = await self.permission_repo.get_by_id(permission_id)
        if not permission:
            raise NotFoundException(msg="权限不存在")

        update_data = data.model_dump(exclude_unset=True)
        permission = await self.permission_repo.update(permission, update_data)
        return permission

    async def delete_permission(self, permission_id: int) -> None:
        """删除权限"""
        success = await self.permission_repo.delete(permission_id)
        if not success:
            raise NotFoundException(msg="权限不存在")


class RoleService:
    """角色服务类"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.role_repo = RoleRepository(db)
        self.permission_repo = PermissionRepository(db)

    async def get_role(self, role_id: int) -> Role:
        """获取单个角色"""
        role = await self.role_repo.get_by_id_with_permissions(role_id)
        if not role:
            raise NotFoundException(msg="角色不存在")
        return role

    async def get_roles(self) -> list[Role]:
        """获取所有角色"""
        return await self.role_repo.get_all_with_permissions()

    async def create_role(self, data: RoleCreate) -> Role:
        """创建角色"""
        # 检查角色代码是否已存在
        if await self.role_repo.code_exists(data.code):
            raise BadRequestException(msg="角色代码已存在")

        # 获取权限
        permissions = await self.permission_repo.get_by_ids(data.permission_ids)

        # 创建角色
        role_data = data.model_dump(exclude={"permission_ids"})
        role = Role(**role_data)
        role.permissions = permissions

        self.db.add(role)
        await self.db.flush()
        await self.db.refresh(role)

        return role

    async def update_role(self, role_id: int, data: RoleUpdate) -> Role:
        """更新角色"""
        role = await self.role_repo.get_by_id_with_permissions(role_id)
        if not role:
            raise NotFoundException(msg="角色不存在")

        # 更新权限
        if data.permission_ids is not None:
            permissions = await self.permission_repo.get_by_ids(data.permission_ids)
            role.permissions = permissions

        # 更新其他字段
        update_data = data.model_dump(exclude={"permission_ids"}, exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(role, field):
                setattr(role, field, value)

        await self.db.flush()
        await self.db.refresh(role)

        return role

    async def delete_role(self, role_id: int) -> None:
        """删除角色"""
        role = await self.role_repo.get_by_id_with_permissions(role_id)
        if not role:
            raise NotFoundException(msg="角色不存在")

        success = await self.role_repo.delete(role_id)
        if not success:
            raise NotFoundException(msg="角色不存在")
