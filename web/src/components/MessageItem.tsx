import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import { UserIcon, BotIcon, CopyIcon, CheckIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Message } from '@/stores/chatStore';
import { formatTime } from '@/utils/date';
import { ToolCallMessage } from './ToolCallMessage';

interface MessageItemProps {
  message: Message & {
    isToolCall?: boolean;
    toolCall?: {
      name: string;
      arguments?: any;
      input?: any;
      output?: any;
    };
  };
  onCopy: (content: string, id: number) => void;
  copiedId: number | null;
}

export const MessageItem = ({ message, onCopy, copiedId }: MessageItemProps) => {
  return (
    <div className="flex gap-4 items-start animate-slide-up">
      {/* 左侧头像区域 */}
      {(message.role === 'assistant' || message.role === 'ai' || message.isToolCall) ? (
        <Avatar className="flex-shrink-0 w-10 h-10 ring-2 ring-primary/20 shadow-md">
          <AvatarFallback className={message.isToolCall ? "bg-gradient-to-br from-orange-500 to-red-600" : "bg-gradient-to-br from-emerald-400 to-slate-500"}>
            {message.isToolCall ? "🔧" : <BotIcon size={20} className="text-white" />}
          </AvatarFallback>
        </Avatar>
      ) : (
        <div className="flex-shrink-0 w-10 h-10" />
      )}

      {/* 消息内容区域 */}
      <div className={`flex-1 ${message.role === 'user' ? 'flex justify-end' : ''}`}>
        <div className={message.role === 'user' ? 'max-w-[85%] sm:max-w-[80%] md:max-w-[75%]' : 'max-w-[90%]'}>
          <div
            className={`relative rounded-2xl px-4 py-3 shadow-md transition-all duration-200 hover:shadow-lg ${
              message.role === 'user'
                ? 'bg-gradient-to-br from-emerald-400 to-slate-500 text-white'
                : message.isToolCall
                ? 'bg-orange-50 dark:bg-orange-950/30 text-foreground border-2 border-orange-300 dark:border-orange-700'
                : 'bg-muted/50 dark:bg-muted text-foreground border border-border'
            }`}
          >
            {/* 工具调用消息 */}
            {message.isToolCall && message.toolCall ? (
              <ToolCallMessage toolCall={message.toolCall} messageId={message.id} />
            ) : (message.role === 'assistant' || message.role === 'ai') ? (
              <>
                <div className="prose prose-base max-w-none dark:prose-invert prose-pre:bg-gray-900 prose-pre:text-gray-100 w-full">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    rehypePlugins={[rehypeHighlight]}
                  >
                    {message.content}
                  </ReactMarkdown>
                  {message.isStreaming && (
                    <span className="inline-flex gap-1 ml-2 items-center">
                      <span className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                      <span className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                      <span className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                    </span>
                  )}
                </div>
              </>
            ) : (
              <div className="whitespace-pre-wrap">{message.content}</div>
            )}
          </div>

          {/* 操作按钮和时间戳 - 工具调用消息不显示 */}
          {!message.isStreaming && !message.isToolCall && (
            <div className="flex items-center justify-between gap-2 mt-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onCopy(message.content, message.id)}
                className="h-6 text-xs text-muted-foreground"
                title="复制"
              >
                {copiedId === message.id ? (
                  <>
                    <CheckIcon size={12} className="mr-1" />
                    已复制
                  </>
                ) : (
                  <>
                    <CopyIcon size={12} className="mr-1" />
                    复制
                  </>
                )}
              </Button>
              {message.created_at && (
                <span className="text-xs text-muted-foreground" title={message.created_at}>
                  {formatTime(message.created_at)}
                </span>
              )}
            </div>
          )}
        </div>
      </div>

      {/* 右侧头像区域 */}
      {message.role === 'user' ? (
        <Avatar className="flex-shrink-0 w-10 h-10 ring-2 ring-primary/20 shadow-md">
          <AvatarFallback className="bg-gradient-to-br from-emerald-400 to-slate-500">
            <UserIcon size={20} className="text-white" />
          </AvatarFallback>
        </Avatar>
      ) : (
        <div className="flex-shrink-0 w-10 h-10" />
      )}
    </div>
  );
};
