# API 使用示例

## 用户管理 API

### 1. 创建用户

**请求**:
```http
POST /users
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "nickname": "John",
  "password": "SecurePass123",
  "is_active": true,
  "is_superuser": false
}
```

**响应**:
```json
{
  "success": true,
  "code": 201,
  "msg": "创建用户成功",
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "nickname": "John",
    "is_active": true,
    "is_superuser": false,
    "create_time": "2024-01-01T12:00:00",
    "update_time": "2024-01-01T12:00:00"
  },
  "err": null
}
```

### 2. 获取用户列表（分页）

**请求**:
```http
GET /users?page_num=1&page_size=10&keyword=john&is_active=true
```

**参数说明**:
- `page_num`: 页码（默认：1，最小：1）
- `page_size`: 每页数量（默认：10，最小：1）
- `keyword`: 搜索关键词（可选，搜索用户名、邮箱、昵称）
- `is_active`: 激活状态筛选（可选，true/false）
- `is_superuser`: 超级管理员筛选（可选，true/false）

**响应**:
```json
{
  "success": true,
  "code": 200,
  "msg": "获取用户列表成功",
  "data": {
    "page_num": 1,
    "page_size": 10,
    "total": 25,
    "items": [
      {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "nickname": "John",
        "is_active": true,
        "is_superuser": false,
        "create_time": "2024-01-01T12:00:00",
        "update_time": "2024-01-01T12:00:00"
      }
    ]
  },
  "err": null
}
```

### 3. 获取单个用户

**请求**:
```http
GET /users/1
```

**响应**:
```json
{
  "success": true,
  "code": 200,
  "msg": "获取用户成功",
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "nickname": "John",
    "is_active": true,
    "is_superuser": false,
    "create_time": "2024-01-01T12:00:00",
    "update_time": "2024-01-01T12:00:00"
  },
  "err": null
}
```

### 4. 更新用户

**请求**:
```http
PUT /users/1
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "nickname": "John Doe",
  "is_active": true
}
```

**注意**: 所有字段都是可选的，只传需要更新的字段

**响应**:
```json
{
  "success": true,
  "code": 200,
  "msg": "更新用户成功",
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john.doe@example.com",
    "nickname": "John Doe",
    "is_active": true,
    "is_superuser": false,
    "create_time": "2024-01-01T12:00:00",
    "update_time": "2024-01-01T12:30:00"
  },
  "err": null
}
```

### 5. 删除用户（逻辑删除）

**请求**:
```http
DELETE /users/1
```

**响应**:
```json
{
  "success": true,
  "code": 200,
  "msg": "删除用户成功",
  "data": null,
  "err": null
}
```

## Python 客户端示例

### 使用 requests

```python
import requests

base_url = "http://localhost:8000"

# 创建用户
response = requests.post(
    f"{base_url}/users",
    json={
        "username": "john_doe",
        "email": "john@example.com",
        "nickname": "John",
        "password": "SecurePass123",
        "is_active": True,
        "is_superuser": False
    }
)
print(response.json())

# 获取用户列表
response = requests.get(
    f"{base_url}/users",
    params={
        "page_num": 1,
        "page_size": 10,
        "keyword": "john"
    }
)
print(response.json())

# 获取单个用户
response = requests.get(f"{base_url}/users/1")
print(response.json())

# 更新用户
response = requests.put(
    f"{base_url}/users/1",
    json={
        "nickname": "John Doe"
    }
)
print(response.json())

# 删除用户
response = requests.delete(f"{base_url}/users/1")
print(response.json())
```

### 使用 httpx (异步)

```python
import asyncio
import httpx

base_url = "http://localhost:8000"

async def main():
    async with httpx.AsyncClient() as client:
        # 创建用户
        response = await client.post(
            f"{base_url}/users",
            json={
                "username": "john_doe",
                "email": "john@example.com",
                "nickname": "John",
                "password": "SecurePass123",
            }
        )
        print(response.json())

        # 获取用户列表
        response = await client.get(
            f"{base_url}/users",
            params={"page_num": 1, "page_size": 10}
        )
        print(response.json())

asyncio.run(main())
```

## JavaScript/TypeScript 客户端示例

### 使用 fetch

```javascript
const baseUrl = "http://localhost:8000";

// 创建用户
async function createUser() {
  const response = await fetch(`${baseUrl}/users`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: "john_doe",
      email: "john@example.com",
      nickname: "John",
      password: "SecurePass123",
      is_active: true,
      is_superuser: false,
    }),
  });
  const data = await response.json();
  console.log(data);
}

// 获取用户列表
async function getUsers() {
  const params = new URLSearchParams({
    page_num: "1",
    page_size: "10",
    keyword: "john",
  });
  const response = await fetch(`${baseUrl}/users?${params}`);
  const data = await response.json();
  console.log(data);
}

// 更新用户
async function updateUser(userId) {
  const response = await fetch(`${baseUrl}/users/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      nickname: "John Doe",
    }),
  });
  const data = await response.json();
  console.log(data);
}

// 删除用户
async function deleteUser(userId) {
  const response = await fetch(`${baseUrl}/users/${userId}`, {
    method: "DELETE",
  });
  const data = await response.json();
  console.log(data);
}
```

### 使用 axios

```javascript
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

// 创建用户
async function createUser() {
  const { data } = await api.post("/users", {
    username: "john_doe",
    email: "john@example.com",
    nickname: "John",
    password: "SecurePass123",
  });
  console.log(data);
}

// 获取用户列表
async function getUsers() {
  const { data } = await api.get("/users", {
    params: {
      page_num: 1,
      page_size: 10,
      keyword: "john",
    },
  });
  console.log(data);
}

// 更新用户
async function updateUser(userId) {
  const { data } = await api.put(`/users/${userId}`, {
    nickname: "John Doe",
  });
  console.log(data);
}

// 删除用户
async function deleteUser(userId) {
  const { data } = await api.delete(`/users/${userId}`);
  console.log(data);
}
```

## 错误处理

### 常见错误响应

#### 400 Bad Request - 参数错误
```json
{
  "success": false,
  "code": 400,
  "msg": "用户名已存在",
  "data": null,
  "err": null
}
```

#### 404 Not Found - 资源不存在
```json
{
  "success": false,
  "code": 404,
  "msg": "用户不存在",
  "data": null,
  "err": null
}
```

#### 422 Unprocessable Entity - 验证错误
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "password"],
      "msg": "String should have at least 6 characters",
      "input": "12345"
    }
  ]
}
```

## Schema 定义

### UserCreate
```python
{
  "username": str,      # 3-50字符，必填
  "email": str,         # 邮箱格式，必填
  "nickname": str,      # 1-50字符，必填
  "password": str,      # 6-128字符，必填
  "is_active": bool,    # 可选，默认true
  "is_superuser": bool  # 可选，默认false
}
```

### UserUpdate
```python
{
  "email": str | None,         # 邮箱格式，可选
  "nickname": str | None,      # 1-50字符，可选
  "is_active": bool | None,    # 可选
  "is_superuser": bool | None  # 可选
}
```

### UserResponse
```python
{
  "id": int,
  "username": str,
  "email": str,
  "nickname": str,
  "is_active": bool,
  "is_superuser": bool,
  "create_time": datetime | None,
  "update_time": datetime | None
}
```

### BasePageQuery (查询参数)
```python
{
  "page_num": int,   # 页码，默认1，最小1
  "page_size": int   # 每页数量，默认10，最小1
}
```

### UserListQuery (查询参数)
```python
{
  "keyword": str | None,         # 搜索关键词
  "is_active": bool | None,      # 激活状态
  "is_superuser": bool | None    # 超级管理员状态
}
```

## 测试命令

### 使用 curl

```bash
# 创建用户
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "nickname": "John",
    "password": "SecurePass123"
  }'

# 获取用户列表
curl "http://localhost:8000/users?page_num=1&page_size=10&keyword=john"

# 获取单个用户
curl "http://localhost:8000/users/1"

# 更新用户
curl -X PUT "http://localhost:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{"nickname": "John Doe"}'

# 删除用户
curl -X DELETE "http://localhost:8000/users/1"
```

## 注意事项

1. **密码安全**: 密码在存储前会自动使用 bcrypt 加密
2. **逻辑删除**: 删除操作是逻辑删除，数据不会真正从数据库中删除
3. **分页**: 所有列表查询都支持分页，使用 `BasePageQuery` 提供统一的分页参数
4. **验证**: 所有输入都会经过 Pydantic 验证，确保数据格式正确
5. **响应格式**: 所有响应都使用统一的 `BaseResponse` 格式包装
6. **错误处理**: API 会返回清晰的错误信息，便于调试
