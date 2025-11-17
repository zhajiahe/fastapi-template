import { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import { UserIcon, BotIcon, CopyIcon, CheckIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useToast } from '@/hooks/use-toast';
import { ToolCallCard } from '@/components/ToolCallCard';
import { Message } from '@/stores/chatStore';
import { useUserSettingsStore } from '@/stores/userSettingsStore';
import 'highlight.js/styles/github-dark.css';

interface MessageListProps {
  messages: Message[];
}

export const MessageList = ({ messages }: MessageListProps) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [copiedId, setCopiedId] = useState<number | null>(null);
  const { toast } = useToast();
  const { settings } = useUserSettingsStore();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleCopy = (content: string, id: number) => {
    navigator.clipboard.writeText(content);
    setCopiedId(id);
    toast({
      title: '已复制',
      description: '消息内容已复制到剪贴板',
    });
    setTimeout(() => setCopiedId(null), 2000);
  };

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center bg-background">
        <div className="text-center">
          <BotIcon size={48} className="mx-auto mb-4 opacity-50 text-muted-foreground" />
          <p className="text-lg text-foreground">开始新的对话</p>
          <p className="text-sm mt-2 text-muted-foreground">输入消息开始聊天</p>
        </div>
      </div>
    );
  }

  return (
    <ScrollArea className="flex-1">
      <div className="px-4 py-6">
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.map((message) => (
            <div
              key={message.id}
              className="flex gap-4 items-start"
            >
              {/* 左侧头像区域 */}
              {(message.role === 'assistant' || message.role === 'ai') ? (
                <Avatar className="flex-shrink-0 w-8 h-8">
                  <AvatarFallback className="bg-primary text-primary-foreground">
                    <BotIcon size={16} />
                  </AvatarFallback>
                </Avatar>
              ) : (
                <div className="flex-shrink-0 w-8 h-8" />
              )}

              {/* 消息内容区域 */}
              <div className={`flex-1 ${message.role === 'user' ? 'flex justify-end' : ''}`}>
                <div className="max-w-[80%]">
                  <div
                    className={`rounded-lg px-4 py-3 ${
                      message.role === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted text-foreground'
                    }`}
                  >
                    {(message.role === 'assistant' || message.role === 'ai') ? (
                      <>
                        <div className="prose prose-sm max-w-none dark:prose-invert prose-pre:bg-gray-900 prose-pre:text-gray-100">
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            rehypePlugins={[rehypeHighlight]}
                          >
                            {message.content}
                          </ReactMarkdown>
                          {message.isStreaming && (
                            <span className="inline-block w-2 h-4 bg-muted-foreground animate-pulse ml-1" />
                          )}
                        </div>

                        {/* 工具调用显示 */}
                        {settings.show_tool_calls &&
                         message.metadata?.tool_calls &&
                         message.metadata.tool_calls.length > 0 && (
                          <div className="mt-2">
                            {message.metadata.tool_calls.map((toolCall, index) => (
                              <ToolCallCard key={index} toolCall={toolCall} />
                            ))}
                          </div>
                        )}
                      </>
                    ) : (
                      <div className="whitespace-pre-wrap">{message.content}</div>
                    )}
                  </div>

                  {/* 操作按钮 */}
                  {!message.isStreaming && (
                    <div className="flex items-center gap-2 mt-2">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleCopy(message.content, message.id)}
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
                    </div>
                  )}
                </div>
              </div>

              {/* 右侧头像区域 */}
              {message.role === 'user' ? (
                <Avatar className="flex-shrink-0 w-8 h-8">
                  <AvatarFallback className="bg-primary text-primary-foreground">
                    <UserIcon size={16} />
                  </AvatarFallback>
                </Avatar>
              ) : (
                <div className="flex-shrink-0 w-8 h-8" />
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>
    </ScrollArea>
  );
};
