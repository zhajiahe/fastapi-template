#!/bin/bash

# 部署测试脚本

echo "🧪 测试部署状态..."
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

BASE_URL="http://localhost:8000"

# 测试函数
test_endpoint() {
    local url=$1
    local name=$2

    status_code=$(curl -s -o /dev/null -w "%{http_code}" "$url")

    if [ "$status_code" -eq 200 ]; then
        echo -e "${GREEN}✅ $name${NC} - HTTP $status_code"
        return 0
    else
        echo -e "${RED}❌ $name${NC} - HTTP $status_code"
        return 1
    fi
}

# 运行测试
echo "测试后端 API..."
test_endpoint "$BASE_URL/" "根路径"
test_endpoint "$BASE_URL/health" "健康检查"
test_endpoint "$BASE_URL/docs" "API 文档"

echo ""
echo "测试前端..."
test_endpoint "$BASE_URL/web/" "前端首页"
test_endpoint "$BASE_URL/web/assets/index-Culy800d.js" "JS 资源"
test_endpoint "$BASE_URL/web/assets/index-DknxVqTm.css" "CSS 资源"

echo ""
echo "📊 测试完成！"
echo ""
echo "访问地址："
echo "  前端: ${YELLOW}http://localhost:8000/web/${NC}"
echo "  API 文档: ${YELLOW}http://localhost:8000/docs${NC}"
echo ""
echo "提示：请在浏览器中打开前端地址进行完整测试"
