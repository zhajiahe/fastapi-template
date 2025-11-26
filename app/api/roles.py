"""
角色和权限管理 API 路由

提供角色和权限的 CRUD 操作
"""

from fastapi import APIRouter, status

from app.core.deps import CurrentAdmin, DBSession
from app.models.base import BaseResponse
from app.schemas.role import (
    PermissionCreate,
    PermissionResponse,
    PermissionUpdate,
    RoleCreate,
    RoleResponse,
    RoleUpdate,
)
from app.services.role import PermissionService, RoleService

router = APIRouter(prefix="/roles", tags=["roles"])
permission_router = APIRouter(prefix="/permissions", tags=["permissions"])


# ==================== 角色管理接口 ====================


@router.get("", response_model=BaseResponse[list[RoleResponse]])
async def get_roles(db: DBSession, _user: CurrentAdmin):
    """获取所有角色"""
    role_service = RoleService(db)
    roles = await role_service.get_roles()
    return BaseResponse(
        success=True,
        code=200,
        msg="获取角色列表成功",
        data=[RoleResponse.model_validate(r) for r in roles],
    )


@router.get("/{role_id}", response_model=BaseResponse[RoleResponse])
async def get_role(role_id: int, db: DBSession, _user: CurrentAdmin):
    """获取单个角色详情"""
    role_service = RoleService(db)
    role = await role_service.get_role(role_id)
    return BaseResponse(success=True, code=200, msg="获取角色成功", data=RoleResponse.model_validate(role))


@router.post("", response_model=BaseResponse[RoleResponse], status_code=status.HTTP_201_CREATED)
async def create_role(role_data: RoleCreate, db: DBSession, _user: CurrentAdmin):
    """创建新角色"""
    role_service = RoleService(db)
    role = await role_service.create_role(role_data)
    return BaseResponse(success=True, code=201, msg="创建角色成功", data=RoleResponse.model_validate(role))


@router.put("/{role_id}", response_model=BaseResponse[RoleResponse])
async def update_role(role_id: int, role_data: RoleUpdate, db: DBSession, _user: CurrentAdmin):
    """更新角色"""
    role_service = RoleService(db)
    role = await role_service.update_role(role_id, role_data)
    return BaseResponse(success=True, code=200, msg="更新角色成功", data=RoleResponse.model_validate(role))


@router.delete("/{role_id}", response_model=BaseResponse[None])
async def delete_role(role_id: int, db: DBSession, _user: CurrentAdmin):
    """删除角色"""
    role_service = RoleService(db)
    await role_service.delete_role(role_id)
    return BaseResponse(success=True, code=200, msg="删除角色成功", data=None)


# ==================== 权限管理接口 ====================


@permission_router.get("", response_model=BaseResponse[list[PermissionResponse]])
async def get_permissions(db: DBSession, _user: CurrentAdmin):
    """获取所有权限"""
    permission_service = PermissionService(db)
    permissions = await permission_service.get_permissions()
    return BaseResponse(
        success=True,
        code=200,
        msg="获取权限列表成功",
        data=[PermissionResponse.model_validate(p) for p in permissions],
    )


@permission_router.get("/{permission_id}", response_model=BaseResponse[PermissionResponse])
async def get_permission(permission_id: int, db: DBSession, _user: CurrentAdmin):
    """获取单个权限详情"""
    permission_service = PermissionService(db)
    permission = await permission_service.get_permission(permission_id)
    return BaseResponse(
        success=True, code=200, msg="获取权限成功", data=PermissionResponse.model_validate(permission)
    )


@permission_router.post("", response_model=BaseResponse[PermissionResponse], status_code=status.HTTP_201_CREATED)
async def create_permission(permission_data: PermissionCreate, db: DBSession, _user: CurrentAdmin):
    """创建新权限"""
    permission_service = PermissionService(db)
    permission = await permission_service.create_permission(permission_data)
    return BaseResponse(
        success=True, code=201, msg="创建权限成功", data=PermissionResponse.model_validate(permission)
    )


@permission_router.put("/{permission_id}", response_model=BaseResponse[PermissionResponse])
async def update_permission(permission_id: int, permission_data: PermissionUpdate, db: DBSession, _user: CurrentAdmin):
    """更新权限"""
    permission_service = PermissionService(db)
    permission = await permission_service.update_permission(permission_id, permission_data)
    return BaseResponse(
        success=True, code=200, msg="更新权限成功", data=PermissionResponse.model_validate(permission)
    )


@permission_router.delete("/{permission_id}", response_model=BaseResponse[None])
async def delete_permission(permission_id: int, db: DBSession, _user: CurrentAdmin):
    """删除权限"""
    permission_service = PermissionService(db)
    await permission_service.delete_permission(permission_id)
    return BaseResponse(success=True, code=200, msg="删除权限成功", data=None)

