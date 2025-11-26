"""
角色和权限 API 集成测试

测试 RBAC 功能
"""

from fastapi import status
from fastapi.testclient import TestClient


class TestPermissionAPI:
    """权限管理 API 测试类"""

    def test_create_permission(self, client: TestClient, auth_headers: dict):
        """测试创建权限"""
        response = client.post(
            "/api/v1/permissions",
            json={
                "code": "test:custom",
                "name": "自定义权限",
                "module": "test",
                "description": "测试用自定义权限",
            },
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["success"] is True
        assert data["data"]["code"] == "test:custom"
        assert data["data"]["name"] == "自定义权限"
        assert data["data"]["module"] == "test"

    def test_create_permission_duplicate_code(self, client: TestClient, auth_headers: dict):
        """测试创建重复权限代码"""
        # 第一次创建
        client.post(
            "/api/v1/permissions",
            json={"code": "dup:perm", "name": "重复权限", "module": "test"},
            headers=auth_headers,
        )
        # 第二次创建相同 code
        response = client.post(
            "/api/v1/permissions",
            json={"code": "dup:perm", "name": "另一个权限", "module": "test"},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "已存在" in response.json()["msg"]

    def test_get_permissions(self, client: TestClient, auth_headers: dict):
        """测试获取权限列表"""
        # 创建测试权限
        client.post(
            "/api/v1/permissions",
            json={"code": "list:perm1", "name": "权限1", "module": "test"},
            headers=auth_headers,
        )
        client.post(
            "/api/v1/permissions",
            json={"code": "list:perm2", "name": "权限2", "module": "test"},
            headers=auth_headers,
        )

        response = client.get("/api/v1/permissions", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 2

    def test_get_permission_by_id(self, client: TestClient, auth_headers: dict):
        """测试根据 ID 获取权限"""
        # 创建权限
        create_response = client.post(
            "/api/v1/permissions",
            json={"code": "get:single", "name": "单个权限", "module": "test"},
            headers=auth_headers,
        )
        perm_id = create_response.json()["data"]["id"]

        # 获取权限
        response = client.get(f"/api/v1/permissions/{perm_id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["id"] == perm_id
        assert data["data"]["code"] == "get:single"

    def test_get_permission_not_found(self, client: TestClient, auth_headers: dict):
        """测试获取不存在的权限"""
        response = client.get("/api/v1/permissions/99999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_permission(self, client: TestClient, auth_headers: dict):
        """测试更新权限"""
        # 创建权限
        create_response = client.post(
            "/api/v1/permissions",
            json={"code": "update:perm", "name": "原名称", "module": "test"},
            headers=auth_headers,
        )
        perm_id = create_response.json()["data"]["id"]

        # 更新权限
        response = client.put(
            f"/api/v1/permissions/{perm_id}",
            json={"name": "新名称", "description": "更新后的描述"},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["name"] == "新名称"
        assert data["data"]["description"] == "更新后的描述"

    def test_delete_permission(self, client: TestClient, auth_headers: dict):
        """测试删除权限"""
        # 创建权限
        create_response = client.post(
            "/api/v1/permissions",
            json={"code": "delete:perm", "name": "待删除权限", "module": "test"},
            headers=auth_headers,
        )
        perm_id = create_response.json()["data"]["id"]

        # 删除权限
        response = client.delete(f"/api/v1/permissions/{perm_id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["success"] is True

        # 验证已删除
        get_response = client.get(f"/api/v1/permissions/{perm_id}", headers=auth_headers)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


class TestRoleAPI:
    """角色管理 API 测试类"""

    def test_create_role(self, client: TestClient, auth_headers: dict):
        """测试创建角色"""
        response = client.post(
            "/api/v1/roles",
            json={
                "code": "editor",
                "name": "编辑者",
                "description": "可以编辑内容",
            },
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["success"] is True
        assert data["data"]["code"] == "editor"
        assert data["data"]["name"] == "编辑者"

    def test_create_role_duplicate_code(self, client: TestClient, auth_headers: dict):
        """测试创建重复角色代码"""
        # 第一次创建
        client.post(
            "/api/v1/roles",
            json={"code": "dup_role", "name": "重复角色"},
            headers=auth_headers,
        )
        # 第二次创建相同 code
        response = client.post(
            "/api/v1/roles",
            json={"code": "dup_role", "name": "另一个角色"},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "已存在" in response.json()["msg"]

    def test_create_role_with_permissions(self, client: TestClient, auth_headers: dict):
        """测试创建角色并关联权限"""
        # 先创建权限
        perm1 = client.post(
            "/api/v1/permissions",
            json={"code": "custom:read", "name": "自定义读取", "module": "custom"},
            headers=auth_headers,
        ).json()["data"]

        perm2 = client.post(
            "/api/v1/permissions",
            json={"code": "custom:write", "name": "自定义编辑", "module": "custom"},
            headers=auth_headers,
        ).json()["data"]

        # 创建角色并关联权限
        response = client.post(
            "/api/v1/roles",
            json={
                "code": "custom_manager",
                "name": "自定义管理员",
                "permission_ids": [perm1["id"], perm2["id"]],
            },
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert len(data["data"]["permissions"]) == 2

    def test_get_roles(self, client: TestClient, auth_headers: dict):
        """测试获取角色列表"""
        # 创建测试角色
        client.post(
            "/api/v1/roles",
            json={"code": "test_role1", "name": "测试角色1"},
            headers=auth_headers,
        )
        client.post(
            "/api/v1/roles",
            json={"code": "test_role2", "name": "测试角色2"},
            headers=auth_headers,
        )

        response = client.get("/api/v1/roles", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert isinstance(data["data"], list)
        # 至少包含 admin 角色和创建的测试角色
        assert len(data["data"]) >= 2

    def test_get_role_by_id(self, client: TestClient, auth_headers: dict):
        """测试根据 ID 获取角色"""
        # 创建角色
        create_response = client.post(
            "/api/v1/roles",
            json={"code": "get_role", "name": "获取角色测试"},
            headers=auth_headers,
        )
        role_id = create_response.json()["data"]["id"]

        # 获取角色
        response = client.get(f"/api/v1/roles/{role_id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["id"] == role_id
        assert data["data"]["code"] == "get_role"

    def test_get_role_not_found(self, client: TestClient, auth_headers: dict):
        """测试获取不存在的角色"""
        response = client.get("/api/v1/roles/99999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_role(self, client: TestClient, auth_headers: dict):
        """测试更新角色"""
        # 创建角色
        create_response = client.post(
            "/api/v1/roles",
            json={"code": "update_role", "name": "原名称"},
            headers=auth_headers,
        )
        role_id = create_response.json()["data"]["id"]

        # 更新角色
        response = client.put(
            f"/api/v1/roles/{role_id}",
            json={"name": "新名称", "description": "更新后的描述"},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["name"] == "新名称"
        assert data["data"]["description"] == "更新后的描述"

    def test_update_role_permissions(self, client: TestClient, auth_headers: dict):
        """测试更新角色权限"""
        # 创建权限
        perm = client.post(
            "/api/v1/permissions",
            json={"code": "new:perm", "name": "新权限", "module": "test"},
            headers=auth_headers,
        ).json()["data"]

        # 创建角色
        create_response = client.post(
            "/api/v1/roles",
            json={"code": "perm_update_role", "name": "权限更新角色"},
            headers=auth_headers,
        )
        role_id = create_response.json()["data"]["id"]

        # 更新角色权限
        response = client.put(
            f"/api/v1/roles/{role_id}",
            json={"permission_ids": [perm["id"]]},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]["permissions"]) == 1
        assert data["data"]["permissions"][0]["id"] == perm["id"]

    def test_delete_role(self, client: TestClient, auth_headers: dict):
        """测试删除角色"""
        # 创建角色
        create_response = client.post(
            "/api/v1/roles",
            json={"code": "delete_role", "name": "待删除角色"},
            headers=auth_headers,
        )
        role_id = create_response.json()["data"]["id"]

        # 删除角色
        response = client.delete(f"/api/v1/roles/{role_id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["success"] is True

        # 验证已删除
        get_response = client.get(f"/api/v1/roles/{role_id}", headers=auth_headers)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


class TestRBACAccess:
    """RBAC 访问控制测试类"""

    def test_non_admin_cannot_manage_roles(self, client: TestClient):
        """测试非管理员无法管理角色"""
        # 注册普通用户
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "normaluser",
                "email": "normal@example.com",
                "nickname": "Normal User",
                "password": "password123",
            },
        )
        # 登录普通用户
        login_response = client.post(
            "/api/v1/auth/login",
            json={"username": "normaluser", "password": "password123"},
        )
        token = login_response.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 尝试获取角色列表
        response = client.get("/api/v1/roles", headers=headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # 尝试创建角色
        response = client.post(
            "/api/v1/roles",
            json={"code": "hacker", "name": "黑客"},
            headers=headers,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_non_admin_cannot_manage_permissions(self, client: TestClient):
        """测试非管理员无法管理权限"""
        # 注册普通用户
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "normaluser2",
                "email": "normal2@example.com",
                "nickname": "Normal User 2",
                "password": "password123",
            },
        )
        # 登录普通用户
        login_response = client.post(
            "/api/v1/auth/login",
            json={"username": "normaluser2", "password": "password123"},
        )
        token = login_response.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 尝试获取权限列表
        response = client.get("/api/v1/permissions", headers=headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # 尝试创建权限
        response = client.post(
            "/api/v1/permissions",
            json={"code": "hack:system", "name": "黑入系统", "module": "hack"},
            headers=headers,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
