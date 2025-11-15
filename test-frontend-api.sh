#!/bin/bash

# 前端 API 测试脚本

set -e

echo "🧪 测试前端 API 调用..."
echo ""

BASE_URL="http://localhost:8000/api/v1"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. 测试注册
echo -e "${YELLOW}1. 测试注册...${NC}"
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "frontendtest",
    "email": "frontend@test.com",
    "nickname": "前端测试",
    "password": "test123456"
  }')

if echo "$REGISTER_RESPONSE" | grep -q '"success":true'; then
    echo -e "${GREEN}✅ 注册成功${NC}"
else
    echo -e "${RED}❌ 注册失败${NC}"
    echo "$REGISTER_RESPONSE" | python3 -m json.tool
fi

echo ""

# 2. 测试登录
echo -e "${YELLOW}2. 测试登录...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login?username=frontendtest&password=test123456")

if echo "$LOGIN_RESPONSE" | grep -q '"success":true'; then
    echo -e "${GREEN}✅ 登录成功${NC}"

    # 提取 token
    ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])")
    echo "Access Token: ${ACCESS_TOKEN:0:50}..."
else
    echo -e "${RED}❌ 登录失败${NC}"
    echo "$LOGIN_RESPONSE" | python3 -m json.tool
    exit 1
fi

echo ""

# 3. 测试获取用户信息
echo -e "${YELLOW}3. 测试获取用户信息...${NC}"
ME_RESPONSE=$(curl -s -X GET "$BASE_URL/auth/me" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$ME_RESPONSE" | grep -q '"success":true'; then
    echo -e "${GREEN}✅ 获取用户信息成功${NC}"
    echo "$ME_RESPONSE" | python3 -m json.tool | grep -E "(username|nickname|email)"
else
    echo -e "${RED}❌ 获取用户信息失败${NC}"
    echo "$ME_RESPONSE" | python3 -m json.tool
fi

echo ""

# 4. 测试创建会话
echo -e "${YELLOW}4. 测试创建会话...${NC}"
CONV_RESPONSE=$(curl -s -X POST "$BASE_URL/conversations" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "测试会话"}')

if echo "$CONV_RESPONSE" | grep -q '"thread_id"'; then
    echo -e "${GREEN}✅ 创建会话成功${NC}"
    THREAD_ID=$(echo "$CONV_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['thread_id'])")
    echo "Thread ID: $THREAD_ID"
else
    echo -e "${RED}❌ 创建会话失败${NC}"
    echo "$CONV_RESPONSE" | python3 -m json.tool
fi

echo ""
echo -e "${GREEN}🎉 API 测试完成！${NC}"
echo ""
echo "前端应该可以正常使用这些 API 了。"
echo "请在浏览器中打开 http://localhost:8000/web/ 测试前端功能。"
