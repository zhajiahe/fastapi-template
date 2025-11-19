"""
测试文件后端功能

验证 FilesystemSandboxBackend 的文件操作功能
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.backends import FilesystemSandboxBackend  # noqa: E402


def test_file_backend():
    """测试文件后端功能"""
    print("=" * 60)
    print("测试文件后端功能")
    print("=" * 60)

    # 创建测试用户的后端
    user_id = 9999
    backend = FilesystemSandboxBackend(
        root_dir=f"/tmp/{user_id}",
        virtual_mode=False,  # 使用实际文件系统
    )

    print(f"\n✅ 用户工作目录: {backend.cwd}")

    # 测试1: 写入文件
    print("\n" + "=" * 60)
    print("测试1: 写入文件")
    print("=" * 60)

    test_content = "Hello, this is a test file!\nLine 2\nLine 3"
    backend.write("test.txt", test_content)
    print("✅ 写入文件 test.txt 成功")

    # 测试2: 读取文件
    print("\n" + "=" * 60)
    print("测试2: 读取文件")
    print("=" * 60)

    content = backend.read("test.txt")
    print("✅ 读取文件 test.txt 成功:")
    print(content)

    if "Hello, this is a test file!" in content:
        print("✅ 文件内容正确")
    else:
        print("❌ 文件内容不正确")
        return False

    # 测试3: 列出文件
    print("\n" + "=" * 60)
    print("测试3: 列出文件")
    print("=" * 60)

    result = backend.execute("ls -lh")
    print("✅ 列出文件:")
    print(result.output)

    # 测试4: 写入第二个文件
    print("\n" + "=" * 60)
    print("测试4: 写入第二个文件")
    print("=" * 60)

    backend.write("test2.txt", "This is another test file.")
    print("✅ 写入文件 test2.txt 成功")

    # 测试5: 列出所有文件
    print("\n" + "=" * 60)
    print("测试5: 列出所有文件")
    print("=" * 60)

    result = backend.execute("ls -1")
    files = result.output.strip().split("\n")
    print(f"✅ 文件列表: {files}")

    if "test.txt" in files and "test2.txt" in files:
        print("✅ 文件列表正确")
    else:
        print("❌ 文件列表不正确")
        return False

    # 测试6: 删除文件
    print("\n" + "=" * 60)
    print("测试6: 删除文件")
    print("=" * 60)

    result = backend.execute("rm -f test.txt")
    print(f"✅ 删除文件 test.txt: exit_code={result.exit_code}")

    # 测试7: 验证文件已删除
    print("\n" + "=" * 60)
    print("测试7: 验证文件已删除")
    print("=" * 60)

    result = backend.execute("ls -1")
    files = result.output.strip().split("\n") if result.output.strip() else []
    print(f"✅ 文件列表: {files}")

    if "test.txt" not in files and "test2.txt" in files:
        print("✅ test.txt 已删除，test2.txt 仍存在")
    else:
        print("❌ 文件删除验证失败")
        return False

    # 测试8: 写入二进制文件（模拟）
    print("\n" + "=" * 60)
    print("测试8: 写入二进制内容")
    print("=" * 60)

    # 使用 Path 直接写入
    binary_path = Path(backend.cwd) / "binary_test.bin"
    binary_content = b"\x00\x01\x02\x03\x04\x05"
    binary_path.write_bytes(binary_content)
    print(f"✅ 写入二进制文件: {binary_path}")

    # 验证文件存在
    result = backend.execute("ls -lh binary_test.bin")
    print(f"✅ 文件信息:\n{result.output}")

    # 清理测试文件
    print("\n" + "=" * 60)
    print("清理测试文件")
    print("=" * 60)

    backend.execute("rm -rf *")
    print("✅ 清理完成")

    print("\n" + "=" * 60)
    print("🎉 所有测试通过！文件后端功能正常工作")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_file_backend()
    sys.exit(0 if success else 1)
