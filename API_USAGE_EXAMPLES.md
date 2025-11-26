# API 使用示例

## 认证 API

### 1. 用户登录

```http
POST /api/v1/auth/login
Content-Type: application/json

{"username": "john_doe", "password": "SecurePass123"}
```

### 2. 用户注册

```http
POST /api/v1/auth/register
Content-Type: application/json

{"username": "john_doe", "email": "john@example.com", "nickname": "John", "password": "SecurePass123"}
```

### 3. 刷新令牌

```http
POST /api/v1/auth/refresh
Content-Type: application/json

{"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
```

### 4. 获取当前用户

```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

### 5. 修改密码

```http
POST /api/v1/auth/change-password
Authorization: Bearer <access_token>
Content-Type: application/json

{"old_password": "OldPass123", "new_password": "NewPass456"}
```

## 用户管理 API（需管理员权限）

### 1. 创建用户

```http
POST /api/v1/users
Authorization: Bearer <access_token>
Content-Type: application/json

{"username": "john_doe", "email": "john@example.com", "nickname": "John", "password": "SecurePass123"}
```

### 2. 获取用户列表

```http
GET /api/v1/users?page_num=1&page_size=10&keyword=john
Authorization: Bearer <access_token>
```

### 3. 获取单个用户

```http
GET /api/v1/users/1
Authorization: Bearer <access_token>
```

### 4. 更新用户

```http
PUT /api/v1/users/1
Authorization: Bearer <access_token>
Content-Type: application/json

{"nickname": "John Doe", "is_active": true}
```

### 5. 删除用户

```http
DELETE /api/v1/users/1
Authorization: Bearer <access_token>
```

## curl 测试命令

```bash
# 登录
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | jq -r '.data.access_token')

# 获取当前用户
curl "http://localhost:8000/api/v1/auth/me" -H "Authorization: Bearer $TOKEN"

# 获取用户列表
curl "http://localhost:8000/api/v1/users" -H "Authorization: Bearer $TOKEN"
```
