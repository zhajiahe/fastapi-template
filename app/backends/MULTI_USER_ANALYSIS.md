# 多用户场景分析

## 概述

当多个用户同时使用不同的 Backend 时，会出现不同的行为和潜在问题。

---

## 1. StateSandboxBackend

### 行为

```python
# 用户 A
backend_a = lambda rt: StateSandboxBackend(rt)
agent_a = create_agent(model, tools, middleware=[FilesystemMiddleware(backend=backend_a)])

# 用户 B
backend_b = lambda rt: StateSandboxBackend(rt)
agent_b = create_agent(model, tools, middleware=[FilesystemMiddleware(backend=backend_b)])
```

### 文件隔离

- ✅ **完全隔离**：每个用户的文件存储在各自的 Agent 状态中
- ✅ **无冲突**：用户 A 和用户 B 的文件互不影响
- ✅ **会话隔离**：不同会话的文件也是隔离的

```
用户 A 会话 1: {"/file.txt": "A1 content"}
用户 A 会话 2: {"/file.txt": "A2 content"}
用户 B 会话 1: {"/file.txt": "B1 content"}
```

### 命令执行

- ⚠️ **共享宿主系统**：所有用户在同一个系统上执行命令
- ⚠️ **无资源隔离**：用户 A 可能占用大量 CPU/内存影响用户 B
- ⚠️ **安全风险**：恶意用户可能执行危险命令

```python
# 用户 A 执行
backend.execute("rm -rf /tmp/*")  # 影响所有用户！

# 用户 B 执行
backend.execute(":(){ :|:& };:")  # Fork 炸弹，影响所有用户！
```

### 潜在问题

| 问题 | 严重性 | 说明 |
|------|--------|------|
| 资源竞争 | 🔴 高 | 多用户争夺 CPU/内存 |
| 安全风险 | 🔴 高 | 恶意命令影响系统 |
| 文件冲突 | ✅ 无 | 文件存储在状态中 |

---

## 2. FilesystemSandboxBackend

### 行为

```python
# 用户 A
backend_a = FilesystemSandboxBackend(
    root_dir="/workspace/user_a",
    virtual_mode=True,
)

# 用户 B
backend_b = FilesystemSandboxBackend(
    root_dir="/workspace/user_b",
    virtual_mode=True,
)
```

### 文件隔离

- ✅ **目录隔离**：每个用户有独立的 `root_dir`
- ⚠️ **需要手动配置**：必须为每个用户设置不同的 `root_dir`
- ⚠️ **虚拟模式必须启用**：否则用户可以访问其他目录

```
/workspace/
├── user_a/
│   └── file.txt  # 用户 A 的文件
└── user_b/
    └── file.txt  # 用户 B 的文件
```

### 命令执行

- ⚠️ **共享宿主系统**：所有用户在同一个系统上执行命令
- ⚠️ **工作目录隔离**：命令在各自的 `root_dir` 中执行
- ⚠️ **仍有安全风险**：用户可以执行系统命令

```python
# 用户 A 执行（在 /workspace/user_a 中）
backend_a.execute("ls")  # 只看到 user_a 的文件

# 用户 B 执行（在 /workspace/user_b 中）
backend_b.execute("ls")  # 只看到 user_b 的文件

# 但是！用户 A 仍然可以：
backend_a.execute("ps aux")  # 看到所有用户的进程
backend_a.execute("cat /etc/passwd")  # 读取系统文件（如果有权限）
```

### 潜在问题

| 问题 | 严重性 | 说明 |
|------|--------|------|
| 资源竞争 | 🔴 高 | 多用户争夺 CPU/内存 |
| 安全风险 | 🟡 中 | 虚拟模式提供部分保护 |
| 文件冲突 | ⚠️ 中 | 需要手动配置不同目录 |
| 磁盘空间 | ⚠️ 中 | 共享磁盘，可能被占满 |

---

## 3. DockerSandboxBackend

### 行为

```python
# 用户 A
backend_a = DockerSandboxBackend(
    image="python:3.12-slim",
    memory_limit="512m",
    cpu_quota=50000,
)

# 用户 B
backend_b = DockerSandboxBackend(
    image="python:3.12-slim",
    memory_limit="512m",
    cpu_quota=50000,
)
```

### 文件隔离

- ✅ **完全隔离**：每个用户有独立的容器和文件系统
- ✅ **自动隔离**：无需手动配置
- ✅ **容器级别隔离**：文件系统、进程、网络全部隔离

```
容器 A (用户 A):
  /workspace/file.txt

容器 B (用户 B):
  /workspace/file.txt

完全独立，互不影响！
```

### 命令执行

- ✅ **完全隔离**：每个用户在独立的容器中执行命令
- ✅ **资源限制**：每个容器有独立的 CPU/内存限制
- ✅ **网络隔离**：默认禁用网络，容器间无法通信

```python
# 用户 A 执行（在容器 A 中）
backend_a.execute("ps aux")  # 只看到容器 A 的进程

# 用户 B 执行（在容器 B 中）
backend_b.execute("ps aux")  # 只看到容器 B 的进程

# 用户 A 无法影响用户 B
backend_a.execute(":(){ :|:& };:")  # 只影响容器 A，不影响容器 B
```

### 潜在问题

| 问题 | 严重性 | 说明 |
|------|--------|------|
| 资源竞争 | ✅ 低 | 每个容器有独立限制 |
| 安全风险 | ✅ 低 | 容器隔离 |
| 文件冲突 | ✅ 无 | 完全隔离 |
| 容器数量 | ⚠️ 中 | 大量用户可能创建大量容器 |
| 启动延迟 | ⚠️ 中 | 每个用户启动容器需要 1-2 秒 |

---

## 对比总结

### 文件隔离

| Backend | 隔离级别 | 配置复杂度 | 安全性 |
|---------|---------|-----------|--------|
| StateSandboxBackend | ✅ 完全隔离（状态） | 简单 | ⚠️ 低 |
| FilesystemSandboxBackend | ⚠️ 目录隔离 | 中等 | ⚠️ 中 |
| DockerSandboxBackend | ✅ 完全隔离（容器） | 简单 | ✅ 高 |

### 命令执行隔离

| Backend | 进程隔离 | 资源隔离 | 网络隔离 |
|---------|---------|---------|---------|
| StateSandboxBackend | ❌ | ❌ | ❌ |
| FilesystemSandboxBackend | ❌ | ❌ | ❌ |
| DockerSandboxBackend | ✅ | ✅ | ✅ |

### 性能影响

| Backend | 并发用户数 | 性能影响 | 资源占用 |
|---------|-----------|---------|---------|
| StateSandboxBackend | 高 | 相互影响 | 低 |
| FilesystemSandboxBackend | 高 | 相互影响 | 低 |
| DockerSandboxBackend | 中 | 互不影响 | 高 |

---

## 推荐方案

### 方案 1: 单用户/开发环境

```python
# 使用 StateSandboxBackend
backend = lambda rt: StateSandboxBackend(rt)
```

**优点**：
- 最快
- 最简单
- 无需配置

**缺点**：
- 无安全保护

---

### 方案 2: 多用户/生产环境（推荐）

```python
# 为每个用户创建独立的 Docker 容器
def get_user_backend(user_id: str) -> DockerSandboxBackend:
    return DockerSandboxBackend(
        image="python:3.12-slim",
        memory_limit="512m",
        cpu_quota=50000,
        network_mode="none",
    )

# 使用时
backend = get_user_backend(current_user.id)
agent = create_agent(model, tools, middleware=[FilesystemMiddleware(backend=backend)])

# 使用完后清理
backend.cleanup()
```

**优点**：
- 完全隔离
- 安全
- 资源限制

**缺点**：
- 启动较慢
- 资源占用高

---

### 方案 3: 多用户/中等安全

```python
# 为每个用户创建独立的工作目录
def get_user_backend(user_id: str) -> FilesystemSandboxBackend:
    return FilesystemSandboxBackend(
        root_dir=f"/workspace/user_{user_id}",
        virtual_mode=True,
    )

# 使用时
backend = get_user_backend(current_user.id)
agent = create_agent(model, tools, middleware=[FilesystemMiddleware(backend=backend)])
```

**优点**：
- 快速
- 文件隔离
- 持久化

**缺点**：
- 命令执行无隔离
- 资源竞争

---

## 实现示例

### 示例 1: FastAPI 中为每个用户创建 Backend

```python
from fastapi import Depends, FastAPI
from app.backends import DockerSandboxBackend
from app.core.deps import get_current_user

app = FastAPI()

# 用户 Backend 缓存
user_backends: dict[str, DockerSandboxBackend] = {}

def get_user_backend(user = Depends(get_current_user)) -> DockerSandboxBackend:
    """为每个用户获取或创建 Backend"""
    user_id = str(user.id)

    if user_id not in user_backends:
        # 创建新的 Docker 容器
        backend = DockerSandboxBackend(
            image="python:3.12-slim",
            memory_limit="512m",
            cpu_quota=50000,
            network_mode="none",
        )
        user_backends[user_id] = backend

    return user_backends[user_id]

@app.post("/chat")
async def chat(
    message: str,
    backend: DockerSandboxBackend = Depends(get_user_backend),
):
    # 使用用户专属的 Backend
    agent = create_agent(
        model,
        tools=tools,
        middleware=[FilesystemMiddleware(backend=backend)]
    )
    result = await agent.ainvoke({"messages": [{"role": "user", "content": message}]})
    return result

@app.on_event("shutdown")
async def cleanup():
    """应用关闭时清理所有容器"""
    for backend in user_backends.values():
        backend.cleanup()
```

### 示例 2: 使用上下文管理器（推荐）

```python
@app.post("/chat")
async def chat(
    message: str,
    user = Depends(get_current_user),
):
    # 每次请求创建新容器，使用完自动清理
    with DockerSandboxBackend(
        memory_limit="512m",
        network_mode="none",
    ) as backend:
        agent = create_agent(
            model,
            tools=tools,
            middleware=[FilesystemMiddleware(backend=backend)]
        )
        result = await agent.ainvoke({"messages": [{"role": "user", "content": message}]})
        return result
    # 容器自动清理
```

### 示例 3: 容器池（高级）

```python
from asyncio import Queue

class DockerBackendPool:
    """Docker Backend 池，复用容器"""

    def __init__(self, size: int = 10):
        self.pool: Queue[DockerSandboxBackend] = Queue(maxsize=size)
        self.size = size
        self._initialize()

    def _initialize(self):
        """预创建容器"""
        for _ in range(self.size):
            backend = DockerSandboxBackend()
            self.pool.put_nowait(backend)

    async def acquire(self) -> DockerSandboxBackend:
        """获取容器"""
        return await self.pool.get()

    async def release(self, backend: DockerSandboxBackend):
        """归还容器"""
        # 清理容器内的文件
        backend.execute("rm -rf /workspace/*")
        await self.pool.put(backend)

    def cleanup(self):
        """清理所有容器"""
        while not self.pool.empty():
            backend = self.pool.get_nowait()
            backend.cleanup()

# 使用
pool = DockerBackendPool(size=10)

@app.post("/chat")
async def chat(message: str):
    backend = await pool.acquire()
    try:
        agent = create_agent(
            model,
            tools=tools,
            middleware=[FilesystemMiddleware(backend=backend)]
        )
        result = await agent.ainvoke({"messages": [{"role": "user", "content": message}]})
        return result
    finally:
        await pool.release(backend)
```

---

## 总结

### 选择建议

1. **开发/测试**：
   - 使用 `StateSandboxBackend`
   - 简单快速

2. **生产环境（少量用户）**：
   - 使用 `DockerSandboxBackend`
   - 每个用户一个容器
   - 完全隔离

3. **生产环境（大量用户）**：
   - 使用 `DockerSandboxBackend` + 容器池
   - 复用容器，减少启动开销
   - 定期清理

4. **生产环境（预算有限）**：
   - 使用 `FilesystemSandboxBackend`
   - 为每个用户创建独立目录
   - 启用虚拟模式
   - ⚠️ 注意：命令执行仍无隔离

### 关键要点

- ✅ **Docker 是最安全的选择**
- ⚠️ **Filesystem 需要手动配置用户目录**
- ⚠️ **State 和 Filesystem 的命令执行共享系统资源**
- ✅ **使用上下文管理器确保资源清理**
- ✅ **考虑使用容器池优化性能**
