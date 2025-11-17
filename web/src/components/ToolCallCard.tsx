import { useState } from 'react';
import { ChevronDownIcon, ChevronRightIcon, WrenchIcon } from 'lucide-react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ToolCall } from '@/stores/chatStore';

interface ToolCallCardProps {
  toolCall: ToolCall;
}

export const ToolCallCard = ({ toolCall }: ToolCallCardProps) => {
  const [isExpanded, setIsExpanded] = useState(false);

  // 解析参数（可能是字符串或对象）
  const parseArguments = () => {
    try {
      if (typeof toolCall.arguments === 'string') {
        return JSON.parse(toolCall.arguments);
      }
      return toolCall.input || toolCall.arguments || {};
    } catch {
      return toolCall.arguments || toolCall.input || {};
    }
  };

  const args = parseArguments();

  return (
    <Card className="my-2 border-l-4 border-l-blue-500 bg-blue-50/50 dark:bg-blue-950/20">
      <CardHeader className="p-3 pb-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <WrenchIcon size={16} className="text-blue-600 dark:text-blue-400" />
            <span className="text-sm font-semibold text-blue-700 dark:text-blue-300">
              工具调用: {toolCall.name}
            </span>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
            className="h-6 w-6 p-0"
          >
            {isExpanded ? (
              <ChevronDownIcon size={16} />
            ) : (
              <ChevronRightIcon size={16} />
            )}
          </Button>
        </div>
      </CardHeader>

      {isExpanded && (
        <CardContent className="p-3 pt-0 space-y-2">
          {/* 输入参数 */}
          {args && Object.keys(args).length > 0 && (
            <div>
              <div className="text-xs font-semibold text-muted-foreground mb-1">
                输入参数:
              </div>
              <pre className="text-xs bg-muted p-2 rounded overflow-x-auto">
                {JSON.stringify(args, null, 2)}
              </pre>
            </div>
          )}

          {/* 输出结果 */}
          {toolCall.output && (
            <div>
              <div className="text-xs font-semibold text-muted-foreground mb-1">
                输出结果:
              </div>
              <pre className="text-xs bg-muted p-2 rounded overflow-x-auto">
                {typeof toolCall.output === 'string'
                  ? toolCall.output
                  : JSON.stringify(toolCall.output, null, 2)}
              </pre>
            </div>
          )}
        </CardContent>
      )}
    </Card>
  );
};
