"""
Schema 单元测试

测试 Pydantic 模型的验证逻辑
"""

import pytest
from pydantic import ValidationError

from app.schemas.user import LoginRequest, PasswordChange, UserCreate, UserUpdate


class TestUserCreateSchema:
    """用户创建 Schema 测试类"""

    @pytest.mark.unit
    def test_valid_user_create(self):
        """测试有效的用户创建数据"""
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            nickname="Test User",
            password="password123",
        )
        assert user_data.username == "testuser"
        assert user_data.email == "test@example.com"
        assert user_data.nickname == "Test User"
        assert user_data.password == "password123"
        assert user_data.is_active is True
        assert user_data.is_superuser is False

    @pytest.mark.unit
    def test_username_too_short(self):
        """测试用户名太短"""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="ab",  # 太短
                email="test@example.com",
                nickname="Test",
                password="password123",
            )
        assert "username" in str(exc_info.value)

    @pytest.mark.unit
    def test_username_too_long(self):
        """测试用户名太长"""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="a" * 51,  # 太长
                email="test@example.com",
                nickname="Test",
                password="password123",
            )
        assert "username" in str(exc_info.value)

    @pytest.mark.unit
    def test_invalid_email(self):
        """测试无效邮箱"""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="testuser",
                email="invalid-email",  # 无效邮箱
                nickname="Test",
                password="password123",
            )
        assert "email" in str(exc_info.value)

    @pytest.mark.unit
    def test_password_too_short(self):
        """测试密码太短"""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="testuser",
                email="test@example.com",
                nickname="Test",
                password="12345",  # 太短
            )
        assert "password" in str(exc_info.value)


class TestUserUpdateSchema:
    """用户更新 Schema 测试类"""

    @pytest.mark.unit
    def test_valid_partial_update(self):
        """测试有效的部分更新"""
        update_data = UserUpdate(nickname="New Nickname")
        assert update_data.nickname == "New Nickname"
        assert update_data.email is None
        assert update_data.is_active is None

    @pytest.mark.unit
    def test_all_fields_update(self):
        """测试所有字段更新"""
        update_data = UserUpdate(
            email="new@example.com",
            nickname="New Name",
            is_active=False,
            is_superuser=True,
        )
        assert update_data.email == "new@example.com"
        assert update_data.nickname == "New Name"
        assert update_data.is_active is False
        assert update_data.is_superuser is True

    @pytest.mark.unit
    def test_empty_update(self):
        """测试空更新"""
        update_data = UserUpdate()
        assert update_data.email is None
        assert update_data.nickname is None


class TestLoginRequestSchema:
    """登录请求 Schema 测试类"""

    @pytest.mark.unit
    def test_valid_login_request(self):
        """测试有效的登录请求"""
        login_data = LoginRequest(
            username="testuser",
            password="password123",
        )
        assert login_data.username == "testuser"
        assert login_data.password == "password123"

    @pytest.mark.unit
    def test_username_too_short(self):
        """测试用户名太短"""
        with pytest.raises(ValidationError):
            LoginRequest(
                username="ab",
                password="password123",
            )

    @pytest.mark.unit
    def test_password_too_short(self):
        """测试密码太短"""
        with pytest.raises(ValidationError):
            LoginRequest(
                username="testuser",
                password="12345",
            )


class TestPasswordChangeSchema:
    """密码修改 Schema 测试类"""

    @pytest.mark.unit
    def test_valid_password_change(self):
        """测试有效的密码修改"""
        pwd_data = PasswordChange(
            old_password="old_password",
            new_password="new_password",
        )
        assert pwd_data.old_password == "old_password"
        assert pwd_data.new_password == "new_password"

    @pytest.mark.unit
    def test_new_password_too_short(self):
        """测试新密码太短"""
        with pytest.raises(ValidationError):
            PasswordChange(
                old_password="old_password",
                new_password="12345",
            )

    @pytest.mark.unit
    def test_old_password_too_short(self):
        """测试旧密码太短"""
        with pytest.raises(ValidationError):
            PasswordChange(
                old_password="12345",
                new_password="new_password",
            )
