"""
角色和权限相关的 Pydantic Schema
"""

from datetime import datetime

from pydantic import BaseModel, Field

# ==================== 权限 Schema ====================


class PermissionBase(BaseModel):
    """权限基础字段"""

    code: str = Field(..., min_length=1, max_length=100, description="权限代码")
    name: str = Field(..., min_length=1, max_length=100, description="权限名称")
    module: str = Field(..., min_length=1, max_length=50, description="所属模块")
    description: str | None = Field(default=None, max_length=255, description="权限描述")


class PermissionCreate(PermissionBase):
    """创建权限请求"""

    pass


class PermissionUpdate(BaseModel):
    """更新权限请求"""

    name: str | None = Field(default=None, min_length=1, max_length=100, description="权限名称")
    module: str | None = Field(default=None, min_length=1, max_length=50, description="所属模块")
    description: str | None = Field(default=None, max_length=255, description="权限描述")


class PermissionResponse(PermissionBase):
    """权限响应"""

    id: int = Field(..., description="权限ID")
    create_time: datetime | None = Field(default=None, description="创建时间")

    model_config = {"from_attributes": True}


# ==================== 角色 Schema ====================


class RoleBase(BaseModel):
    """角色基础字段"""

    code: str = Field(..., min_length=1, max_length=50, description="角色代码")
    name: str = Field(..., min_length=1, max_length=100, description="角色名称")
    description: str | None = Field(default=None, max_length=255, description="角色描述")
    parent_id: int | None = Field(default=None, description="父角色ID")


class RoleCreate(RoleBase):
    """创建角色请求"""

    permission_ids: list[int] = Field(default_factory=list, description="权限ID列表")


class RoleUpdate(BaseModel):
    """更新角色请求"""

    name: str | None = Field(default=None, min_length=1, max_length=100, description="角色名称")
    description: str | None = Field(default=None, max_length=255, description="角色描述")
    parent_id: int | None = Field(default=None, description="父角色ID")
    permission_ids: list[int] | None = Field(default=None, description="权限ID列表")


class RoleResponse(RoleBase):
    """角色响应"""

    id: int = Field(..., description="角色ID")
    create_time: datetime | None = Field(default=None, description="创建时间")
    permissions: list[PermissionResponse] = Field(default_factory=list, description="权限列表")

    model_config = {"from_attributes": True}


class RoleSimpleResponse(BaseModel):
    """角色简单响应（不含权限详情）"""

    id: int = Field(..., description="角色ID")
    code: str = Field(..., description="角色代码")
    name: str = Field(..., description="角色名称")

    model_config = {"from_attributes": True}


# ==================== 用户角色 Schema ====================


class UserRoleAssign(BaseModel):
    """用户角色分配请求"""

    user_id: int = Field(..., description="用户ID")
    role_ids: list[int] = Field(..., description="角色ID列表")


class RolePermissionAssign(BaseModel):
    """角色权限分配请求"""

    role_id: int = Field(..., description="角色ID")
    permission_ids: list[int] = Field(..., description="权限ID列表")

