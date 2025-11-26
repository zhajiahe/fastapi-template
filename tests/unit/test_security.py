"""
安全模块单元测试

测试密码哈希、JWT 令牌等安全功能
"""

import pytest

from app.core.security import (
    create_tokens,
    get_password_hash,
    get_token_hash,
    verify_access_token,
    verify_password,
    verify_refresh_token,
)


class TestPasswordHashing:
    """密码哈希测试类"""

    @pytest.mark.unit
    def test_password_hash_generation(self):
        """测试密码哈希生成"""
        password = "test_password_123"
        hashed = get_password_hash(password)

        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 0

    @pytest.mark.unit
    def test_password_verification_success(self):
        """测试密码验证成功"""
        password = "test_password_123"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    @pytest.mark.unit
    def test_password_verification_failure(self):
        """测试密码验证失败"""
        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False

    @pytest.mark.unit
    def test_different_passwords_different_hashes(self):
        """测试不同密码产生不同哈希"""
        password1 = "password1"
        password2 = "password2"

        hash1 = get_password_hash(password1)
        hash2 = get_password_hash(password2)

        assert hash1 != hash2

    @pytest.mark.unit
    def test_same_password_different_hashes(self):
        """测试相同密码产生不同哈希（盐值不同）"""
        password = "same_password"

        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        # 由于盐值不同，哈希值应该不同
        assert hash1 != hash2
        # 但两个哈希都应该能验证原密码
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestJWTTokens:
    """JWT 令牌测试类"""

    @pytest.mark.unit
    def test_create_tokens(self):
        """测试令牌创建"""
        user_data = {"user_id": 1}
        access_token, refresh_token = create_tokens(user_data)

        assert access_token is not None
        assert refresh_token is not None
        assert access_token != refresh_token
        assert len(access_token) > 0
        assert len(refresh_token) > 0

    @pytest.mark.unit
    def test_verify_access_token_success(self):
        """测试访问令牌验证成功"""
        user_id = 123
        access_token, _ = create_tokens({"user_id": user_id})

        class MockException(Exception):
            pass

        result = verify_access_token(access_token, MockException())
        assert result == user_id

    @pytest.mark.unit
    def test_verify_access_token_invalid(self):
        """测试无效访问令牌"""

        class MockException(Exception):
            pass

        with pytest.raises(MockException):
            verify_access_token("invalid_token", MockException())

    @pytest.mark.unit
    def test_verify_refresh_token_success(self):
        """测试刷新令牌验证成功"""
        user_id = 456
        _, refresh_token = create_tokens({"user_id": user_id})

        class MockException(Exception):
            pass

        result = verify_refresh_token(refresh_token, MockException())
        assert result == user_id

    @pytest.mark.unit
    def test_verify_refresh_token_invalid(self):
        """测试无效刷新令牌"""

        class MockException(Exception):
            pass

        with pytest.raises(MockException):
            verify_refresh_token("invalid_token", MockException())

    @pytest.mark.unit
    def test_access_token_cannot_be_used_as_refresh(self):
        """测试访问令牌不能作为刷新令牌使用"""
        access_token, _ = create_tokens({"user_id": 1})

        class MockException(Exception):
            pass

        with pytest.raises(MockException):
            verify_refresh_token(access_token, MockException())

    @pytest.mark.unit
    def test_refresh_token_cannot_be_used_as_access(self):
        """测试刷新令牌不能作为访问令牌使用"""
        _, refresh_token = create_tokens({"user_id": 1})

        class MockException(Exception):
            pass

        with pytest.raises(MockException):
            verify_access_token(refresh_token, MockException())


class TestTokenHash:
    """令牌哈希测试类"""

    @pytest.mark.unit
    def test_token_hash_generation(self):
        """测试令牌哈希生成"""
        token = "sample_token_12345"
        hashed = get_token_hash(token)

        assert hashed is not None
        assert len(hashed) == 64  # SHA256 哈希长度

    @pytest.mark.unit
    def test_same_token_same_hash(self):
        """测试相同令牌产生相同哈希"""
        token = "sample_token"
        hash1 = get_token_hash(token)
        hash2 = get_token_hash(token)

        assert hash1 == hash2

    @pytest.mark.unit
    def test_different_tokens_different_hashes(self):
        """测试不同令牌产生不同哈希"""
        token1 = "token1"
        token2 = "token2"

        hash1 = get_token_hash(token1)
        hash2 = get_token_hash(token2)

        assert hash1 != hash2
