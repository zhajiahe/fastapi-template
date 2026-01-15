.PHONY: help install dev test test-unit test-integration test-cov lint lint-fix format type-check check \
       db-migrate db-upgrade db-downgrade db-history db-current \
       docker-build docker-run docker-stop docker-dev clean pre-commit-install pre-commit-run

# 默认目标
.DEFAULT_GOAL := help

help: ## 显示帮助信息
	@echo "FastAPI Template - 可用命令:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-18s %s\n", $$1, $$2}'

# ==================== 开发相关 ====================

install: ## 安装依赖
	@echo "📦 安装依赖..."
	uv sync

dev: ## 启动开发服务器
	@echo "🚀 启动开发服务器..."
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# ==================== 测试相关 ====================

test: ## 运行所有测试
	@echo "🧪 运行所有测试..."
	uv run pytest tests/ -v

test-unit: ## 运行单元测试
	@echo "🧪 运行单元测试..."
	uv run pytest tests/unit/ -v -m unit

test-integration: ## 运行集成测试
	@echo "🧪 运行集成测试..."
	uv run pytest tests/integration/ -v -m integration

test-cov: ## 运行测试并生成覆盖率报告
	@echo "🧪 运行测试并生成覆盖率报告..."
	uv run pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

# ==================== 代码质量 ====================

lint: ## 代码检查
	@echo "🔍 代码检查..."
	uv run ruff check app/ tests/

lint-fix: ## 代码检查并修复
	@echo "🔧 代码检查并修复..."
	uv run ruff check app/ tests/ --fix

format: ## 格式化代码
	@echo "🎨 格式化代码..."
	uv run ruff format app/ tests/

type-check: ## 类型检查 (使用 ty - 比 mypy 快 10x-100x)
	@echo "🔍 类型检查..."
	uv run ty check

check: lint-fix format type-check ## 运行所有检查（lint + format + type-check）
	@echo "✅ 所有检查完成"

# ==================== 数据库迁移 ====================

db-migrate: ## 创建数据库迁移 (用法: make db-migrate msg="迁移说明")
	@echo "📝 创建数据库迁移..."
	uv run alembic revision --autogenerate -m "$(msg)"

db-upgrade: ## 升级数据库到最新版本
	@echo "⬆️ 升级数据库..."
	uv run alembic upgrade head

db-downgrade: ## 回滚数据库到上一版本
	@echo "⬇️ 回滚数据库..."
	uv run alembic downgrade -1

db-history: ## 查看迁移历史
	@echo "📜 迁移历史..."
	uv run alembic history --verbose

db-current: ## 查看当前数据库版本
	@echo "📌 当前数据库版本..."
	uv run alembic current

# ==================== Pre-commit ====================

pre-commit-install: ## 安装 pre-commit hooks
	@echo "🔗 安装 pre-commit hooks..."
	uv run pre-commit install

pre-commit-run: ## 运行 pre-commit 检查
	@echo "🔍 运行 pre-commit 检查..."
	uv run pre-commit run --all-files

# ==================== 清理相关 ====================

clean: ## 清理临时文件
	@echo "🧹 清理临时文件..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ty" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf htmlcov/ .coverage 2>/dev/null || true
	@echo "✅ 清理完成"
