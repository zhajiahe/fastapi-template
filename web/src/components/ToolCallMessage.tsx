import { useState } from 'react';

interface ToolCall {
  name: string;
  arguments?: any;
  input?: any;
  output?: any;
}

interface ToolCallMessageProps {
  toolCall: ToolCall;
  messageId: number;
}

export const ToolCallMessage = ({ toolCall, messageId }: ToolCallMessageProps) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="space-y-3">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between text-orange-700 dark:text-orange-300 font-medium hover:opacity-80 transition-opacity"
      >
        <div className="flex items-center gap-3">
          <span className="text-xl">🔧</span>
          <div className="text-left">
            <div className="font-semibold">{toolCall.name}</div>
            {!isExpanded && (toolCall.arguments || toolCall.input) && (
              <div className="text-xs text-orange-600 dark:text-orange-400 truncate max-w-md">
                {JSON.stringify(toolCall.arguments || toolCall.input)}
              </div>
            )}
          </div>
        </div>
        <span className="text-sm ml-2">{isExpanded ? '▼' : '▶'}</span>
      </button>

      {isExpanded && (
        <div className="space-y-3 animate-slide-up pt-2 border-t border-orange-200 dark:border-orange-800">
          {(toolCall.arguments || toolCall.input) && (
            <div>
              <div className="text-sm font-medium text-orange-700 dark:text-orange-300 mb-2">输入参数</div>
              <pre className="text-xs bg-white dark:bg-orange-900/20 p-3 rounded-lg overflow-x-auto border border-orange-200 dark:border-orange-800">
                {JSON.stringify(toolCall.arguments || toolCall.input, null, 2)}
              </pre>
            </div>
          )}
          {toolCall.output && (
            <div>
              <div className="text-sm font-medium text-orange-700 dark:text-orange-300 mb-2">输出结果</div>
              <pre className="text-xs bg-white dark:bg-orange-900/20 p-3 rounded-lg overflow-x-auto max-h-60 border border-orange-200 dark:border-orange-800">
                {typeof toolCall.output === 'string' ? toolCall.output : JSON.stringify(toolCall.output, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
