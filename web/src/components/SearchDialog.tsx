import { useState } from 'react';
import { SearchIcon, XIcon } from 'lucide-react';
import request from '@/utils/request';
import { SearchRequest, SearchResponse } from '@/api/aPIDoc';

interface SearchDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectConversation: (threadId: string) => void;
}

export const SearchDialog = ({ isOpen, onClose, onSelectConversation }: SearchDialogProps) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;

    try {
      setLoading(true);
      setSearched(true);
      const data: SearchRequest = {
        query: query.trim(),
        skip: 0,
        limit: 20,
      };
      const response = await request.post<SearchResponse>('/conversations/search', data);
      setResults(response.data.results || []);
    } catch (error) {
      console.error('Search failed:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    } else if (e.key === 'Escape') {
      onClose();
    }
  };

  const handleSelectResult = (threadId: string) => {
    onSelectConversation(threadId);
    onClose();
    setQuery('');
    setResults([]);
    setSearched(false);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-start justify-center pt-20 z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4">
        {/* Header */}
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <SearchIcon size={20} className="text-gray-400" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="搜索会话和消息..."
              className="flex-1 text-lg outline-none"
              autoFocus
            />
            <button
              onClick={onClose}
              className="p-1 hover:bg-gray-100 rounded transition-colors"
            >
              <XIcon size={20} />
            </button>
          </div>
        </div>

        {/* Results */}
        <div className="max-h-96 overflow-y-auto p-4">
          {loading && (
            <div className="text-center text-gray-500 py-8">
              搜索中...
            </div>
          )}

          {!loading && searched && results.length === 0 && (
            <div className="text-center text-gray-500 py-8">
              没有找到匹配的结果
            </div>
          )}

          {!loading && !searched && (
            <div className="text-center text-gray-400 py-8">
              输入关键词并按 Enter 搜索
            </div>
          )}

          {!loading && results.length > 0 && (
            <div className="space-y-3">
              {results.map((result, index) => (
                <div
                  key={index}
                  onClick={() => handleSelectResult(result.thread_id)}
                  className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
                >
                  <div className="font-medium text-gray-900 mb-1">
                    {result.title || '未命名会话'}
                  </div>
                  {result.content && (
                    <div className="text-sm text-gray-600 line-clamp-2">
                      {result.content}
                    </div>
                  )}
                  <div className="flex items-center gap-4 mt-2 text-xs text-gray-400">
                    {result.role && (
                      <span className="px-2 py-1 bg-gray-100 rounded">
                        {result.role === 'user' ? '用户' : '助手'}
                      </span>
                    )}
                    {result.created_at && (
                      <span>{new Date(result.created_at).toLocaleString()}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200 bg-gray-50 text-xs text-gray-500 flex items-center justify-between">
          <div>
            <kbd className="px-2 py-1 bg-white border border-gray-300 rounded">Enter</kbd> 搜索
            <span className="mx-2">·</span>
            <kbd className="px-2 py-1 bg-white border border-gray-300 rounded">Esc</kbd> 关闭
          </div>
          {results.length > 0 && (
            <div>找到 {results.length} 个结果</div>
          )}
        </div>
      </div>
    </div>
  );
};
