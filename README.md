# FastAPI 后端开发模板

> 基于 FastAPI 的现代 Python 后端项目模板，集成最佳实践

## ✨ 特性

- 🚀 **FastAPI** + SQLAlchemy 2.0 异步 ORM
- 🔐 **JWT 认证** (Access Token + Refresh Token)
- 📁 **分层架构** (Router → Service → Repository)
- 🗃️ **Alembic** 数据库迁移
- 🧪 **Pytest** 单元测试 + 集成测试
- 🐳 **Docker** 容器化支持
- 🔍 **Ruff + Ty** 代码质量保证 (Ty 比 MyPy 快 10x-100x)
- 🤖 **AGENTS.md** AI 编程助手指南

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
│   ├── middleware/       # 自定义中间件
│   ├── utils/            # 工具函数
│   └── main.py           # 应用入口
├── tests/                # 测试代码
├── scripts/              # 工具脚本
├── alembic/              # 数据库迁移
├── AGENTS.md             # AI 编程助手指南
├── .env.example          # 环境变量模板
├── Dockerfile            # Docker 配置
├── docker-compose.yml    # Docker Compose
└── Makefile              # 构建脚本
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

### 4. 启动服务

```bash
make dev
# 访问 http://localhost:8000/docs
```

## 🛠️ 常用命令

```bash
# 开发相关
make dev              # 启动开发服务器
make install          # 安装依赖

# 测试相关
make test             # 运行所有测试
make test-unit        # 仅运行单元测试
make test-integration # 仅运行集成测试
make test-cov         # 测试 + 覆盖率报告

# 代码质量
make lint             # 代码检查
make lint-fix         # 代码检查并自动修复
make format           # 格式化代码
make type-check       # 类型检查 (使用 ty)
make check            # 运行所有检查

# 数据库迁移
make db-migrate msg="描述"  # 创建新迁移
make db-upgrade       # 升级到最新版本
make db-downgrade     # 回滚上一版本
make db-current       # 查看当前版本

# 其他工具
make clean            # 清理缓存文件
make pre-commit-install # 安装 pre-commit hooks
```

## 📡 API 概览

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/auth/login` | POST | 用户登录 |
| `/api/v1/auth/register` | POST | 用户注册 |
| `/api/v1/auth/refresh` | POST | 刷新令牌 |
| `/api/v1/auth/me` | GET | 获取当前用户 |
| `/api/v1/users` | GET/POST | 用户列表/创建 |
| `/api/v1/users/{id}` | GET/PUT/DELETE | 用户详情/更新/删除 |

## 🐳 Docker 部署

```bash
# 生产环境
docker-compose up -d app

# 开发环境（支持热重载）
docker-compose --profile dev up -d app-dev

# 使用 PostgreSQL
docker-compose --profile postgres up -d
```

## 🤖 AI 编程助手指南

本项目包含 `AGENTS.md` 文件，这是一个专为 AI 编程助手编写的使用指南，定义了：

- 项目架构和技术栈说明
- 开发环境搭建和常用命令
- 代码风格和命名规范
- Git 提交规范和 PR 流程
- 安全注意事项和 AI 操作边界

如果你正在使用 AI 编程助手开发这个项目，请先阅读 `AGENTS.md` 文件以了解项目的约定和规范。

## 📄 License

MIT License
