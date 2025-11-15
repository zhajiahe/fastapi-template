import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';
import request from '@/utils/request';
import { UserSettingsResponse, UserSettingsUpdate, PasswordChange } from '@/api/aPIDoc';
import { ArrowLeftIcon, SaveIcon } from 'lucide-react';
import { UserStats } from '@/components/UserStats';

export const Settings = () => {
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuthStore();

  const [settings, setSettings] = useState<UserSettingsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // 表单数据
  const [formData, setFormData] = useState({
    default_model: '',
    default_temperature: 0.7,
    default_max_tokens: 2000,
    theme: 'light',
    language: 'zh-CN',
  });

  // 密码修改
  const [passwordData, setPasswordData] = useState({
    old_password: '',
    new_password: '',
    confirm_password: '',
  });

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    loadSettings();
  }, [isAuthenticated, navigate]);

  const loadSettings = async () => {
    try {
      setLoading(true);
      const response = await request.get<any>('/users/settings');
      if (response.data.success && response.data.data) {
        const data = response.data.data;
        setSettings(data);
        setFormData({
          default_model: data.default_model || '',
          default_temperature: data.default_temperature || 0.7,
          default_max_tokens: data.default_max_tokens || 2000,
          theme: data.theme || 'light',
          language: data.language || 'zh-CN',
        });
      }
    } catch (err) {
      console.error('Failed to load settings:', err);
      setError('加载设置失败');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveSettings = async () => {
    try {
      setSaving(true);
      setError('');
      setSuccess('');

      const updateData: UserSettingsUpdate = {
        default_model: formData.default_model || null,
        default_temperature: formData.default_temperature,
        default_max_tokens: formData.default_max_tokens,
        theme: formData.theme || null,
        language: formData.language || null,
      };

      await request.put('/users/settings', updateData);
      setSuccess('设置保存成功');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err: any) {
      setError(err.response?.data?.msg || '保存设置失败');
    } finally {
      setSaving(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (passwordData.new_password !== passwordData.confirm_password) {
      setError('两次输入的密码不一致');
      return;
    }

    if (passwordData.new_password.length < 6) {
      setError('新密码长度至少为 6 位');
      return;
    }

    try {
      setSaving(true);
      const data: PasswordChange = {
        old_password: passwordData.old_password,
        new_password: passwordData.new_password,
      };
      await request.post('/auth/reset-password', data);
      setSuccess('密码修改成功');
      setPasswordData({ old_password: '', new_password: '', confirm_password: '' });
      setTimeout(() => setSuccess(''), 3000);
    } catch (err: any) {
      setError(err.response?.data?.msg || '修改密码失败');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-gray-600">加载中...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="mb-6 flex items-center gap-4">
          <Link
            to="/chat"
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900"
          >
            <ArrowLeftIcon size={20} />
            <span>返回聊天</span>
          </Link>
          <h1 className="text-2xl font-bold text-gray-900">设置</h1>
        </div>

        {error && (
          <div className="mb-4 bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-4 bg-green-50 border border-green-400 text-green-700 px-4 py-3 rounded">
            {success}
          </div>
        )}

        {/* 用户统计 */}
        <UserStats />

        {/* 用户信息 */}
        <div className="bg-white rounded-lg shadow p-6 my-6">
          <h2 className="text-lg font-semibold mb-4">用户信息</h2>
          <div className="space-y-3">
            <div>
              <label className="text-sm text-gray-600">用户名</label>
              <div className="mt-1 text-gray-900">{user?.username}</div>
            </div>
            <div>
              <label className="text-sm text-gray-600">昵称</label>
              <div className="mt-1 text-gray-900">{user?.nickname}</div>
            </div>
            <div>
              <label className="text-sm text-gray-600">邮箱</label>
              <div className="mt-1 text-gray-900">{user?.email}</div>
            </div>
          </div>
        </div>

        {/* AI 设置 */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-lg font-semibold mb-4">AI 设置</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                默认模型
              </label>
              <input
                type="text"
                value={formData.default_model}
                onChange={(e) =>
                  setFormData({ ...formData, default_model: e.target.value })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="例如: Qwen/Qwen3-8B"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                温度 (Temperature): {formData.default_temperature}
              </label>
              <input
                type="range"
                min="0"
                max="2"
                step="0.1"
                value={formData.default_temperature}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    default_temperature: parseFloat(e.target.value),
                  })
                }
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>精确 (0)</span>
                <span>平衡 (1)</span>
                <span>创造 (2)</span>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                最大 Token 数
              </label>
              <input
                type="number"
                value={formData.default_max_tokens}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    default_max_tokens: parseInt(e.target.value),
                  })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                min="100"
                max="8000"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                主题
              </label>
              <select
                value={formData.theme}
                onChange={(e) => setFormData({ ...formData, theme: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="light">亮色</option>
                <option value="dark">暗色</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                语言
              </label>
              <select
                value={formData.language}
                onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="zh-CN">简体中文</option>
                <option value="en-US">English</option>
              </select>
            </div>

            <button
              onClick={handleSaveSettings}
              disabled={saving}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
            >
              <SaveIcon size={16} />
              <span>{saving ? '保存中...' : '保存设置'}</span>
            </button>
          </div>
        </div>

        {/* 修改密码 */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">修改密码</h2>
          <form onSubmit={handleChangePassword} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                当前密码
              </label>
              <input
                type="password"
                value={passwordData.old_password}
                onChange={(e) =>
                  setPasswordData({ ...passwordData, old_password: e.target.value })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                新密码
              </label>
              <input
                type="password"
                value={passwordData.new_password}
                onChange={(e) =>
                  setPasswordData({ ...passwordData, new_password: e.target.value })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                required
                minLength={6}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                确认新密码
              </label>
              <input
                type="password"
                value={passwordData.confirm_password}
                onChange={(e) =>
                  setPasswordData({ ...passwordData, confirm_password: e.target.value })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                required
                minLength={6}
              />
            </div>

            <button
              type="submit"
              disabled={saving}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
            >
              {saving ? '修改中...' : '修改密码'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
