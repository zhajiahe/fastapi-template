# AI 编程助手指南

## 项目架构

```
app/
├── api/          # 路由层：处理 HTTP 请求
├── services/     # 服务层：业务逻辑
├── repositories/ # 数据层：数据库操作
├── models/       # SQLAlchemy 模型
├── schemas/      # Pydantic 验证模型
├── core/         # 配置、安全、异常、权限
│   ├── permissions.py  # 权限码常量定义
│   └── deps.py         # 依赖注入（权限检查）
└── main.py       # 应用入口
```

## 开发规范

### 分层职责
- **Router**: 参数验证、调用 Service、返回响应
- **Service**: 业务逻辑、调用 Repository
- **Repository**: 数据库 CRUD 操作

### 响应格式
统一使用 `BaseResponse`:
```python
BaseResponse(success=True, code=200, msg="成功", data=result)
```

### 异常处理
使用自定义异常（自动转换为统一响应）:
- `NotFoundException` - 404
- `BadRequestException` - 400
- `UnauthorizedException` - 401
- `ForbiddenException` - 403

### 数据库
- 使用异步 SQLAlchemy
- 继承 `BaseTableMixin` 获取通用字段
- 软删除：`deleted=1`

### RBAC 权限控制
使用细粒度权限码检查，权限码定义在 `app/core/permissions.py`：

```python
# 使用方式 1：装饰器方式
@router.get("/users", dependencies=[Depends(require_permission(PermissionCode.USER_READ))])
async def get_users(db: DBSession):
    ...

# 使用方式 2：参数依赖方式
@router.get("/users/{id}")
async def get_user(
    user_id: int,
    current_user: Annotated[User, Depends(require_permission(PermissionCode.USER_READ))]
):
    ...
```

权限码命名规范：`{模块}:{操作}`，如 `user:read`、`role:create`

## 工作流程

1. **新增功能**: Schema → Model → Repository → Service → Router
2. **测试优先**: 先执行测试，再编写文档
3. **提交前**: `make check` 确保代码质量

## 常用命令

```bash
make dev          # 启动开发服务器
make test         # 运行测试
make check        # lint + format + type-check
make db-migrate msg="xxx"  # 数据库迁移
make db-init-rbac # 初始化 RBAC 权限数据
```

## 注意事项

- 密码传输使用 JSON Body，不用 Query 参数
- JWT 双令牌：access_token (30分钟) + refresh_token (7天)
- 权限检查使用 `require_permission(PermissionCode.XXX)` 依赖
- 角色检查使用 `require_role("admin")` 依赖
- 新增功能时需要同步添加权限码到 `app/core/permissions.py`
