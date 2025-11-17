import { useState, useRef, KeyboardEvent } from 'react';
import { SendIcon, StopCircleIcon, RotateCcwIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { useUserSettingsStore } from '@/stores/userSettingsStore';
import { useToast } from '@/hooks/use-toast';

interface ChatInputProps {
  onSend: (message: string) => void;
  onStop?: () => void;
  onReset?: () => void;
  disabled?: boolean;
  isSending?: boolean;
  showReset?: boolean;
}

export const ChatInput = ({ onSend, onStop, onReset, disabled, isSending, showReset }: ChatInputProps) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { settings, updateShowToolCalls } = useUserSettingsStore();
  const { toast } = useToast();

  const handleToggleToolCalls = async (checked: boolean) => {
    try {
      await updateShowToolCalls(checked);
      toast({
        title: '设置已更新',
        description: `工具调用显示已${checked ? '开启' : '关闭'}`,
      });
    } catch (error) {
      console.error('Failed to update tool calls setting:', error);
      toast({
        title: '更新失败',
        description: '无法更新工具调用显示设置',
        variant: 'destructive',
      });
    }
  };

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    // 自动调整高度
    e.target.style.height = 'auto';
    e.target.style.height = `${e.target.scrollHeight}px`;
  };

  return (
    <div className="border-t bg-card p-4">
      <div className="max-w-3xl mx-auto">
        <div className="flex items-end gap-2">
          {/* 工具调用显示开关 */}
          <div className="flex flex-col items-center gap-1 pb-2">
            <Switch
              id="show-tool-calls"
              checked={settings.show_tool_calls}
              onCheckedChange={handleToggleToolCalls}
              title="显示工具调用信息"
            />
            <Label htmlFor="show-tool-calls" className="text-xs text-muted-foreground cursor-pointer">
              工具
            </Label>
          </div>

          <Textarea
            ref={textareaRef}
            value={message}
            onChange={handleInput}
            onKeyDown={handleKeyDown}
            placeholder="输入消息... (Shift + Enter 换行)"
            disabled={disabled}
            className="flex-1 resize-none max-h-40 min-h-[60px]"
            rows={1}
          />
          {isSending ? (
            <Button
              onClick={onStop}
              variant="destructive"
              size="icon"
              className="h-[60px] w-[60px]"
              title="停止生成"
            >
              <StopCircleIcon size={24} />
            </Button>
          ) : (
            <Button
              onClick={handleSend}
              disabled={disabled || !message.trim()}
              size="icon"
              className="h-[60px] w-[60px]"
              title="发送消息"
            >
              <SendIcon size={24} />
            </Button>
          )}
          {showReset && onReset && (
            <Button
              onClick={onReset}
              variant="outline"
              size="icon"
              className="h-[60px] w-[60px]"
              title="重置对话"
            >
              <RotateCcwIcon size={24} />
            </Button>
          )}
        </div>
        <div className="mt-2 text-xs text-muted-foreground text-center">
          按 Enter 发送，Shift + Enter 换行
        </div>
      </div>
    </div>
  );
};
