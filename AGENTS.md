# AI 编程助手指南

## 项目架构

```
app/
├── api/          # 路由层：处理 HTTP 请求
├── services/     # 服务层：业务逻辑
├── repositories/ # 数据层：数据库操作
├── models/       # SQLAlchemy 模型
├── schemas/      # Pydantic 验证模型
├── core/         # 配置、安全、异常
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
```

## 注意事项

- 密码传输使用 JSON Body，不用 Query 参数
- JWT 双令牌：access_token (30分钟) + refresh_token (7天)
- 管理员接口需要 `CurrentSuperUser` 依赖
