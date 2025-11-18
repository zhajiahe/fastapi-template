# 快速参考手册

## 🚀 常用命令

### 开发
```bash
pnpm run dev          # 启动开发服务器
pnpm run build        # 构建生产版本
pnpm run preview      # 预览生产构建
```

### 代码质量
```bash
pnpm run check        # 检查并自动修复格式和lint问题
pnpm run format       # 仅格式化代码
pnpm run lint         # 仅lint检查
```

### API 生成
```bash
pnpm run gen:apis     # 根据 OpenAPI 规范生成 API 客户端
```

### 依赖管理
```bash
pnpm install          # 安装依赖
pnpm add <package>    # 添加依赖
pnpm remove <package> # 移除依赖
pnpm update           # 更新依赖
```

## 📦 添加 UI 组件

```bash
# 查看所有可用组件
npx shadcn@latest add

# 添加特定组件
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add dialog
npx shadcn@latest add dropdown-menu
npx shadcn@latest add form
npx shadcn@latest add input
npx shadcn@latest add label
npx shadcn@latest add select
npx shadcn@latest add table
npx shadcn@latest add tabs
npx shadcn@latest add toast
```

## 🎨 样式工具

### Tailwind CSS 常用类

#### 布局
```tsx
// Flexbox
<div className="flex flex-col items-center justify-center gap-4">

// Grid
<div className="grid grid-cols-3 gap-4">

// 响应式
<div className="w-full md:w-1/2 lg:w-1/3">
```

#### 间距
```tsx
// Padding
<div className="p-4 px-6 py-2">

// Margin
<div className="m-4 mx-auto my-2">

// Gap
<div className="flex gap-4">
```

#### 颜色
```tsx
// 背景色
<div className="bg-primary bg-secondary bg-muted">

// 文本色
<span className="text-foreground text-muted-foreground">

// 边框色
<div className="border border-border">
```

#### 文本
```tsx
// 大小
<span className="text-xs text-sm text-base text-lg text-xl text-2xl">

// 粗细
<span className="font-normal font-medium font-semibold font-bold">

// 对齐
<div className="text-left text-center text-right">
```

#### 圆角
```tsx
<div className="rounded rounded-md rounded-lg rounded-full">
```

#### 阴影
```tsx
<div className="shadow shadow-md shadow-lg shadow-xl">
```

### CSS 变量（主题色）

```css
/* 在 src/index.css 中定义 */
:root {
  --primary: 150 30% 55%;
  --secondary: 150 15% 95%;
  --muted: 150 15% 95%;
  --accent: 150 15% 95%;
  --destructive: 0 84.2% 60.2%;
  --border: 150 20% 88%;
  --input: 150 20% 88%;
  --ring: 150 30% 55%;
}

/* 在组件中使用 */
<div className="bg-primary text-primary-foreground">
```

## 🔧 工具函数

### 日期格式化

```tsx
import { formatTime, formatDate } from '@/utils/date';

// 格式化时间 (HH:MM)
const time = formatTime('2024-01-01T10:30:00Z'); // "10:30"

// 格式化日期 (M/D)
const date = formatDate('2024-01-01T10:30:00Z'); // "1/1"
```

### 本地存储

```tsx
import { storage } from '@/utils/storage';

// 保存数据
storage.set('key', { data: 'value' });

// 读取数据
const data = storage.get('key');

// 删除数据
storage.remove('key');

// 清空所有数据
storage.clear();
```

### HTTP 请求

```tsx
import request from '@/utils/request';

// GET 请求
const response = await request.get('/api/users');

// POST 请求
const response = await request.post('/api/users', {
  name: 'John',
  email: 'john@example.com',
});

// PUT 请求
const response = await request.put('/api/users/1', {
  name: 'John Updated',
});

// DELETE 请求
const response = await request.delete('/api/users/1');
```

### 样式工具

```tsx
import { cn } from '@/lib/utils';

// 合并类名
const className = cn(
  'base-class',
  condition && 'conditional-class',
  'another-class'
);
```

## 📊 状态管理 (Zustand)

### 创建 Store

```tsx
// src/stores/appStore.ts
import { create } from 'zustand';

interface AppState {
  count: number;
  increment: () => void;
  decrement: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}));
```

### 使用 Store

```tsx
import { useAppStore } from '@/stores/appStore';

function Counter() {
  const { count, increment, decrement } = useAppStore();

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}
```

### 持久化 Store

```tsx
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      count: 0,
      increment: () => set((state) => ({ count: state.count + 1 })),
    }),
    {
      name: 'app-storage', // localStorage key
    }
  )
);
```

## 🎯 组件模式

### 基础组件

```tsx
interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary';
}

export const Button = ({ children, onClick, variant = 'primary' }: ButtonProps) => {
  return (
    <button
      onClick={onClick}
      className={cn(
        'px-4 py-2 rounded-lg',
        variant === 'primary' && 'bg-primary text-primary-foreground',
        variant === 'secondary' && 'bg-secondary text-secondary-foreground'
      )}
    >
      {children}
    </button>
  );
};
```

### 表单组件

```tsx
import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

interface FormData {
  name: string;
  email: string;
}

interface FormProps {
  onSubmit: (data: FormData) => void;
}

export const Form = ({ onSubmit }: FormProps) => {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        value={formData.name}
        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
        placeholder="姓名"
      />
      <Input
        type="email"
        value={formData.email}
        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        placeholder="邮箱"
      />
      <Button type="submit">提交</Button>
    </form>
  );
};
```

### 列表组件

```tsx
import { useEffect, useState } from 'react';
import request from '@/utils/request';

interface Item {
  id: string;
  name: string;
}

export const List = () => {
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await request.get('/api/items');
        setItems(response.data);
      } catch (error) {
        console.error('Failed to fetch items:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchItems();
  }, []);

  if (loading) return <div>加载中...</div>;

  return (
    <div className="space-y-2">
      {items.map((item) => (
        <div key={item.id} className="p-4 border rounded-lg">
          {item.name}
        </div>
      ))}
    </div>
  );
};
```

### 对话框组件

```tsx
import { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';

export const MyDialog = () => {
  const [open, setOpen] = useState(false);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>打开对话框</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>对话框标题</DialogTitle>
        </DialogHeader>
        <div>对话框内容</div>
      </DialogContent>
    </Dialog>
  );
};
```

## 🔐 认证模式

### 登录

```tsx
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';
import request from '@/utils/request';

export const Login = () => {
  const navigate = useNavigate();
  const setAuth = useAuthStore((state) => state.setAuth);

  const handleLogin = async (username: string, password: string) => {
    try {
      const response = await request.post('/auth/login', {
        username,
        password,
      });
      setAuth(response.data.token, response.data.user);
      navigate('/dashboard');
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    // 登录表单
  );
};
```

### 受保护的路由

```tsx
import { Navigate } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};
```

## 🎨 主题切换

```tsx
import { useThemeStore } from '@/stores/themeStore';
import { Button } from '@/components/ui/button';
import { MoonIcon, SunIcon } from 'lucide-react';

export const ThemeToggle = () => {
  const { theme, toggleTheme } = useThemeStore();

  return (
    <Button onClick={toggleTheme} variant="ghost" size="icon">
      {theme === 'dark' ? <SunIcon size={20} /> : <MoonIcon size={20} />}
    </Button>
  );
};
```

## 📱 响应式设计

### 断点

```tsx
// Tailwind 默认断点
sm: 640px   // 小屏幕
md: 768px   // 中等屏幕
lg: 1024px  // 大屏幕
xl: 1280px  // 超大屏幕
2xl: 1536px // 2倍超大屏幕

// 使用示例
<div className="w-full sm:w-1/2 md:w-1/3 lg:w-1/4">
```

### 移动端适配

```tsx
// 隐藏/显示
<div className="hidden md:block">桌面端显示</div>
<div className="block md:hidden">移动端显示</div>

// 布局切换
<div className="flex flex-col md:flex-row">
```

## 🔍 调试技巧

### React DevTools

```bash
# 安装浏览器扩展
Chrome: React Developer Tools
Firefox: React Developer Tools
```

### 控制台日志

```tsx
console.log('Debug:', data);
console.error('Error:', error);
console.warn('Warning:', warning);
console.table(arrayData);
```

### 性能分析

```tsx
import { Profiler } from 'react';

<Profiler id="MyComponent" onRender={(id, phase, actualDuration) => {
  console.log(`${id} (${phase}) took ${actualDuration}ms`);
}}>
  <MyComponent />
</Profiler>
```

## 📚 常用库推荐

### 数据获取
```bash
pnpm add @tanstack/react-query
```

### 表单处理
```bash
pnpm add react-hook-form zod @hookform/resolvers
```

### 日期处理
```bash
pnpm add date-fns
```

### 动画
```bash
pnpm add framer-motion
```

### 图标
```bash
pnpm add lucide-react  # 已包含
```

### 国际化
```bash
pnpm add i18next react-i18next
```

## 🐛 常见问题

### Q: 如何解决 CORS 问题？
A: 在 `vite.config.ts` 中配置代理：
```ts
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
```

### Q: 如何优化构建大小？
A:
1. 使用动态导入 `const Component = lazy(() => import('./Component'))`
2. 移除未使用的依赖
3. 启用代码分割

### Q: 如何处理环境变量？
A: 在 `.env` 文件中定义，使用 `import.meta.env.VITE_*` 访问

### Q: 如何添加 PWA 支持？
A:
```bash
pnpm add vite-plugin-pwa -D
```
