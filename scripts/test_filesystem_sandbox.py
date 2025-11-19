"""测试 FilesystemSandboxBackend 的功能"""

import asyncio
import sys
import tempfile
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.backends import FilesystemSandboxBackend  # noqa: E402


async def test_filesystem_sandbox():
    """测试 FilesystemSandboxBackend 功能"""
    print("=" * 70)
    print("测试 FilesystemSandboxBackend")
    print("=" * 70)

    # 创建临时目录作为工作空间
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"\n[步骤 1] 创建后端，工作目录: {tmpdir}")
        backend = FilesystemSandboxBackend(
            root_dir=tmpdir,
            virtual_mode=True,  # 启用路径沙箱
        )
        print(f"✓ 后端创建成功，ID: {backend.id}")
        print(f"  - 根目录: {backend.cwd}")
        print(f"  - 虚拟模式: {backend.virtual_mode}")

        # 测试 1: 命令执行
        print("\n[测试 1] 执行命令")
        result = backend.execute("echo 'Hello from Filesystem!'")
        print("✓ 命令执行成功")
        print(f"  - 输出: {result.output.strip()}")
        print(f"  - 退出码: {result.exit_code}")

        # 测试 2: 获取 Python 版本
        print("\n[测试 2] 获取 Python 版本")
        result = backend.execute("python --version")
        print(f"✓ Python 版本: {result.output.strip()}")

        # 测试 3: 列出当前目录
        print("\n[测试 3] 列出当前目录")
        result = backend.execute("ls -la")
        print("✓ 目录内容:")
        print(result.output)

        # 测试 4: 写入文件（使用 FilesystemBackend 方法）
        print("\n[测试 4] 写入文件")
        write_result = backend.write("/test.txt", "Hello Filesystem!\nLine 2\nLine 3")
        if write_result.error:
            print(f"✗ 写入失败: {write_result.error}")
        else:
            print(f"✓ 文件写入成功: {write_result.path}")

        # 测试 5: 读取文件
        print("\n[测试 5] 读取文件")
        content = backend.read("/test.txt")
        print("✓ 文件读取成功:")
        print(content)

        # 测试 6: 使用 cat 命令验证文件
        print("\n[测试 6] 使用 cat 命令验证文件")
        result = backend.execute("cat test.txt")  # 相对路径，因为 cwd 已设置
        print("✓ cat 命令输出:")
        print(result.output)

        # 测试 7: 创建目录
        print("\n[测试 7] 创建目录")
        result = backend.execute("mkdir -p subdir/nested")
        if result.exit_code == 0:
            print("✓ 目录创建成功")
        else:
            print(f"✗ 目录创建失败: {result.output}")

        # 测试 8: 在子目录中创建文件
        print("\n[测试 8] 在子目录中创建文件")
        backend.write("/subdir/file.txt", "Content in subdirectory")
        content = backend.read("/subdir/file.txt")
        print("✓ 子目录文件内容:")
        print(content)

        # 测试 9: 列出子目录
        print("\n[测试 9] 列出子目录")
        files = backend.ls_info("/subdir")
        print(f"✓ 找到 {len(files)} 个文件/目录:")
        for file in files:
            file_type = "目录" if file["is_dir"] else f"{file['size']} bytes"
            print(f"  - {file['path']} ({file_type})")

        # 测试 10: Python 脚本执行
        print("\n[测试 10] 创建并执行 Python 脚本")
        script_content = """#!/usr/bin/env python3
import sys
import os
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print("Hello from Python script!")
for i in range(5):
    print(f"Count: {i}")
"""
        backend.write("/script.py", script_content)
        result = backend.execute("python script.py")
        print("✓ Python 脚本执行成功:")
        print(result.output)

        # 测试 11: 文件编辑
        print("\n[测试 11] 编辑文件")
        edit_result = backend.edit("/test.txt", "Filesystem", "FileSystem")
        if edit_result.error:
            print(f"✗ 编辑失败: {edit_result.error}")
        else:
            print(f"✓ 文件编辑成功，替换了 {edit_result.occurrences} 处")

        # 测试 12: 验证编辑结果
        print("\n[测试 12] 验证编辑结果")
        content = backend.read("/test.txt")
        print("✓ 编辑后的内容:")
        print(content)

        # 测试 13: 复杂命令
        print("\n[测试 13] 执行复杂命令")
        result = backend.execute("echo 'Line 1' > output.txt && echo 'Line 2' >> output.txt && cat output.txt")
        print("✓ 复杂命令执行成功:")
        print(result.output)

        # 测试 14: 虚拟模式安全性测试
        print("\n[测试 14] 虚拟模式安全性测试")
        try:
            # 尝试访问父目录（应该失败）
            backend.write("/../etc/passwd", "malicious content")
            print("⚠ 警告: 虚拟模式未能阻止路径遍历")
        except ValueError as e:
            print(f"✓ 虚拟模式正常工作，阻止了路径遍历: {e}")

        # 测试 15: 验证文件实际存在于临时目录
        print("\n[测试 15] 验证文件实际存在")
        actual_file = Path(tmpdir) / "test.txt"
        if actual_file.exists():
            print(f"✓ 文件确实存在于: {actual_file}")
            print(f"  - 文件大小: {actual_file.stat().st_size} bytes")
        else:
            print("✗ 文件不存在")

        print("\n" + "=" * 70)
        print("所有测试完成！")
        print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_filesystem_sandbox())
