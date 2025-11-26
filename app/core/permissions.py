"""
权限码常量定义

定义系统中所有的权限码，统一管理便于维护
命名规范: {模块}:{操作}
"""

from typing import TypedDict


class PermissionDict(TypedDict):
    """权限字典类型"""

    code: str
    name: str
    description: str


class PermissionGroupDict(TypedDict):
    """权限分组字典类型"""

    module: str
    permissions: list[PermissionDict]


class PermissionCode:
    """权限码常量"""

    # ==================== 用户管理权限 ====================
    USER_READ = "user:read"  # 查看用户
    USER_CREATE = "user:create"  # 创建用户
    USER_UPDATE = "user:update"  # 更新用户
    USER_DELETE = "user:delete"  # 删除用户

    # ==================== 角色管理权限 ====================
    ROLE_READ = "role:read"  # 查看角色
    ROLE_CREATE = "role:create"  # 创建角色
    ROLE_UPDATE = "role:update"  # 更新角色
    ROLE_DELETE = "role:delete"  # 删除角色

    # ==================== 权限管理权限 ====================
    PERMISSION_READ = "permission:read"  # 查看权限
    PERMISSION_CREATE = "permission:create"  # 创建权限
    PERMISSION_UPDATE = "permission:update"  # 更新权限
    PERMISSION_DELETE = "permission:delete"  # 删除权限


# 权限分组（用于初始化种子数据）
PERMISSION_GROUPS: dict[str, PermissionGroupDict] = {
    "user": {
        "module": "用户管理",
        "permissions": [
            {"code": PermissionCode.USER_READ, "name": "查看用户", "description": "查看用户列表和用户详情"},
            {"code": PermissionCode.USER_CREATE, "name": "创建用户", "description": "创建新用户"},
            {"code": PermissionCode.USER_UPDATE, "name": "更新用户", "description": "更新用户信息"},
            {"code": PermissionCode.USER_DELETE, "name": "删除用户", "description": "删除用户"},
        ],
    },
    "role": {
        "module": "角色管理",
        "permissions": [
            {"code": PermissionCode.ROLE_READ, "name": "查看角色", "description": "查看角色列表和角色详情"},
            {"code": PermissionCode.ROLE_CREATE, "name": "创建角色", "description": "创建新角色"},
            {"code": PermissionCode.ROLE_UPDATE, "name": "更新角色", "description": "更新角色信息和权限"},
            {"code": PermissionCode.ROLE_DELETE, "name": "删除角色", "description": "删除角色"},
        ],
    },
    "permission": {
        "module": "权限管理",
        "permissions": [
            {"code": PermissionCode.PERMISSION_READ, "name": "查看权限", "description": "查看权限列表和权限详情"},
            {"code": PermissionCode.PERMISSION_CREATE, "name": "创建权限", "description": "创建新权限"},
            {"code": PermissionCode.PERMISSION_UPDATE, "name": "更新权限", "description": "更新权限信息"},
            {"code": PermissionCode.PERMISSION_DELETE, "name": "删除权限", "description": "删除权限"},
        ],
    },
}


def get_all_permissions() -> list[dict[str, str | None]]:
    """获取所有权限的扁平列表，用于初始化"""
    permissions: list[dict[str, str | None]] = []
    for group_key, group in PERMISSION_GROUPS.items():
        for perm in group["permissions"]:
            permissions.append(
                {
                    "code": perm["code"],
                    "name": perm["name"],
                    "description": perm.get("description"),
                    "module": group_key,
                }
            )
    return permissions
