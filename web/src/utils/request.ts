import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

// 创建 axios 实例
const request = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 从 localStorage 获取 token
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    // 检查 BaseResponse 格式的错误
    if (response.data && !response.data.success) {
      // 即使 HTTP 状态码是 200，但业务逻辑失败
      const error: any = new Error(response.data.msg || '请求失败');
      error.response = {
        data: response.data,
        status: response.data.code,
      };
      return Promise.reject(error);
    }
    return response;
  },
  async (error: AxiosError<any>) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // 如果是 401 错误且未重试过
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // 尝试使用 refresh token 刷新
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          // TODO: 实现 refresh token 逻辑
          // const response = await axios.post('/api/v1/auth/refresh', { refresh_token: refreshToken });
          // localStorage.setItem('access_token', response.data.access_token);
          // return request(originalRequest);
        }
      } catch (refreshError) {
        // Refresh token 也失效，清除本地存储并跳转到登录页
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    // 增强错误信息，从 BaseResponse 中提取 msg
    if (error.response?.data?.msg) {
      error.message = error.response.data.msg;
    }

    return Promise.reject(error);
  }
);

export default request;
