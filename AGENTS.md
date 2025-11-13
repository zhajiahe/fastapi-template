# Ragflow

## Rule for Feedback
1. 在任何流程、任务、对话进行时，无论是询问、回复、或完成阶段性任务，皆必须调用 MCP mcp-feedback-enhanced。
2. 每当收到用户反馈，若反馈内容非空，必须再次调用 MCP mcp-feedback-enhanced，并根据反馈内容调整行为。
3. 仅当用户明确表示「结束」或「不再需要交互」时，才可停止调用 MCP mcp-feedback-enhanced，流程才算结束。
4. 除非收到结束指令，否则所有步骤都必须重复调用 MCP mcp-feedback-enhanced。
5. 完成任务前，必须使用 MCP mcp-feedback-enhanced 工具向用户询问反馈。

## Rule for Commit

**重要：仅在用户明确要求时才进行 Git 提交操作。**

### 提交规范（Commit Standards）：
遵循约定式提交格式，使用合适的 emoji 并创建描述性的中文提交信息。

### Commit Types:
- ✨ feat: 新功能
- 🐛 fix: Bug 修复
- 📝 docs: 文档修改
- ♻️ refactor: 代码重构
- 🧑‍💻 chore: 工具和维护
- 🎨 style: 代码格式、样式调整
- ⚡️ perf: 性能优化
- ✅ test: 测试相关
- 🗑️ chore: 删除文件或代码

### 提交步骤（仅在用户要求时执行）：
1. 运行 `git status` 查看变更
2. 使用 `git add` 添加文件到暂存区
3. 执行 `git commit -m` 提交，使用中文描述
4. 不包含 Claude 协作者信息

## Rule for Test
当实现测试脚本后，先执行测试后再编写文档
