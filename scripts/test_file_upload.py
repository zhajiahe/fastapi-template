"""
测试文件上传 API

验证文件上传、列表、读取、删除功能
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import httpx  # noqa: E402


async def test_file_upload_api():
    """测试文件上传 API"""
    print("=" * 60)
    print("测试文件上传 API")
    print("=" * 60)

    # 首先需要登录获取 token
    base_url = "http://localhost:8000/api/v1"

    async with httpx.AsyncClient() as client:
        # 1. 登录获取 token
        print("\n" + "=" * 60)
        print("步骤 1: 登录获取 token")
        print("=" * 60)

        login_data = {"username": "testuser", "password": "test123"}

        try:
            response = await client.post(f"{base_url}/auth/login", params=login_data)
            response.raise_for_status()
            result = response.json()

            if not result.get("success"):
                print(f"❌ 登录失败: {result.get('msg')}")
                print("提示: 请先运行 'uv run python scripts/create_superuser.py' 创建管理员账户")
                return False

            access_token = result["data"]["access_token"]
            print(f"✅ 登录成功，获取到 token: {access_token[:20]}...")

        except httpx.HTTPStatusError as e:
            print(f"❌ 登录失败: {e}")
            print("提示: 请确保后端服务正在运行 (make dev)")
            return False
        except Exception as e:
            print(f"❌ 登录失败: {e}")
            return False

        # 设置认证头
        headers = {"Authorization": f"Bearer {access_token}"}

        # 2. 上传文本文件
        print("\n" + "=" * 60)
        print("步骤 2: 上传文本文件")
        print("=" * 60)

        test_content = "Hello, this is a test file!\nLine 2\nLine 3"
        files = {"file": ("test.txt", test_content, "text/plain")}

        try:
            response = await client.post(f"{base_url}/files/upload", headers=headers, files=files)
            response.raise_for_status()
            result = response.json()

            if result.get("success"):
                print(f"✅ 文件上传成功: {result['data']['filename']}")
                print(f"   路径: {result['data']['path']}")
                print(f"   大小: {result['data']['size']} bytes")
            else:
                print(f"❌ 文件上传失败: {result.get('msg')}")
                return False

        except Exception as e:
            print(f"❌ 文件上传失败: {e}")
            return False

        # 3. 列出文件
        print("\n" + "=" * 60)
        print("步骤 3: 列出文件")
        print("=" * 60)

        try:
            response = await client.get(f"{base_url}/files/list", headers=headers)
            response.raise_for_status()
            result = response.json()

            if result.get("success"):
                files_list = result["data"]["files"]
                print(f"✅ 获取文件列表成功，共 {result['data']['total']} 个文件:")
                for file_info in files_list:
                    print(f"   - {file_info['filename']} ({file_info['size']} bytes)")
            else:
                print(f"❌ 获取文件列表失败: {result.get('msg')}")

        except Exception as e:
            print(f"❌ 获取文件列表失败: {e}")

        # 4. 读取文件
        print("\n" + "=" * 60)
        print("步骤 4: 读取文件")
        print("=" * 60)

        try:
            response = await client.get(f"{base_url}/files/read/test.txt", headers=headers)
            response.raise_for_status()
            result = response.json()

            if result.get("success"):
                content = result["data"]["content"]
                print("✅ 读取文件成功:")
                print(f"   内容:\n{content}")
            else:
                print(f"❌ 读取文件失败: {result.get('msg')}")

        except Exception as e:
            print(f"❌ 读取文件失败: {e}")

        # 5. 上传第二个文件
        print("\n" + "=" * 60)
        print("步骤 5: 上传第二个文件")
        print("=" * 60)

        test_content2 = "This is another test file."
        files2 = {"file": ("test2.txt", test_content2, "text/plain")}

        try:
            response = await client.post(f"{base_url}/files/upload", headers=headers, files=files2)
            response.raise_for_status()
            result = response.json()

            if result.get("success"):
                print(f"✅ 第二个文件上传成功: {result['data']['filename']}")
            else:
                print(f"❌ 第二个文件上传失败: {result.get('msg')}")

        except Exception as e:
            print(f"❌ 第二个文件上传失败: {e}")

        # 6. 再次列出文件
        print("\n" + "=" * 60)
        print("步骤 6: 再次列出文件")
        print("=" * 60)

        try:
            response = await client.get(f"{base_url}/files/list", headers=headers)
            response.raise_for_status()
            result = response.json()

            if result.get("success"):
                files_list = result["data"]["files"]
                print(f"✅ 获取文件列表成功，共 {result['data']['total']} 个文件:")
                for file_info in files_list:
                    print(f"   - {file_info['filename']} ({file_info['size']} bytes)")

                if result["data"]["total"] >= 2:
                    print("✅ 文件数量正确")
                else:
                    print("❌ 文件数量不正确")

            else:
                print(f"❌ 获取文件列表失败: {result.get('msg')}")

        except Exception as e:
            print(f"❌ 获取文件列表失败: {e}")

        # 7. 删除文件
        print("\n" + "=" * 60)
        print("步骤 7: 删除文件")
        print("=" * 60)

        try:
            response = await client.delete(f"{base_url}/files/test.txt", headers=headers)
            response.raise_for_status()
            result = response.json()

            if result.get("success"):
                print(f"✅ 删除文件成功: {result['data']['filename']}")
            else:
                print(f"❌ 删除文件失败: {result.get('msg')}")

        except Exception as e:
            print(f"❌ 删除文件失败: {e}")

        # 8. 验证文件已删除
        print("\n" + "=" * 60)
        print("步骤 8: 验证文件已删除")
        print("=" * 60)

        try:
            response = await client.get(f"{base_url}/files/list", headers=headers)
            response.raise_for_status()
            result = response.json()

            if result.get("success"):
                files_list = result["data"]["files"]
                print(f"✅ 获取文件列表成功，共 {result['data']['total']} 个文件:")
                for file_info in files_list:
                    print(f"   - {file_info['filename']}")

                # 检查 test.txt 是否已删除
                filenames = [f["filename"] for f in files_list]
                if "test.txt" not in filenames:
                    print("✅ test.txt 已成功删除")
                else:
                    print("❌ test.txt 仍然存在")

                if "test2.txt" in filenames:
                    print("✅ test2.txt 仍然存在（未被误删）")
                else:
                    print("❌ test2.txt 被误删了")

            else:
                print(f"❌ 获取文件列表失败: {result.get('msg')}")

        except Exception as e:
            print(f"❌ 获取文件列表失败: {e}")

        print("\n" + "=" * 60)
        print("🎉 文件上传 API 测试完成")
        print("=" * 60)
        return True


if __name__ == "__main__":
    try:
        success = asyncio.run(test_file_upload_api())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n测试被中断")
        sys.exit(1)
