"""
角色模型

定义系统角色和角色层级
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, BaseTableMixin

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

    # 父角色ID（用于角色继承）
    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("roles.id", ondelete="SET NULL"), nullable=True, comment="父角色ID"
    )

    # 角色层级关系
    parent: Mapped["Role | None"] = relationship("Role", remote_side="Role.id", back_populates="children")
    children: Mapped[list["Role"]] = relationship("Role", back_populates="parent")

    # 关联权限
    permissions: Mapped[list["Permission"]] = relationship(  # noqa: F821
        "Permission",
        secondary=role_permissions,
        back_populates="roles",
    )

    # 关联用户
    users: Mapped[list["User"]] = relationship(  # noqa: F821
        "User",
        secondary=user_roles,
        back_populates="roles",
    )

    def __repr__(self) -> str:
        return f"<Role(code={self.code}, name={self.name})>"

    def get_all_permissions(self) -> set[str]:
        """
        获取角色的所有权限（包括继承的权限）

        Returns:
            权限代码集合
        """
        permissions = {p.code for p in self.permissions}

        # 递归获取父角色的权限
        if self.parent:
            permissions.update(self.parent.get_all_permissions())

        return permissions

