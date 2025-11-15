#!/bin/bash

# 前端部署到 FastAPI 的脚本

set -e

echo "🚀 部署前端到 FastAPI..."
echo ""

# 进入 web 目录
cd web

# 构建前端
echo "📦 构建前端..."
pnpm build

# 检查构建是否成功
if [ ! -d "dist" ]; then
    echo "❌ 构建失败！"
    exit 1
fi

echo "✅ 构建成功！"
echo ""
echo "📁 构建产物位于: web/dist/"
echo ""
echo "🎉 部署完成！"
echo ""
echo "后端已配置静态文件服务，重启后端即可访问前端："
echo "  访问地址: http://localhost:8000/web/"
echo ""
echo "重启后端命令："
echo "  cd .."
echo "  make dev"
