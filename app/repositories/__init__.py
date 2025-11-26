"""
Repository 层

提供数据访问抽象，封装数据库操作逻辑
"""

from app.repositories.base import BaseRepository
from app.repositories.user import UserRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
]
