import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import type { Message } from '@/stores/chatStore';
import { AIMessage } from './AIMessage';
import { ToolCallMessage } from './ToolCallMessage';
import { UserMessage } from './UserMessage';

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
  // 用户消息
  if (message.role === 'user') {
    return <UserMessage message={message} onCopy={onCopy} copiedId={copiedId} />;
  }

  // 工具调用消息
  if (message.isToolCall && message.toolCall) {
    return (
      <div className="max-w-3xl w-full mx-auto px-4 animate-slide-up">
        <div className="bg-orange-50 dark:bg-orange-950/30 rounded-grok px-5 py-4 text-foreground border border-orange-300 dark:border-orange-700">
          <ToolCallMessage toolCall={message.toolCall} messageId={message.id} />
        </div>
      </div>
    );
  }

  // AI 消息
  return <AIMessage message={message} onCopy={onCopy} copiedId={copiedId} />;
};
