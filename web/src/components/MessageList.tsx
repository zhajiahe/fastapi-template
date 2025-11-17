import { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import { UserIcon, BotIcon, CopyIcon, CheckIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useToast } from '@/hooks/use-toast';
import { Message } from '@/stores/chatStore';
import { useUserSettingsStore } from '@/stores/userSettingsStore';
import 'highlight.js/styles/github-dark.css';

interface MessageListProps {
  messages: Message[];
}

// 扩展消息类型以支持工具调用消息
interface ExpandedMessage extends Message {
  isToolCall?: boolean;
  toolCall?: {
    name: string;
    arguments?: any;
    input?: any;
    output?: any;
  };
}

export const MessageList = ({ messages }: MessageListProps) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [copiedId, setCopiedId] = useState<number | null>(null);
  const [expandedToolCalls, setExpandedToolCalls] = useState<Set<number>>(new Set());
  const { toast } = useToast();
  const { settings } = useUserSettingsStore();

  const toggleToolCall = (id: number) => {
    setExpandedToolCalls(prev => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // 将消息展开，将工具调用作为独立的消息项
  const expandedMessages: ExpandedMessage[] = [];
  messages.forEach((message) => {
    // 如果是 AI 消息且有工具调用，先显示工具调用
    if ((message.role === 'assistant' || message.role === 'ai') &&
        settings.show_tool_calls &&
        message.metadata?.tool_calls &&
        message.metadata.tool_calls.length > 0) {
      // 添加工具调用消息
      message.metadata.tool_calls.forEach((toolCall, index) => {
        expandedMessages.push({
          ...message,
          id: message.id * 1000 + index, // 生成唯一 ID
          isToolCall: true,
          toolCall: toolCall,
        });
      });
    }
    // 然后添加原始消息
    expandedMessages.push(message);
  });

  useEffect(() => {
    scrollToBottom();
  }, [expandedMessages.length]);

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
      <div className="flex-1 flex items-center justify-center bg-background p-8">
        <div className="text-center animate-fade-in">
          <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mb-4 shadow-lg mx-auto">
            <BotIcon size={40} className="text-white" />
          </div>
          <h3 className="text-xl font-semibold mb-2">开始新的对话</h3>
          <p className="text-sm text-muted-foreground mb-6">
            输入消息开始与 AI 助手聊天
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-md mx-auto">
            <button className="p-3 border border-border rounded-lg hover:border-primary hover:bg-accent transition-all duration-200 text-left group">
              <p className="text-sm font-medium group-hover:text-primary transition-colors">💡 解释一个概念</p>
              <p className="text-xs text-muted-foreground mt-1">获取详细的解释和示例</p>
            </button>
            <button className="p-3 border border-border rounded-lg hover:border-primary hover:bg-accent transition-all duration-200 text-left group">
              <p className="text-sm font-medium group-hover:text-primary transition-colors">🔍 分析问题</p>
              <p className="text-xs text-muted-foreground mt-1">深入分析复杂问题</p>
            </button>
            <button className="p-3 border border-border rounded-lg hover:border-primary hover:bg-accent transition-all duration-200 text-left group">
              <p className="text-sm font-medium group-hover:text-primary transition-colors">✍️ 写作助手</p>
              <p className="text-xs text-muted-foreground mt-1">帮助撰写和改进文本</p>
            </button>
            <button className="p-3 border border-border rounded-lg hover:border-primary hover:bg-accent transition-all duration-200 text-left group">
              <p className="text-sm font-medium group-hover:text-primary transition-colors">💻 编程帮助</p>
              <p className="text-xs text-muted-foreground mt-1">代码编写和调试支持</p>
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <ScrollArea className="flex-1">
      <div className="px-4 py-6">
        <div className="max-w-3xl mx-auto space-y-6">
          {expandedMessages.map((message, index) => (
            <div
              key={message.id}
              className="flex gap-4 items-start animate-slide-up"
              style={{ animationDelay: `${index * 0.05}s` }}
            >
              {/* 左侧头像区域 */}
              {(message.role === 'assistant' || message.role === 'ai' || message.isToolCall) ? (
                <Avatar className="flex-shrink-0 w-10 h-10 ring-2 ring-primary/20 shadow-md">
                  <AvatarFallback className={message.isToolCall ? "bg-gradient-to-br from-orange-500 to-red-600" : "bg-gradient-to-br from-blue-500 to-purple-600"}>
                    {message.isToolCall ? "🔧" : <BotIcon size={20} className="text-white" />}
                  </AvatarFallback>
                </Avatar>
              ) : (
                <div className="flex-shrink-0 w-10 h-10" />
              )}

              {/* 消息内容区域 */}
              <div className={`flex-1 ${message.role === 'user' ? 'flex justify-end' : ''}`}>
                <div className="max-w-[80%]">
                  <div
                    className={`relative rounded-2xl px-4 py-3 shadow-md transition-all duration-200 hover:shadow-lg ${
                      message.role === 'user'
                        ? 'bg-gradient-to-br from-blue-500 to-purple-600 text-white'
                        : message.isToolCall
                        ? 'bg-orange-50 dark:bg-orange-950/30 text-foreground border-2 border-orange-300 dark:border-orange-700'
                        : 'bg-muted/50 dark:bg-muted text-foreground border border-border'
                    }`}
                  >
                    {/* AI消息添加左侧彩色边框指示器 */}
                    {(message.role === 'assistant' || message.role === 'ai') && !message.isToolCall && (
                      <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-blue-500 to-purple-500 rounded-l-2xl" />
                    )}
                    {/* 工具调用消息 */}
                    {message.isToolCall && message.toolCall ? (
                      <div className="space-y-2">
                        <button
                          onClick={() => toggleToolCall(message.id)}
                          className="w-full flex items-center justify-between text-orange-700 dark:text-orange-400 font-semibold hover:opacity-80 transition-opacity"
                        >
                          <div className="flex items-center gap-2">
                            <span className="text-lg">🔧</span>
                            <span>调用工具: {message.toolCall.name}</span>
                          </div>
                          <span className="text-sm">
                            {expandedToolCalls.has(message.id) ? '▼' : '▶'}
                          </span>
                        </button>
                        {expandedToolCalls.has(message.id) && (
                          <div className="space-y-2 animate-slide-up">
                            {(message.toolCall.arguments || message.toolCall.input) && (
                              <div>
                                <div className="text-sm text-muted-foreground mb-1">输入参数：</div>
                                <pre className="text-xs bg-muted p-2 rounded overflow-x-auto">
                                  {JSON.stringify(message.toolCall.arguments || message.toolCall.input, null, 2)}
                                </pre>
                              </div>
                            )}
                            {message.toolCall.output && (
                              <div>
                                <div className="text-sm text-muted-foreground mb-1">输出结果：</div>
                                <pre className="text-xs bg-muted p-2 rounded overflow-x-auto max-h-40">
                                  {typeof message.toolCall.output === 'string'
                                    ? message.toolCall.output
                                    : JSON.stringify(message.toolCall.output, null, 2)}
                                </pre>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    ) : (message.role === 'assistant' || message.role === 'ai') ? (
                      <>
                        <div className="prose prose-sm max-w-none dark:prose-invert prose-pre:bg-gray-900 prose-pre:text-gray-100">
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            rehypePlugins={[rehypeHighlight]}
                          >
                            {message.content}
                          </ReactMarkdown>
                          {message.isStreaming && (
                            <span className="inline-flex gap-1 ml-2 items-center">
                              <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                              <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                              <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                            </span>
                          )}
                        </div>
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
                <Avatar className="flex-shrink-0 w-10 h-10 ring-2 ring-primary/20 shadow-md">
                  <AvatarFallback className="bg-gradient-to-br from-blue-500 to-purple-600">
                    <UserIcon size={20} className="text-white" />
                  </AvatarFallback>
                </Avatar>
              ) : (
                <div className="flex-shrink-0 w-10 h-10" />
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>
    </ScrollArea>
  );
};
