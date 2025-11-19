"""测试 StateSandboxBackend 的功能"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.agent import get_agent  # noqa: E402


async def test_execute_command():
    """测试命令执行功能"""
    print("=" * 60)
    print("测试 StateSandboxBackend 命令执行功能")
    print("=" * 60)

    # 创建 agent
    agent = await get_agent()

    # 测试1: 执行简单命令
    print("\n[测试 1] 执行 'echo Hello World'")
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "使用 execute 工具执行命令: echo 'Hello from StateSandboxBackend!'"}]}
    )
    print(f"结果: {result}")

    # 测试2: 列出文件
    print("\n[测试 2] 列出当前目录文件")
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "使用 execute 工具列出当前目录的文件 (ls -la)"}]}
    )
    print(f"结果: {result}")

    # 测试3: 获取 Python 版本
    print("\n[测试 3] 获取 Python 版本")
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "使用 execute 工具获取 Python 版本 (python --version)"}]}
    )
    print(f"结果: {result}")

    # 测试4: 文件系统操作
    print("\n[测试 4] 创建文件并读取")
    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "1. 使用 write_file 工具创建文件 /test.txt，内容为 'Hello World'\n2. 使用 read_file 工具读取 /test.txt\n3. 使用 execute 工具执行 'cat /test.txt' 验证文件内容",
                }
            ]
        }
    )
    print(f"结果: {result}")

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_execute_command())
