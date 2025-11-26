from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, BaseTableMixin

if TYPE_CHECKING:
    from app.models.role import Role


class User(Base, BaseTableMixin):
    """用户表模型"""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True, comment="用户名")
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True, comment="邮箱")
    nickname: Mapped[str] = mapped_column(String(50), nullable=False, comment="昵称")
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False, comment="加密密码")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, comment="是否激活")

    # 关联角色 - 使用 lazy="selectin" 自动急切加载
    roles: Mapped[list[Role]] = relationship(  # noqa: F821
        "Role",
        secondary="user_roles",
        back_populates="users",
        lazy="selectin",  # 自动急切加载，解决惰性加载问题
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

    def has_permission(self, permission_code: str) -> bool:
        """
        检查用户是否拥有指定权限

        Args:
            permission_code: 权限代码

        Returns:
            是否拥有权限
        """
        for role in self.roles:
            if permission_code in role.get_all_permissions():
                return True
        return False

    def has_role(self, role_code: str) -> bool:
        """
        检查用户是否拥有指定角色

        Args:
            role_code: 角色代码

        Returns:
            是否拥有角色
        """
        return any(role.code == role_code for role in self.roles)

    def get_all_permissions(self) -> set[str]:
        """
        获取用户的所有权限

        Returns:
            权限代码集合
        """
        permissions: set[str] = set()
        for role in self.roles:
            permissions.update(role.get_all_permissions())
        return permissions
