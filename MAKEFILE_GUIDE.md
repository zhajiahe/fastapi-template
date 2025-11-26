# Makefile 使用指南

## 查看帮助

```bash
make help
```

## 开发命令

```bash
make install          # 安装依赖
make dev              # 启动开发服务器
```

## 测试命令

```bash
make test             # 运行所有测试
make test-unit        # 运行单元测试
make test-integration # 运行集成测试
make test-cov         # 测试 + 覆盖率报告
```

## 代码质量

```bash
make lint             # 代码检查
make lint-fix         # 检查并修复
make format           # 格式化代码
make type-check       # 类型检查
make check            # 运行所有检查
```

## Pre-commit

```bash
make pre-commit-install  # 安装 hooks
make pre-commit-run      # 运行检查
```

## 数据库

```bash
make db-migrate msg="xxx"  # 创建迁移
make db-upgrade            # 应用迁移
make db-downgrade          # 回滚迁移
make db-history            # 查看历史
make db-current            # 当前版本
```

## Docker

```bash
make docker-build     # 构建镜像
make docker-run       # 运行容器
make docker-stop      # 停止容器
make docker-dev       # 开发环境
```

## 清理

```bash
make clean            # 清理临时文件
```
