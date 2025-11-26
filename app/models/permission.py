"""
权限模型

定义系统权限
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, BaseTableMixin

if TYPE_CHECKING:
    from app.models.role import Role


class Permission(Base, BaseTableMixin):
    """权限表模型"""

    __tablename__ = "permissions"

    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True, comment="权限代码")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="权限名称")
    module: Mapped[str] = mapped_column(String(50), nullable=False, comment="所属模块")
    description: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="权限描述")

    # 关联角色 - 使用 lazy="selectin" 自动急切加载
    roles: Mapped[list[Role]] = relationship(  # noqa: F821
        "Role",
        secondary="role_permissions",
        back_populates="permissions",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Permission(code={self.code}, name={self.name})>"
