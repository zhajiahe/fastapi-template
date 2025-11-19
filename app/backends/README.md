# Custom Backends

为 LangGraph Agent 提供文件系统和命令执行能力的自定义后端实现。

## 快速选择

| Backend | 适用场景 | 隔离级别 | 性能 | 文件持久化 |
|---------|---------|---------|------|-----------|
| [StateSandboxBackend](#statesandboxbackend) | 开发/测试 | ❌ 无 | ⚡ 极快 | ❌ 会话结束即删除 |
| [FilesystemSandboxBackend](#filesystemsandboxbackend) | 本地开发 | ⚠️ 路径隔离 | ⚡ 快 | ✅ 永久保存 |
| [DockerSandboxBackend](#dockersandboxbackend) | **生产环境** | ✅ 完全隔离 | 🐢 较慢 | ⚠️ 容器删除即删除 |

---

# StateSandboxBackend

## 概述

轻量级沙箱，文件存储在 Agent 状态（内存）中，支持命令执行。

## 特性

- ✅ 命令执行（宿主系统）
- ✅ 文件系统操作（内存）
- ✅ 零依赖
- ⚡ 极快启动
- ❌ 无隔离（安全性低）

## 使用

```python
from app.backends import StateSandboxBackend
from deepagents.middleware import FilesystemMiddleware

agent = create_agent(
    model,
    tools=tools,
    middleware=[
        FilesystemMiddleware(backend=lambda rt: StateSandboxBackend(rt))
    ]
)
```

## 配置

```python
StateSandboxBackend(
    runtime: ToolRuntime,
    max_output_size: int = 100000  # 最大输出大小
)
```

## ⚠️ 安全警告

- 直接在宿主系统执行命令，**无隔离**
- 仅适合开发/测试环境
- 不要在生产环境使用

---

# FilesystemSandboxBackend

## 概述

基于真实文件系统的后端，文件永久保存，支持命令执行和路径沙箱。

## 特性

- ✅ 真实文件系统（永久保存）
- ✅ 命令执行（宿主系统）
- ✅ 虚拟模式（路径隔离）
- ⚡ 快速启动
- ⚠️ 中等安全性

## 使用

```python
from app.backends import FilesystemSandboxBackend

# 基础使用
backend = FilesystemSandboxBackend(
    root_dir="./workspace",
    virtual_mode=True,  # 启用路径沙箱
)

agent = create_agent(
    model,
    tools=tools,
    middleware=[FilesystemMiddleware(backend=backend)]
)
```

### 使用临时目录

```python
import tempfile

with tempfile.TemporaryDirectory() as tmpdir:
    backend = FilesystemSandboxBackend(
        root_dir=tmpdir,
        virtual_mode=True,
    )
    # 使用 backend...
```

## 配置

```python
FilesystemSandboxBackend(
    root_dir: str | Path = None,      # 根目录（默认：当前目录）
    virtual_mode: bool = False,       # 启用路径沙箱
    max_file_size_mb: int = 10,       # 最大文件大小
    max_output_size: int = 100000,    # 最大输出大小
    command_timeout: int = 30,        # 命令超时（秒）
)
```

## 虚拟模式

启用 `virtual_mode=True` 后：
- ✅ 防止访问 `root_dir` 外的文件
- ✅ 阻止路径遍历（`..`、`~`）
- ✅ 确保文件操作安全

```python
backend = FilesystemSandboxBackend(
    root_dir="/workspace",
    virtual_mode=True,
)

# ✅ 允许
backend.write("/file.txt", "content")  # → /workspace/file.txt

# ❌ 阻止
backend.write("/../etc/passwd", "x")   # → ValueError: Path traversal not allowed
```

## 测试

```bash
uv run python scripts/test_filesystem_sandbox.py
```

---

# DockerSandboxBackend

## 概述

生产级沙箱，使用 Docker 容器提供完全隔离的执行环境。

## 特性

- ✅ 完全隔离（容器）
- ✅ 资源限制（CPU、内存）
- ✅ 网络隔离（可选）
- ✅ 自动清理
- 🐢 启动较慢（1-2秒）

## 使用

### 基础使用

```python
from app.backends import DockerSandboxBackend

backend = DockerSandboxBackend(
    image="python:3.12-slim",
    memory_limit="512m",
    network_mode="none",  # 完全隔离网络
)

agent = create_agent(
    model,
    tools=tools,
    middleware=[FilesystemMiddleware(backend=backend)]
)

# 使用完后清理
backend.cleanup()
```

### 使用上下文管理器（推荐）

```python
with DockerSandboxBackend() as backend:
    agent = create_agent(
        model,
        tools=tools,
        middleware=[FilesystemMiddleware(backend=backend)]
    )
    result = await agent.ainvoke({"messages": [...]})
    # 容器自动清理
```

## 配置

```python
DockerSandboxBackend(
    image: str = "python:3.12-slim",  # Docker 镜像
    memory_limit: str = "512m",        # 内存限制
    cpu_quota: int = 50000,            # CPU 配额（50% = 50000）
    network_mode: str = "none",        # 网络模式
    working_dir: str = "/workspace",   # 工作目录
    auto_remove: bool = True,          # 自动删除容器
    max_output_size: int = 100000,     # 最大输出大小
    command_timeout: int = 30,         # 命令超时（秒）
)
```

## 网络模式

```python
# 完全禁用网络（推荐）
backend = DockerSandboxBackend(network_mode="none")

# 允许网络访问（谨慎使用）
backend = DockerSandboxBackend(network_mode="bridge")
```

## 资源限制

```python
backend = DockerSandboxBackend(
    memory_limit="256m",   # 最多 256MB 内存
    cpu_quota=25000,       # 最多 25% CPU
)
```

## 测试

```bash
# 基础测试
uv run python scripts/test_docker_sandbox.py

# Agent 集成测试
uv run python scripts/test_docker_sandbox.py --with-agent
```

## 依赖

需要安装 Docker：

```bash
# 检查 Docker 是否运行
docker ps

# 预拉取镜像（可选，加快首次启动）
docker pull python:3.12-slim
```

---

# 使用建议

## 开发阶段

```python
# 快速测试，无需 Docker
from app.backends import StateSandboxBackend

middleware=[
    FilesystemMiddleware(backend=lambda rt: StateSandboxBackend(rt))
]
```

## 本地开发

```python
# 真实文件系统，方便调试
from app.backends import FilesystemSandboxBackend

middleware=[
    FilesystemMiddleware(backend=FilesystemSandboxBackend(
        root_dir="./workspace",
        virtual_mode=True,
    ))
]
```

## 生产环境

```python
# 完全隔离，最安全
from app.backends import DockerSandboxBackend

with DockerSandboxBackend(
    memory_limit="512m",
    network_mode="none",
) as backend:
    middleware=[
        FilesystemMiddleware(backend=backend)
    ]
```

---

# 功能对比

## 文件系统

| Backend | 存储位置 | 持久化 | 真实文件 |
|---------|---------|--------|---------|
| StateSandboxBackend | 内存 | ❌ | ❌ |
| FilesystemSandboxBackend | 磁盘 | ✅ | ✅ |
| DockerSandboxBackend | 容器 | ⚠️ | ⚠️ |

## 命令执行

| Backend | 执行环境 | 隔离 | 安全性 |
|---------|---------|------|--------|
| StateSandboxBackend | 宿主系统 | ❌ | ⚠️ 低 |
| FilesystemSandboxBackend | 宿主系统 | ⚠️ 路径 | ⚠️ 中 |
| DockerSandboxBackend | 容器 | ✅ 完全 | ✅ 高 |

## 性能

| Backend | 启动时间 | 命令执行 | 文件操作 |
|---------|---------|---------|---------|
| StateSandboxBackend | ⚡ <1ms | ⚡ 快 | ⚡ 快 |
| FilesystemSandboxBackend | ⚡ <1ms | ⚡ 快 | ⚡ 快 |
| DockerSandboxBackend | 🐢 1-2s | ⚡ 快 | ⚡ 快 |

---

# 常见问题

## Q: 如何选择 Backend？

**A**: 根据场景选择：
- **开发/测试**：StateSandboxBackend（最快）
- **本地开发**：FilesystemSandboxBackend（真实文件）
- **生产环境**：DockerSandboxBackend（最安全）

## Q: Docker 容器会自动清理吗？

**A**: 是的，设置 `auto_remove=True`（默认）后，容器停止时自动删除。
也可以使用上下文管理器确保清理：

```python
with DockerSandboxBackend() as backend:
    # 使用 backend...
    pass
# 容器自动清理
```

## Q: 虚拟模式是什么？

**A**: FilesystemSandboxBackend 的安全特性，防止访问 `root_dir` 外的文件：

```python
backend = FilesystemSandboxBackend(
    root_dir="/workspace",
    virtual_mode=True,  # 启用
)

# ✅ 允许：/workspace/file.txt
# ❌ 阻止：/../etc/passwd
```

## Q: 如何限制 Docker 资源？

**A**: 通过参数配置：

```python
backend = DockerSandboxBackend(
    memory_limit="256m",   # 内存限制
    cpu_quota=25000,       # CPU 限制（25%）
)
```

## Q: 文件会永久保存吗？

**A**: 取决于 Backend：
- StateSandboxBackend：❌ 会话结束即删除
- FilesystemSandboxBackend：✅ 永久保存
- DockerSandboxBackend：⚠️ 容器删除即删除

---

# 参考

- [deepagents 文档](https://github.com/langchain-ai/deepagents)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [Docker Python SDK](https://docker-py.readthedocs.io/)
