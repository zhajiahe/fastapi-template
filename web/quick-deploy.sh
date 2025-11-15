#!/bin/bash

# 快速部署脚本 - AI 聊天助手前端

set -e

echo "🚀 AI 聊天助手 - 快速部署脚本"
echo "================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 pnpm 是否安装
if ! command -v pnpm &> /dev/null; then
    echo -e "${RED}错误: pnpm 未安装${NC}"
    echo "请先安装 pnpm: npm install -g pnpm"
    exit 1
fi

# 1. 清理旧的构建产物
echo -e "${YELLOW}📦 清理旧的构建产物...${NC}"
rm -rf dist

# 2. 安装依赖
echo -e "${YELLOW}📥 安装依赖...${NC}"
pnpm install

# 3. 构建生产版本
echo -e "${YELLOW}🔨 构建生产版本...${NC}"
pnpm build

# 检查构建是否成功
if [ ! -d "dist" ]; then
    echo -e "${RED}❌ 构建失败！${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 构建成功！${NC}"
echo ""
echo "构建产物位于: $(pwd)/dist"
echo ""

# 询问部署方式
echo "请选择部署方式："
echo "1) 复制到 Nginx 目录"
echo "2) 复制到 FastAPI 静态目录"
echo "3) 仅构建，不部署"
echo ""
read -p "请输入选项 (1-3): " choice

case $choice in
    1)
        read -p "请输入 Nginx 目录路径 (例如: /var/www/ai-chat/web): " nginx_path

        if [ -z "$nginx_path" ]; then
            echo -e "${RED}错误: 路径不能为空${NC}"
            exit 1
        fi

        echo -e "${YELLOW}📂 创建目标目录...${NC}"
        sudo mkdir -p "$nginx_path"

        echo -e "${YELLOW}📋 复制文件...${NC}"
        sudo cp -r dist/* "$nginx_path/"

        echo -e "${YELLOW}🔐 设置权限...${NC}"
        sudo chown -R www-data:www-data "$nginx_path"
        sudo chmod -R 755 "$nginx_path"

        echo -e "${GREEN}✅ 部署到 Nginx 完成！${NC}"
        echo ""
        echo "下一步："
        echo "1. 配置 Nginx (参考 nginx.conf.example)"
        echo "2. 测试配置: sudo nginx -t"
        echo "3. 重启 Nginx: sudo systemctl restart nginx"
        ;;

    2)
        read -p "请输入 FastAPI 静态目录路径 (例如: ../static/web): " static_path

        if [ -z "$static_path" ]; then
            echo -e "${RED}错误: 路径不能为空${NC}"
            exit 1
        fi

        echo -e "${YELLOW}📂 创建目标目录...${NC}"
        mkdir -p "$static_path"

        echo -e "${YELLOW}📋 复制文件...${NC}"
        cp -r dist/* "$static_path/"

        echo -e "${GREEN}✅ 部署到 FastAPI 完成！${NC}"
        echo ""
        echo "下一步："
        echo "1. 确保 FastAPI 配置了静态文件服务"
        echo "2. 重启 FastAPI 服务"
        ;;

    3)
        echo -e "${GREEN}✅ 构建完成！${NC}"
        echo ""
        echo "构建产物位于: dist/"
        echo "您可以手动部署这些文件"
        ;;

    *)
        echo -e "${RED}无效的选项${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}🎉 部署流程完成！${NC}"
echo ""
echo "访问地址: http://your-domain.com/web/"
echo ""
echo "如有问题，请查看 DEPLOYMENT.md 文档"
