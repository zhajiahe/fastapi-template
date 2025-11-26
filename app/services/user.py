"""
用户服务

处理用户管理相关的业务逻辑
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestException, NotFoundException
from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserListQuery, UserUpdate


class UserService:
    """用户服务类"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)

    async def get_user(self, user_id: int) -> User:
        """获取单个用户"""
        user = await self.user_repo.get_by_id_with_roles(user_id)
        if not user:
            raise NotFoundException(msg="用户不存在")
        return user

    async def get_users(
        self,
        query_params: UserListQuery,
        page_num: int = 1,
        page_size: int = 10,
    ) -> tuple[list[User], int]:
        """获取用户列表"""
        skip = (page_num - 1) * page_size
        return await self.user_repo.search(
            keyword=query_params.keyword,
            is_active=query_params.is_active,
            skip=skip,
            limit=page_size,
        )

    async def create_user(self, user_data: UserCreate) -> User:
        """创建用户"""
        # 检查用户名是否已存在
        if await self.user_repo.username_exists(user_data.username):
            raise BadRequestException(msg="用户名已存在")

        # 检查邮箱是否已存在
        if await self.user_repo.email_exists(user_data.email):
            raise BadRequestException(msg="邮箱已存在")

        # 获取角色
        roles = await self.role_repo.get_by_ids(user_data.role_ids) if user_data.role_ids else []

        # 创建用户
        user = User(
            username=user_data.username,
            email=user_data.email,
            nickname=user_data.nickname,
            hashed_password=get_password_hash(user_data.password),
            is_active=user_data.is_active,
        )
        user.roles = roles

        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)

        return user

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """更新用户"""
        user = await self.user_repo.get_by_id_with_roles(user_id)
        if not user:
            raise NotFoundException(msg="用户不存在")

        # 检查邮箱是否已被其他用户使用
        if user_data.email is not None:
            if await self.user_repo.email_exists(user_data.email, exclude_id=user_id):
                raise BadRequestException(msg="邮箱已被使用")

        # 更新角色
        if user_data.role_ids is not None:
            roles = await self.role_repo.get_by_ids(user_data.role_ids)
            user.roles = roles

        # 更新其他字段
        if user_data.email is not None:
            user.email = user_data.email
        if user_data.nickname is not None:
            user.nickname = user_data.nickname
        if user_data.is_active is not None:
            user.is_active = user_data.is_active

        await self.db.flush()
        await self.db.refresh(user)

        return user

    async def update_current_user(self, user: User, user_data: UserUpdate) -> User:
        """更新当前用户信息（只允许更新邮箱和昵称）"""
        # 检查邮箱是否已被其他用户使用
        if user_data.email is not None:
            if await self.user_repo.email_exists(user_data.email, exclude_id=user.id):
                raise BadRequestException(msg="邮箱已被使用")
            user.email = user_data.email

        if user_data.nickname is not None:
            user.nickname = user_data.nickname

        await self.db.flush()
        await self.db.refresh(user)

        return user

    async def delete_user(self, user_id: int) -> None:
        """删除用户（逻辑删除）"""
        success = await self.user_repo.delete(user_id, soft_delete=True)
        if not success:
            raise NotFoundException(msg="用户不存在")
