import { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import { UserIcon, BotIcon, CopyIcon, CheckIcon } from 'lucide-react';
import 'highlight.js/styles/github-dark.css';

interface Message {
  id: number;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
  isStreaming?: boolean;
}

interface MessageListProps {
  messages: Message[];
}

export const MessageList = ({ messages }: MessageListProps) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [copiedId, setCopiedId] = useState<number | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleCopy = (content: string, id: number) => {
    navigator.clipboard.writeText(content);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-400 dark:text-gray-500 bg-white dark:bg-gray-900">
        <div className="text-center">
          <BotIcon size={48} className="mx-auto mb-4 opacity-50" />
          <p className="text-lg">开始新的对话</p>
          <p className="text-sm mt-2">输入消息开始聊天</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto px-4 py-6 bg-white dark:bg-gray-900">
      <div className="max-w-3xl mx-auto space-y-6">
        {messages.map((message) => (
          <div
            key={message.id}
            className="flex gap-4 items-start"
          >
            {/* 左侧头像区域 */}
            {(message.role === 'assistant' || message.role === 'ai') ? (
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-green-600 flex items-center justify-center">
                <BotIcon size={20} className="text-white" />
              </div>
            ) : (
              <div className="flex-shrink-0 w-8 h-8" />
            )}

            {/* 消息内容区域 */}
            <div className={`flex-1 ${message.role === 'user' ? 'flex justify-end' : ''}`}>
              <div className="max-w-[80%]">
                <div
                  className={`rounded-lg px-4 py-3 ${
                    message.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100'
                  }`}
                >
                  {(message.role === 'assistant' || message.role === 'ai') ? (
                    <div className="prose prose-sm max-w-none dark:prose-invert prose-pre:bg-gray-900 prose-pre:text-gray-100">
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        rehypePlugins={[rehypeHighlight]}
                      >
                        {message.content}
                      </ReactMarkdown>
                      {message.isStreaming && (
                        <span className="inline-block w-2 h-4 bg-gray-400 dark:bg-gray-500 animate-pulse ml-1" />
                      )}
                    </div>
                  ) : (
                    <div className="whitespace-pre-wrap">{message.content}</div>
                  )}
                </div>

                {/* 操作按钮 */}
                {!message.isStreaming && (
                  <div className="flex items-center gap-2 mt-2 text-xs text-gray-500 dark:text-gray-400">
                    <button
                      onClick={() => handleCopy(message.content, message.id)}
                      className="flex items-center gap-1 hover:text-gray-700 dark:hover:text-gray-200 transition-colors"
                      title="复制"
                    >
                      {copiedId === message.id ? (
                        <>
                          <CheckIcon size={14} />
                          <span>已复制</span>
                        </>
                      ) : (
                        <>
                          <CopyIcon size={14} />
                          <span>复制</span>
                        </>
                      )}
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* 右侧头像区域 */}
            {message.role === 'user' ? (
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
                <UserIcon size={20} className="text-white" />
              </div>
            ) : (
              <div className="flex-shrink-0 w-8 h-8" />
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};
