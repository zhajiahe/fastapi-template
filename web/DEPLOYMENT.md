# 部署指南

本文档介绍如何部署 AI 聊天助手前端应用。

## 📋 前置要求

- Node.js 18+ 或使用 pnpm
- Nginx（推荐）或其他 Web 服务器
- 后端 API 服务已启动

## 🚀 部署步骤

### 方案 1: 使用 Nginx 部署（推荐）

#### 1. 构建生产版本

```bash
cd web
pnpm install
pnpm build
```

构建完成后，产物位于 `dist/` 目录。

#### 2. 复制文件到 Web 服务器

```bash
# 创建目标目录
sudo mkdir -p /var/www/ai-chat/web

# 复制构建产物
sudo cp -r dist/* /var/www/ai-chat/web/

# 设置权限
sudo chown -R www-data:www-data /var/www/ai-chat
sudo chmod -R 755 /var/www/ai-chat
```

#### 3. 配置 Nginx

创建 Nginx 配置文件：

```bash
sudo nano /etc/nginx/sites-available/ai-chat
```

复制以下配置（参考 `nginx.conf.example`）：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location /web/ {
        alias /var/www/ai-chat/web/;
        try_files $uri $uri/ /web/index.html;

        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # SSE 支持
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 300s;
    }

    # 根路径重定向
    location = / {
        return 301 /web/;
    }
}
```

#### 4. 启用配置并重启 Nginx

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/ai-chat /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

#### 5. 验证部署

访问 `http://your-domain.com/web/` 检查是否正常运行。

### 方案 2: 使用 FastAPI 静态文件服务

如果后端配置了静态文件服务，可以直接将前端部署到后端：

#### 1. 构建前端

```bash
cd web
pnpm build
```

#### 2. 复制到后端静态目录

```bash
# 假设后端有 static 目录
mkdir -p ../static/web
cp -r dist/* ../static/web/
```

#### 3. 配置后端静态文件服务

在 FastAPI 主文件中添加：

```python
from fastapi.staticfiles import StaticFiles

app.mount("/web", StaticFiles(directory="static/web", html=True), name="web")
```

#### 4. 重启后端服务

```bash
cd ..
make restart
```

访问 `http://localhost:8000/web/` 验证。

### 方案 3: 使用 Docker 部署

#### 1. 创建 Dockerfile

```dockerfile
# 构建阶段
FROM node:18-alpine AS builder

WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install
COPY . .
RUN pnpm build

# 运行阶段
FROM nginx:alpine

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html/web

# 复制 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### 2. 构建并运行容器

```bash
docker build -t ai-chat-frontend .
docker run -d -p 80:80 ai-chat-frontend
```

## 🔧 配置说明

### 环境变量

如果需要配置不同的 API 地址，可以在构建前设置环境变量：

```bash
# .env.production
VITE_API_BASE_URL=https://api.your-domain.com/api/v1
```

然后重新构建：

```bash
pnpm build
```

### 代理配置

如果前端和后端不在同一域名下，需要配置 CORS：

后端配置示例：

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 性能优化

### 1. 启用 Gzip 压缩

Nginx 配置：

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript
           application/x-javascript application/xml+rss
           application/json application/javascript;
```

### 2. 启用浏览器缓存

```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 3. 使用 CDN

将静态资源上传到 CDN，修改 `vite.config.ts`：

```typescript
export default defineConfig({
  base: 'https://cdn.your-domain.com/web/',
  // ...
});
```

## 🔒 安全配置

### 1. HTTPS 配置

使用 Let's Encrypt 免费证书：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 2. 安全头配置

Nginx 添加安全头：

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
```

### 3. 限流配置

```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

location /api/ {
    limit_req zone=api_limit burst=20 nodelay;
    # ...
}
```

## 🐛 故障排查

### 问题 1: 页面空白

**原因**: base 路径配置不正确

**解决**: 检查 `vite.config.ts` 中的 `base` 配置是否与 Nginx 的 `location` 匹配。

### 问题 2: API 请求失败

**原因**: CORS 或代理配置问题

**解决**:
1. 检查后端 CORS 配置
2. 检查 Nginx 代理配置
3. 查看浏览器控制台错误信息

### 问题 3: 刷新页面 404

**原因**: SPA 路由未配置

**解决**: 确保 Nginx 配置了 `try_files $uri $uri/ /web/index.html;`

### 问题 4: 流式响应不工作

**原因**: Nginx 缓冲配置

**解决**: 添加以下配置：

```nginx
proxy_buffering off;
proxy_cache off;
proxy_read_timeout 300s;
```

## 📝 维护

### 更新部署

```bash
# 1. 拉取最新代码
git pull

# 2. 重新构建
cd web
pnpm install
pnpm build

# 3. 复制文件
sudo cp -r dist/* /var/www/ai-chat/web/

# 4. 清除浏览器缓存或使用版本号
```

### 日志查看

```bash
# Nginx 访问日志
sudo tail -f /var/log/nginx/access.log

# Nginx 错误日志
sudo tail -f /var/log/nginx/error.log
```

### 监控

建议使用以下工具监控应用：

- **Nginx 状态**: `nginx -t` 和 `systemctl status nginx`
- **应用性能**: Google Lighthouse
- **错误追踪**: Sentry 或类似服务

## 🎯 检查清单

部署前检查：

- [ ] 后端 API 已启动并可访问
- [ ] 前端构建成功（`pnpm build`）
- [ ] Nginx 配置正确（`nginx -t`）
- [ ] 文件权限正确
- [ ] CORS 配置正确
- [ ] HTTPS 证书有效（如果使用）
- [ ] 防火墙规则配置
- [ ] 域名 DNS 解析正确

部署后测试：

- [ ] 访问首页正常
- [ ] 登录功能正常
- [ ] 注册功能正常
- [ ] 发送消息正常
- [ ] 流式响应正常
- [ ] 会话管理正常
- [ ] 刷新页面正常
- [ ] 浏览器控制台无错误

## 📞 支持

如有问题，请查看：

1. 项目 README.md
2. 后端 API 文档
3. Nginx 官方文档
4. 提交 Issue

## 📄 许可证

MIT License
