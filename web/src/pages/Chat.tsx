import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Sidebar } from '@/components/Sidebar';
import { MessageList } from '@/components/MessageList';
import { ChatInput } from '@/components/ChatInput';
import { SearchDialog } from '@/components/SearchDialog';
import { useAuthStore } from '@/stores/authStore';
import { useThemeStore } from '@/stores/themeStore';
import { useChat } from '@/hooks/useChat';
import { useConversations } from '@/hooks/useConversations';
import { LogOutIcon, SettingsIcon, SearchIcon, MoonIcon, SunIcon } from 'lucide-react';

export const Chat = () => {
  const navigate = useNavigate();
  const { isAuthenticated, user, clearAuth } = useAuthStore();
  const { theme, toggleTheme } = useThemeStore();
  const { messages, isSending, sendMessageStream, stopStreaming } = useChat();
  const { conversations, selectConversation, currentConversation, resetConversation } = useConversations();
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  const handleLogout = () => {
    clearAuth();
    navigate('/login');
  };

  const handleSelectConversation = async (threadId: string) => {
    const conversation = conversations.find((c) => c.thread_id === threadId);
    if (conversation) {
      await selectConversation(conversation);
    }
  };

  const handleResetCurrentConversation = async () => {
    if (!currentConversation) return;

    if (window.confirm('确定要重置当前对话吗？所有消息将被清空。')) {
      try {
        await resetConversation(currentConversation.thread_id);
      } catch (error) {
        console.error('Failed to reset conversation:', error);
      }
    }
  };

  // 快捷键支持
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        setIsSearchOpen(true);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="flex h-screen bg-white dark:bg-gray-900">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="h-16 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-6 bg-white dark:bg-gray-800">
          <h1 className="text-xl font-semibold text-gray-800 dark:text-gray-100">AI Agent</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600 dark:text-gray-300">
              欢迎，{user?.nickname || user?.username}
            </span>
            <button
              onClick={() => setIsSearchOpen(true)}
              className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              title="搜索 (Ctrl+K)"
            >
              <SearchIcon size={16} />
              <span>搜索</span>
            </button>
            <button
              onClick={toggleTheme}
              className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              title={theme === 'light' ? '切换到暗色模式' : '切换到亮色模式'}
            >
              {theme === 'light' ? <MoonIcon size={16} /> : <SunIcon size={16} />}
            </button>
            <Link
              to="/settings"
              className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <SettingsIcon size={16} />
              <span>设置</span>
            </Link>
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <LogOutIcon size={16} />
              <span>退出</span>
            </button>
          </div>
        </div>

        {/* Messages */}
        <MessageList messages={messages} />

        {/* Input */}
        <ChatInput
          onSend={sendMessageStream}
          onStop={stopStreaming}
          onReset={handleResetCurrentConversation}
          disabled={isSending}
          isSending={isSending}
          showReset={!!currentConversation}
        />
      </div>

      {/* Search Dialog */}
      <SearchDialog
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
        onSelectConversation={handleSelectConversation}
      />
    </div>
  );
};
