"""
角色模型

定义系统角色
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, BaseTableMixin

if TYPE_CHECKING:
    from app.models.permission import Permission
    from app.models.user import User

# 角色-权限关联表
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)

# 用户-角色关联表
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)


class Role(Base, BaseTableMixin):
    """角色表模型"""

    __tablename__ = "roles"

    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True, comment="角色代码")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="角色名称")
    description: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="角色描述")

    # 关联权限 - 使用 lazy="selectin" 自动急切加载
    permissions: Mapped[list[Permission]] = relationship(  # noqa: F821
        "Permission",
        secondary=role_permissions,
        back_populates="roles",
        lazy="selectin",
    )

    # 关联用户
    users: Mapped[list[User]] = relationship(  # noqa: F821
        "User",
        secondary=user_roles,
        back_populates="roles",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Role(code={self.code}, name={self.name})>"

    def get_all_permissions(self) -> set[str]:
        """
        获取角色的所有权限

        Returns:
            权限代码集合
        """
        return {p.code for p in self.permissions}
