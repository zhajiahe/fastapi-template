"""测试 DockerSandboxBackend 的功能"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from deepagents.middleware import FilesystemMiddleware  # noqa: E402
from langchain.agents import create_agent  # noqa: E402
from langchain_openai import ChatOpenAI  # noqa: E402

from app.backends import DockerSandboxBackend  # noqa: E402


async def test_docker_sandbox():
    """测试 DockerSandboxBackend 功能"""
    print("=" * 70)
    print("测试 DockerSandboxBackend")
    print("=" * 70)

    # 创建 Docker 沙箱后端
    print("\n[步骤 1] 创建 Docker 沙箱后端...")
    backend = DockerSandboxBackend(
        image="python:3.12-slim",
        memory_limit="512m",
        cpu_quota=50000,  # 50% of one core
        network_mode="none",  # 完全隔离网络
        working_dir="/workspace",
    )
    print(f"✓ 后端创建成功，ID: {backend.id}")

    try:
        # 测试 1: 容器创建
        print("\n[测试 1] 容器创建和启动")
        container = backend.container
        print(f"✓ 容器创建成功: {container.short_id}")
        print(f"  - 镜像: {backend.image}")
        print(f"  - 内存限制: {backend.memory_limit}")
        print(f"  - CPU 配额: {backend.cpu_quota}")
        print(f"  - 网络模式: {backend.network_mode}")

        # 测试 2: 命令执行
        print("\n[测试 2] 执行命令")
        result = backend.execute("echo 'Hello from Docker!'")
        print("✓ 命令执行成功")
        print(f"  - 输出: {result.output.strip()}")
        print(f"  - 退出码: {result.exit_code}")

        # 测试 3: Python 版本
        print("\n[测试 3] 获取 Python 版本")
        result = backend.execute("python --version")
        print(f"✓ Python 版本: {result.output.strip()}")

        # 测试 4: 文件写入
        print("\n[测试 4] 写入文件")
        write_result = backend.write("/workspace/test.txt", "Hello Docker!\nLine 2\nLine 3")
        if write_result.error:
            print(f"✗ 写入失败: {write_result.error}")
        else:
            print(f"✓ 文件写入成功: {write_result.path}")

        # 测试 5: 文件读取
        print("\n[测试 5] 读取文件")
        content = backend.read("/workspace/test.txt")
        print("✓ 文件读取成功:")
        print(content)

        # 测试 6: 使用 cat 命令验证文件
        print("\n[测试 6] 使用 cat 命令验证文件")
        result = backend.execute("cat /workspace/test.txt")
        print("✓ cat 命令输出:")
        print(result.output)

        # 测试 7: 文件编辑
        print("\n[测试 7] 编辑文件")
        edit_result = backend.edit("/workspace/test.txt", "Docker", "Container")
        if edit_result.error:
            print(f"✗ 编辑失败: {edit_result.error}")
        else:
            print(f"✓ 文件编辑成功，替换了 {edit_result.occurrences} 处")

        # 测试 8: 验证编辑结果
        print("\n[测试 8] 验证编辑结果")
        content = backend.read("/workspace/test.txt")
        print("✓ 编辑后的内容:")
        print(content)

        # 测试 9: 列出文件
        print("\n[测试 9] 列出工作目录文件")
        files = backend.ls_info("/workspace")
        print(f"✓ 找到 {len(files)} 个文件/目录:")
        for file in files:
            file_type = "目录" if file["is_dir"] else f"{file['size']} bytes"
            print(f"  - {file['path']} ({file_type})")

        # 测试 10: Python 脚本执行
        print("\n[测试 10] 创建并执行 Python 脚本")
        script_content = """#!/usr/bin/env python3
import sys
print(f"Python version: {sys.version}")
print("Hello from Python script!")
for i in range(5):
    print(f"Count: {i}")
"""
        backend.write("/workspace/script.py", script_content)
        result = backend.execute("python /workspace/script.py")
        print("✓ Python 脚本执行成功:")
        print(result.output)

        # 测试 11: 安全测试 - 网络隔离
        print("\n[测试 11] 安全测试 - 网络隔离")
        result = backend.execute("ping -c 1 8.8.8.8")
        if result.exit_code != 0:
            print("✓ 网络隔离正常工作（无法访问外网）")
        else:
            print("⚠ 警告: 网络隔离可能未生效")

        # 测试 12: 资源限制测试
        print("\n[测试 12] 资源限制测试")
        result = backend.execute("cat /sys/fs/cgroup/memory/memory.limit_in_bytes")
        print(f"✓ 内存限制: {result.output.strip()} bytes")

        print("\n" + "=" * 70)
        print("所有测试完成！")
        print("=" * 70)

    finally:
        # 清理容器
        print("\n[清理] 停止并删除容器...")
        backend.cleanup()
        print("✓ 清理完成")


async def test_docker_with_agent():
    """测试 DockerSandboxBackend 与 Agent 集成"""
    print("\n" + "=" * 70)
    print("测试 DockerSandboxBackend 与 Agent 集成")
    print("=" * 70)

    # 创建 Docker 沙箱后端
    backend = DockerSandboxBackend(
        image="python:3.12-slim",
        memory_limit="512m",
        network_mode="none",
    )

    try:
        # 创建 Agent
        print("\n[步骤 1] 创建 Agent...")
        model = ChatOpenAI(
            model="Qwen/Qwen3-8B",
            base_url="https://api.siliconflow.cn/v1",
            streaming=True,
        )

        agent = create_agent(
            model,
            tools=[],
            middleware=[FilesystemMiddleware(backend=backend)],
        )
        print("✓ Agent 创建成功")

        # 测试 Agent 使用文件系统
        print("\n[测试] Agent 使用文件系统工具")
        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": """
                        请执行以下任务：
                        1. 使用 write_file 创建 /workspace/hello.py，内容为一个打印 "Hello World" 的 Python 脚本
                        2. 使用 execute 工具执行这个脚本
                        3. 使用 ls 列出 /workspace 目录的文件
                        """,
                    }
                ]
            }
        )

        print("\n✓ Agent 执行完成")
        print(f"最后一条消息: {result['messages'][-1].content[:200]}...")

    finally:
        # 清理
        print("\n[清理] 停止并删除容器...")
        backend.cleanup()
        print("✓ 清理完成")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="测试 DockerSandboxBackend")
    parser.add_argument("--with-agent", action="store_true", help="同时测试 Agent 集成（需要 API key）")
    args = parser.parse_args()

    # 运行基础测试
    asyncio.run(test_docker_sandbox())

    # 可选：运行 Agent 集成测试
    if args.with_agent:
        asyncio.run(test_docker_with_agent())
