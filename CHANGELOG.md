# Changelog

所有重要的项目变更都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [0.2.0] - 2025-01-XX

### ✨ 新增功能
- 添加工具调用信息的实时显示
- 实现统一 API 响应格式、增强参数验证和异常处理
- 添加对话接口性能测试系统
- 添加前端聊天界面增强功能
- 更新前端以适配统一 API 响应格式

### ⚡️ 性能优化
- 使用 astream_events 实现真正的逐 token 流式输出
- 优化流式对话输出，实现真正的逐字流式效果

### 🐛 Bug 修复
- 修复流式输出中文编码问题
- 修复 chat 接口重复保存用户消息的问题
- 添加 MyPy 配置忽略性能测试文件的类型检查错误

## [0.1.0] - 初始版本

### ✨ 核心功能
- FastAPI + SQLAlchemy 2.0+ 异步 ORM
- 完整的用户认证系统（JWT 双令牌）
- LangGraph 对话系统（流式/非流式）
- 会话管理和状态持久化
- 数据库迁移（Alembic）
- 结构化日志系统（Loguru）
- 代码质量保证（Ruff、MyPy、Pytest）
- 用户个性化设置
