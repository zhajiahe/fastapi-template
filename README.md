# FastAPI 后端开发模板

> 基于 FastAPI 的现代 Python 后端项目模板，集成最佳实践

## ✨ 特性

- 🚀 **FastAPI** + SQLAlchemy 2.0 异步 ORM
- 🔐 **JWT 认证** (Access Token + Refresh Token)
- 🛡️ **RBAC 权限控制** (角色 + 细粒度权限码)
- 📁 **分层架构** (Router → Service → Repository)
- 🗃️ **Alembic** 数据库迁移
- 🧪 **Pytest** 单元测试 + 集成测试
- 🐳 **Docker** 容器化支持
- 🔍 **Ruff + MyPy** 代码质量保证

## 📦 项目结构

```
fastapi-template/
├── app/
│   ├── api/              # API 路由
│   ├── core/             # 配置、安全、数据库
│   ├── models/           # SQLAlchemy 模型
│   ├── schemas/          # Pydantic 模型
│   ├── services/         # 业务逻辑层
│   ├── repositories/     # 数据访问层
│   └── main.py           # 应用入口
├── tests/                # 测试代码
├── alembic/              # 数据库迁移
├── Dockerfile            # Docker 配置
└── docker-compose.yml    # Docker Compose
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装 uv（如未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆并安装
git clone <your-repo-url>
cd fastapi-template
uv sync
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 设置数据库和密钥
```

### 3. 初始化数据库

```bash
make db-upgrade
```

### 4. 初始化 RBAC 权限数据

```bash
make db-init-rbac
```

这将创建：
- 12 个基础权限 (user/role/permission 各 4 个 CRUD 权限)
- admin 角色（拥有所有权限）
- user_manager 角色（用户管理权限）
- viewer 角色（只读权限）

### 5. 启动服务

```bash
make dev
# 访问 http://localhost:8000/docs
```

## 🛠️ 常用命令

```bash
make dev              # 启动开发服务器
make test             # 运行测试
make test-cov         # 测试 + 覆盖率报告
make lint-fix         # 代码检查并修复
make format           # 格式化代码
make check            # 运行所有检查
make db-init-rbac     # 初始化 RBAC 权限数据
```

## 📡 API 概览

### 认证接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/auth/login` | POST | 用户登录 |
| `/api/v1/auth/register` | POST | 用户注册 |
| `/api/v1/auth/refresh` | POST | 刷新令牌 |
| `/api/v1/auth/me` | GET/PUT | 获取/更新当前用户 |
| `/api/v1/auth/change-password` | POST | 修改密码 |

### 用户管理接口 (需要对应权限)

| 接口 | 方法 | 所需权限 |
|------|------|----------|
| `/api/v1/users` | GET | `user:read` |
| `/api/v1/users` | POST | `user:create` |
| `/api/v1/users/{id}` | GET | `user:read` |
| `/api/v1/users/{id}` | PUT | `user:update` |
| `/api/v1/users/{id}` | DELETE | `user:delete` |

### 角色管理接口 (需要对应权限)

| 接口 | 方法 | 所需权限 |
|------|------|----------|
| `/api/v1/roles` | GET/POST | `role:read` / `role:create` |
| `/api/v1/roles/{id}` | GET/PUT/DELETE | `role:read/update/delete` |

### 权限管理接口 (需要对应权限)

| 接口 | 方法 | 所需权限 |
|------|------|----------|
| `/api/v1/permissions` | GET/POST | `permission:read/create` |
| `/api/v1/permissions/{id}` | GET/PUT/DELETE | `permission:read/update/delete` |

## 🐳 Docker 部署

```bash
# 生产环境
docker-compose up -d app

# 开发环境（支持热重载）
docker-compose --profile dev up -d app-dev

# 使用 PostgreSQL
docker-compose --profile postgres up -d
```
## 📄 License

MIT License
