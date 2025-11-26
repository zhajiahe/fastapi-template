"""
配置管理模块

使用 Pydantic Settings 管理应用配置，支持从 .env 文件加载配置
"""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # 环境配置
    ENVIRONMENT: Literal["development", "testing", "production"] = "development"

    # JWT 配置
    SECRET_KEY: str = "your-secret-key-here-change-in-production"  # 生产环境必须更改
    REFRESH_SECRET_KEY: str = "your-refresh-secret-key-here-change-in-production"  # 生产环境必须更改
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 访问令牌过期时间（分钟）
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 刷新令牌过期时间（天）

    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

    # 应用配置
    APP_NAME: str = "FastAPI Template"
    DEBUG: bool = True

    # CORS 配置
    ALLOWED_ORIGINS: list[str] = ["*"]

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    @property
    def is_development(self) -> bool:
        """是否为开发环境"""
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        """是否为生产环境"""
        return self.ENVIRONMENT == "production"

    @property
    def is_testing(self) -> bool:
        """是否为测试环境"""
        return self.ENVIRONMENT == "testing"


# 创建全局配置实例
settings = Settings()
