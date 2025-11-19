"""
测试多用户隔离效果

验证不同用户拥有独立的工作目录
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.backends import FilesystemSandboxBackend  # noqa: E402


async def test_multi_user_isolation():
    """测试多用户文件系统隔离"""
    print("=" * 60)
    print("测试多用户文件系统隔离")
    print("=" * 60)

    # 模拟两个不同的用户
    user1_id = 1001
    user2_id = 1002

    # 为用户1创建 Backend
    backend1 = FilesystemSandboxBackend(
        root_dir=f"/tmp/{user1_id}",
        virtual_mode=True,
    )

    # 为用户2创建 Backend
    backend2 = FilesystemSandboxBackend(
        root_dir=f"/tmp/{user2_id}",
        virtual_mode=True,
    )

    print(f"\n✅ 用户1工作目录: {backend1.cwd}")
    print(f"✅ 用户2工作目录: {backend2.cwd}")

    # 测试1: 用户1创建文件
    print("\n" + "=" * 60)
    print("测试1: 用户1创建文件 user1.txt")
    print("=" * 60)
    backend1.write("user1.txt", "This is user 1's file")
    content1 = backend1.read("user1.txt")
    print(f"✅ 用户1读取 user1.txt: {content1}")

    # 测试2: 用户2创建同名文件
    print("\n" + "=" * 60)
    print("测试2: 用户2创建同名文件 user1.txt")
    print("=" * 60)
    backend2.write("user1.txt", "This is user 2's file")
    content2 = backend2.read("user1.txt")
    print(f"✅ 用户2读取 user1.txt: {content2}")

    # 测试3: 验证文件隔离
    print("\n" + "=" * 60)
    print("测试3: 验证文件隔离")
    print("=" * 60)
    content1_again = backend1.read("user1.txt")
    print(f"✅ 用户1再次读取 user1.txt: {content1_again}")

    # 检查内容是否包含预期文本（忽略行号前缀）
    if "This is user 1's file" in content1_again and "This is user 2's file" in content2:
        print("✅ 文件隔离成功！用户1和用户2的文件互不影响")
    else:
        print("❌ 文件隔离失败！")
        return False

    # 测试4: 用户1执行命令
    print("\n" + "=" * 60)
    print("测试4: 用户1执行命令")
    print("=" * 60)
    result1 = backend1.execute("pwd")
    print(f"✅ 用户1执行 pwd: {result1.output.strip()}")
    result1_ls = backend1.execute("ls -la")
    print(f"✅ 用户1执行 ls -la:\n{result1_ls.output}")

    # 测试5: 用户2执行命令
    print("\n" + "=" * 60)
    print("测试5: 用户2执行命令")
    print("=" * 60)
    result2 = backend2.execute("pwd")
    print(f"✅ 用户2执行 pwd: {result2.output.strip()}")
    result2_ls = backend2.execute("ls -la")
    print(f"✅ 用户2执行 ls -la:\n{result2_ls.output}")

    # 测试6: 用户1列出文件（使用 execute）
    print("\n" + "=" * 60)
    print("测试6: 用户1列出文件")
    print("=" * 60)
    result1_files = backend1.execute("ls -1")
    files1 = result1_files.output.strip().split("\n")
    print(f"✅ 用户1的文件列表: {files1}")

    # 测试7: 用户2列出文件（使用 execute）
    print("\n" + "=" * 60)
    print("测试7: 用户2列出文件")
    print("=" * 60)
    result2_files = backend2.execute("ls -1")
    files2 = result2_files.output.strip().split("\n")
    print(f"✅ 用户2的文件列表: {files2}")

    # 测试8: 用户2尝试删除所有文件
    print("\n" + "=" * 60)
    print("测试8: 用户2删除所有文件（模拟危险操作）")
    print("=" * 60)
    result2_rm = backend2.execute("rm -f *")
    print(f"✅ 用户2执行 rm -f *: exit_code={result2_rm.exit_code}")
    result2_files_after = backend2.execute("ls -1")
    files2_after = result2_files_after.output.strip().split("\n") if result2_files_after.output.strip() else []
    print(f"✅ 用户2删除后的文件列表: {files2_after}")

    # 测试9: 验证用户1的文件未受影响
    print("\n" + "=" * 60)
    print("测试9: 验证用户1的文件未受影响")
    print("=" * 60)
    result1_files_after = backend1.execute("ls -1")
    files1_after = result1_files_after.output.strip().split("\n")
    print(f"✅ 用户1的文件列表（用户2删除后）: {files1_after}")

    if "user1.txt" in files1_after:
        print("✅ 用户1的文件未受影响！隔离成功")
    else:
        print("❌ 用户1的文件受到影响！隔离失败")
        return False

    # 最终验证
    print("\n" + "=" * 60)
    print("最终验证")
    print("=" * 60)
    content1_final = backend1.read("user1.txt")
    print(f"✅ 用户1最终读取 user1.txt: {content1_final}")

    if "This is user 1's file" in content1_final:
        print("\n" + "=" * 60)
        print("🎉 所有测试通过！多用户隔离功能正常工作")
        print("=" * 60)
        return True
    else:
        print("\n❌ 测试失败")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_multi_user_isolation())
    sys.exit(0 if success else 1)
