# AI Agent - 前端应用

这是一个基于 React + TypeScript + Vite 构建的现代化 AI 聊天应用前端。

## 功能特性

- ✅ **用户认证**：登录、注册、自动 token 刷新
- ✅ **实时聊天**：支持流式和非流式响应
- ✅ **会话管理**：创建、删除、重命名会话
- ✅ **Markdown 渲染**：支持代码高亮、列表、引用等
- ✅ **响应式设计**：适配桌面和移动设备
- ✅ **状态管理**：使用 Zustand 进行全局状态管理
- ✅ **类型安全**：完整的 TypeScript 类型支持

## 技术栈

- **React 18**: UI 框架
- **TypeScript**: 类型安全
- **Vite**: 构建工具
- **React Router**: 路由管理
- **Zustand**: 状态管理
- **Axios**: HTTP 客户端
- **React Markdown**: Markdown 渲染
- **Tailwind CSS**: 样式框架
- **Lucide React**: 图标库

## 项目结构

```
web/
├── src/
│   ├── api/                    # API 类型定义（自动生成）
│   │   └── aPIDoc.ts
│   ├── components/             # UI 组件
│   │   ├── Sidebar.tsx         # 侧边栏（会话列表）
│   │   ├── MessageList.tsx     # 消息列表
│   │   └── ChatInput.tsx       # 消息输入框
│   ├── pages/                  # 页面组件
│   │   ├── Login.tsx           # 登录页
│   │   ├── Register.tsx        # 注册页
│   │   └── Chat.tsx            # 聊天主页
│   ├── stores/                 # 状态管理
│   │   ├── authStore.ts        # 认证状态
│   │   └── chatStore.ts        # 聊天状态
│   ├── hooks/                  # 自定义 Hooks
│   │   ├── useChat.ts          # 聊天逻辑
│   │   └── useConversations.ts # 会话管理
│   ├── utils/                  # 工具函数
│   │   ├── request.ts          # Axios 实例
│   │   └── storage.ts          # 本地存储
│   ├── App.tsx                 # 应用根组件
│   ├── main.tsx                # 应用入口
│   └── index.css               # 全局样式
├── index.html                  # HTML 模板
├── package.json                # 依赖配置
├── vite.config.ts              # Vite 配置
├── tailwind.config.ts          # Tailwind 配置
└── tsconfig.json               # TypeScript 配置
```

## 快速开始

### 1. 安装依赖

```bash
pnpm install
```

### 2. 启动后端服务

确保后端服务已经启动并运行在 `http://localhost:8000`

```bash
# 在项目根目录
cd ..
make dev
```

### 3. 启动开发服务器

```bash
pnpm dev
```

应用将在 `http://localhost:5173/web/` 启动

### 4. 构建生产版本

```bash
pnpm build
```

构建产物将输出到 `dist/` 目录

### 5. 预览生产版本

```bash
pnpm preview
```

## API 类型生成

当后端 API 发生变化时，可以重新生成 TypeScript 类型定义：

```bash
# 确保后端服务正在运行
pnpm gen:apis
```

这将从 `http://localhost:8000/openapi.json` 获取最新的 API 定义并生成类型文件。

## 使用说明

### 登录

1. 访问 `/login` 页面
2. 输入用户名和密码
3. 点击"登录"按钮

### 注册

1. 访问 `/register` 页面
2. 填写用户信息（用户名、邮箱、昵称、密码）
3. 点击"注册"按钮
4. 注册成功后跳转到登录页

### 聊天

1. 登录后自动跳转到聊天页面
2. 点击"新建对话"创建新会话
3. 在输入框中输入消息，按 Enter 发送
4. 支持 Shift + Enter 换行
5. 点击停止按钮可以中断流式响应

### 会话管理

- **创建会话**：点击侧边栏的"新建对话"按钮
- **选择会话**：点击侧边栏的会话项
- **重命名会话**：悬停在会话上，点击编辑图标
- **删除会话**：悬停在会话上，点击删除图标

## 开发指南

### 添加新页面

1. 在 `src/pages/` 创建新的页面组件
2. 在 `src/App.tsx` 中添加路由

### 添加新组件

1. 在 `src/components/` 创建组件文件
2. 导出组件供其他文件使用

### 添加新的状态

1. 在 `src/stores/` 创建新的 store
2. 使用 Zustand 的 `create` 函数定义状态和操作

### 添加新的 API 调用

1. 使用 `src/utils/request.ts` 中的 axios 实例
2. 或者使用 `src/api/aPIDoc.ts` 中自动生成的 API 函数

## 环境变量

可以在 `.env` 文件中配置环境变量：

```env
# API 基础路径（可选，默认使用 /api/v1）
VITE_API_BASE_URL=/api/v1
```

## 代理配置

开发环境下，API 请求会被代理到后端服务器：

```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

## 部署

### 部署到 Nginx

1. 构建生产版本：`pnpm build`
2. 将 `dist/` 目录的内容复制到 Nginx 的 web 目录
3. 配置 Nginx：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location /web/ {
        alias /path/to/dist/;
        try_files $uri $uri/ /web/index.html;
    }

    # API 代理
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 部署到 FastAPI 静态文件服务

后端已经配置了静态文件服务，可以直接将构建产物放到后端的静态目录：

```bash
# 构建前端
pnpm build

# 复制到后端静态目录（如果配置了）
cp -r dist/* ../static/
```

## 常见问题

### Q: 登录后刷新页面需要重新登录？

A: 检查浏览器的 localStorage 是否被清除，或者 token 是否过期。

### Q: API 请求返回 401 错误？

A: 检查 token 是否有效，或者后端认证配置是否正确。

### Q: 流式响应不工作？

A: 确保后端支持 SSE（Server-Sent Events），并且浏览器支持 EventSource。

### Q: 样式不生效？

A: 检查 Tailwind CSS 配置是否正确，确保 `index.css` 已经导入。

## 许可证

MIT License
