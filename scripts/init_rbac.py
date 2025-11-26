"""
初始化 RBAC 权限数据

创建默认权限和角色
"""

import asyncio

from loguru import logger
from sqlalchemy import select

from app.core.database import get_db
from app.core.permissions import get_all_permissions
from app.models.permission import Permission
from app.models.role import Role


async def init_permissions() -> list[Permission]:
    """初始化所有权限"""
    permissions_data = get_all_permissions()
    created_permissions = []

    async for db in get_db():
        for perm_data in permissions_data:
            # 检查权限是否已存在
            result = await db.execute(select(Permission).where(Permission.code == perm_data["code"], Permission.deleted == 0))
            existing = result.scalar_one_or_none()

            if existing:
                logger.info(f"  权限已存在: {perm_data['code']}")
                created_permissions.append(existing)
            else:
                permission = Permission(
                    code=perm_data["code"],
                    name=perm_data["name"],
                    module=perm_data["module"],
                    description=perm_data.get("description"),
                )
                db.add(permission)
                created_permissions.append(permission)
                logger.info(f"  ✅ 创建权限: {perm_data['code']}")

        await db.commit()

        # 刷新以获取 ID
        for perm in created_permissions:
            await db.refresh(perm)

        return created_permissions

    return []


async def init_admin_role(permissions: list[Permission]) -> Role:
    """初始化管理员角色（拥有所有权限）"""
    async for db in get_db():
        # 检查 admin 角色是否已存在
        result = await db.execute(select(Role).where(Role.code == "admin", Role.deleted == 0))
        admin_role = result.scalar_one_or_none()

        if admin_role:
            logger.info("  管理员角色已存在，更新权限...")
            # 更新权限
            admin_role.permissions = permissions
        else:
            admin_role = Role(
                code="admin",
                name="管理员",
                description="系统管理员，拥有所有权限",
                permissions=permissions,
            )
            db.add(admin_role)
            logger.info("  ✅ 创建管理员角色")

        await db.commit()
        await db.refresh(admin_role)
        return admin_role

    raise RuntimeError("无法初始化管理员角色")


async def init_default_roles(permissions: list[Permission]) -> list[Role]:
    """初始化默认角色"""
    # 权限映射：按 code 索引
    perm_map = {p.code: p for p in permissions}

    # 定义默认角色及其权限
    default_roles = [
        {
            "code": "user_manager",
            "name": "用户管理员",
            "description": "负责用户管理，拥有用户相关的所有权限",
            "permissions": ["user:read", "user:create", "user:update", "user:delete"],
        },
        {
            "code": "viewer",
            "name": "只读用户",
            "description": "只能查看数据，没有修改权限",
            "permissions": ["user:read", "role:read", "permission:read"],
        },
    ]

    created_roles = []
    async for db in get_db():
        for role_data in default_roles:
            # 检查角色是否已存在
            result = await db.execute(select(Role).where(Role.code == role_data["code"], Role.deleted == 0))
            existing_role = result.scalar_one_or_none()

            role_permissions = [perm_map[code] for code in role_data["permissions"] if code in perm_map]

            if existing_role:
                logger.info(f"  角色已存在: {role_data['code']}，更新权限...")
                existing_role.permissions = role_permissions
                created_roles.append(existing_role)
            else:
                role = Role(
                    code=role_data["code"],
                    name=role_data["name"],
                    description=role_data["description"],
                    permissions=role_permissions,
                )
                db.add(role)
                created_roles.append(role)
                logger.info(f"  ✅ 创建角色: {role_data['code']}")

        await db.commit()
        return created_roles

    return []


async def main():
    """主函数"""
    logger.info("🔐 开始初始化 RBAC 权限数据...")

    try:
        # 1. 初始化权限
        logger.info("\n📋 初始化权限...")
        permissions = await init_permissions()
        logger.info(f"   共 {len(permissions)} 个权限")

        # 2. 初始化管理员角色
        logger.info("\n👑 初始化管理员角色...")
        await init_admin_role(permissions)

        # 3. 初始化默认角色
        logger.info("\n👥 初始化默认角色...")
        await init_default_roles(permissions)

        logger.info("\n✅ RBAC 权限数据初始化完成！")

    except Exception as e:
        logger.error(f"❌ RBAC 初始化失败: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())

