import { useEffect, useState } from 'react';
import request from '@/utils/request';
import { UserStatsResponse } from '@/api/aPIDoc';
import { MessageSquareIcon, FileTextIcon, ClockIcon } from 'lucide-react';

export const UserStats = () => {
  const [stats, setStats] = useState<UserStatsResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      setLoading(true);
      const response = await request.get('/conversations/users/stats');
      // 解析 BaseResponse 包装的数据
      if (response.data.success && response.data.data) {
        setStats(response.data.data);
      }
    } catch (error) {
      console.error('Failed to load stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="text-gray-600">加载统计信息...</div>
      </div>
    );
  }

  if (!stats) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold mb-4">使用统计</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="flex items-center gap-3 p-4 bg-blue-50 rounded-lg">
          <div className="p-2 bg-blue-100 rounded-lg">
            <MessageSquareIcon size={24} className="text-blue-600" />
          </div>
          <div>
            <div className="text-2xl font-bold text-blue-600">
              {stats.total_conversations}
            </div>
            <div className="text-sm text-gray-600">总会话数</div>
          </div>
        </div>

        <div className="flex items-center gap-3 p-4 bg-green-50 rounded-lg">
          <div className="p-2 bg-green-100 rounded-lg">
            <FileTextIcon size={24} className="text-green-600" />
          </div>
          <div>
            <div className="text-2xl font-bold text-green-600">
              {stats.total_messages}
            </div>
            <div className="text-sm text-gray-600">总消息数</div>
          </div>
        </div>

        <div className="flex items-center gap-3 p-4 bg-purple-50 rounded-lg">
          <div className="p-2 bg-purple-100 rounded-lg">
            <ClockIcon size={24} className="text-purple-600" />
          </div>
          <div>
            <div className="text-2xl font-bold text-purple-600">
              {stats.recent_conversations.length}
            </div>
            <div className="text-sm text-gray-600">最近会话</div>
          </div>
        </div>
      </div>

      {stats.recent_conversations.length > 0 && (
        <div className="mt-6">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">最近的会话</h3>
          <div className="space-y-2">
            {stats.recent_conversations.slice(0, 5).map((conv: any, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex-1 truncate">
                  <div className="text-sm font-medium text-gray-900 truncate">
                    {conv.title || '未命名会话'}
                  </div>
                  <div className="text-xs text-gray-500">
                    {conv.message_count || 0} 条消息
                  </div>
                </div>
                <div className="text-xs text-gray-400">
                  {new Date(conv.updated_at).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
