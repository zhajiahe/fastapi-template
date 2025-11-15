"""
创建测试管理员用户

用于性能测试的非交互式创建admin用户
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.user import User


async def create_test_admin():
    """创建测试管理员用户"""
    logger.info("👤 创建测试管理员用户")

    username = "admin"
    password = "admin123"
    email = "admin@example.com"
    nickname = "Test Admin"

    # 创建用户
    async with AsyncSessionLocal() as db:
        try:
            # 检查用户名是否已存在
            result = await db.execute(select(User).where(User.username == username, User.deleted == 0))
            existing_user = result.scalar_one_or_none()

            if existing_user:
                logger.info(f"✅ 测试管理员用户 '{username}' 已存在")
                return

            # 创建测试管理员
            test_admin = User(
                username=username,
                email=email,
                nickname=nickname,
                hashed_password=get_password_hash(password),
                is_active=True,
                is_superuser=True,
            )

            db.add(test_admin)
            await db.commit()
            await db.refresh(test_admin)

            logger.info("✅ 测试管理员创建成功！")
            logger.info(f"   用户名: {test_admin.username}")
            logger.info(f"   邮箱: {test_admin.email}")
            logger.info(f"   密码: {password}")

        except Exception as e:
            logger.error(f"❌ 创建测试管理员失败: {e}")
            await db.rollback()
            raise


async def main():
    """主函数"""
    try:
        await create_test_admin()
    except Exception as e:
        logger.error(f"❌ 发生错误: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
