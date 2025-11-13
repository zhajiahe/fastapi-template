"""
pytest 全局配置文件
定义全局 fixtures 和配置
"""

import os
from collections.abc import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.models.base import Base

try:
    from app.main import app  # type: ignore[attr-defined]
except (ImportError, AttributeError):
    from fastapi import FastAPI

    app = FastAPI()

# ============ 数据库配置 ============

# 使用内存数据库进行测试
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # 使用静态连接池，确保所有测试使用同一个内存数据库
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ============ Pytest 配置 ============


def pytest_configure(config):
    """pytest 启动时的配置"""
    # 设置测试环境变量
    os.environ["TESTING"] = "1"
    os.environ["DATABASE_URL"] = SQLALCHEMY_DATABASE_URL


# ============ 数据库 Fixtures ============


@pytest.fixture(scope="session")
def db_engine():
    """
    创建测试数据库引擎（整个测试会话只创建一次）
    """
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db(db_engine) -> Generator[Session, None, None]:
    """
    创建数据库会话（每个测试函数都会创建新的会话）
    测试结束后自动回滚
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def override_get_db(db: Session):
    """
    覆盖应用的数据库依赖
    """

    def _override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


# ============ 客户端 Fixtures ============


@pytest.fixture(scope="function")
def client(override_get_db) -> Generator[TestClient, None, None]:
    """
    同步测试客户端
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
async def async_client(override_get_db) -> AsyncGenerator[AsyncClient, None]:
    """
    异步测试客户端
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
