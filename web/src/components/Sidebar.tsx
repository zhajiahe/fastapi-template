import { useState, useMemo } from 'react';
import { PlusIcon, MessageSquareIcon, TrashIcon, EditIcon, CheckIcon, XIcon, RotateCcwIcon, SearchIcon } from 'lucide-react';
import { useConversations } from '@/hooks/useConversations';
import { ConversationResponse } from '@/api/aPIDoc';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { useToast } from '@/hooks/use-toast';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';

export const Sidebar = () => {
  const {
    conversations,
    currentConversation,
    createConversation,
    selectConversation,
    updateConversationTitle,
    removeConversation,
    resetConversation,
  } = useConversations();
  const { toast } = useToast();

  const [editingId, setEditingId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [resetDialogOpen, setResetDialogOpen] = useState(false);
  const [targetConversationId, setTargetConversationId] = useState<string | null>(null);

  const handleCreateConversation = async () => {
    try {
      await createConversation();
    } catch (error) {
      console.error('Failed to create conversation:', error);
    }
  };

  const handleStartEdit = (conversation: ConversationResponse) => {
    setEditingId(conversation.thread_id);
    setEditTitle(conversation.title);
  };

  const handleSaveEdit = async (threadId: string) => {
    if (editTitle.trim()) {
      try {
        await updateConversationTitle(threadId, editTitle.trim());
        setEditingId(null);
      } catch (error) {
        console.error('Failed to update title:', error);
      }
    }
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setEditTitle('');
  };

  const handleDelete = async (threadId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setTargetConversationId(threadId);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = async () => {
    if (!targetConversationId) return;
    try {
      await removeConversation(targetConversationId);
      toast({
        title: '删除成功',
        description: '对话已删除',
      });
      setDeleteDialogOpen(false);
      setTargetConversationId(null);
    } catch (error) {
      console.error('Failed to delete conversation:', error);
      toast({
        title: '删除失败',
        description: '删除对话时发生错误',
        variant: 'destructive',
      });
    }
  };

  const handleReset = async (threadId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setTargetConversationId(threadId);
    setResetDialogOpen(true);
  };

  const confirmReset = async () => {
    if (!targetConversationId) return;
    try {
      await resetConversation(targetConversationId);
      toast({
        title: '重置成功',
        description: '对话已重置，所有消息已清空',
      });
      setResetDialogOpen(false);
      setTargetConversationId(null);
    } catch (error) {
      console.error('Failed to reset conversation:', error);
      toast({
        title: '重置失败',
        description: '重置对话时发生错误',
        variant: 'destructive',
      });
    }
  };

  // 过滤会话列表
  const filteredConversations = useMemo(() => {
    if (!searchQuery.trim()) {
      return conversations;
    }
    const query = searchQuery.toLowerCase();
    return conversations.filter((conv) =>
      conv.title.toLowerCase().includes(query)
    );
  }, [conversations, searchQuery]);

  return (
    <div className="w-64 border-r bg-card flex flex-col h-screen">
      {/* Header */}
      <div className="p-4 border-b space-y-3">
        <Button
          onClick={handleCreateConversation}
          className="w-full"
          size="sm"
        >
          <PlusIcon size={16} className="mr-2" />
          新建对话
        </Button>

        {/* 搜索框 */}
        <div className="relative">
          <SearchIcon size={16} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" />
          <Input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="搜索对话..."
            className="pl-9"
          />
        </div>
      </div>

      {/* Conversation List */}
      <ScrollArea className="flex-1">
        {filteredConversations.length === 0 && searchQuery && (
          <div className="p-4 text-center text-muted-foreground text-sm">
            没有找到匹配的对话
          </div>
        )}
        {filteredConversations.map((conversation) => (
          <div
            key={conversation.thread_id}
            className={`group relative px-3 py-3 cursor-pointer hover:bg-accent transition-colors ${
              currentConversation?.thread_id === conversation.thread_id
                ? 'bg-accent'
                : ''
            }`}
            onClick={() => selectConversation(conversation)}
          >
            {editingId === conversation.thread_id ? (
              <div className="flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
                <Input
                  type="text"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  className="flex-1 h-8 text-sm"
                  autoFocus
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      handleSaveEdit(conversation.thread_id);
                    } else if (e.key === 'Escape') {
                      handleCancelEdit();
                    }
                  }}
                />
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => handleSaveEdit(conversation.thread_id)}
                  className="h-8 w-8"
                >
                  <CheckIcon size={14} />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={handleCancelEdit}
                  className="h-8 w-8"
                >
                  <XIcon size={14} />
                </Button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <MessageSquareIcon size={16} className="flex-shrink-0 text-muted-foreground" />
                <span className="flex-1 text-sm truncate">{conversation.title}</span>
                <div className="hidden group-hover:flex items-center gap-1">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleStartEdit(conversation);
                    }}
                    className="h-6 w-6"
                    title="重命名"
                  >
                    <EditIcon size={12} />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(e) => handleReset(conversation.thread_id, e)}
                    className="h-6 w-6 text-yellow-600 hover:text-yellow-700"
                    title="重置对话"
                  >
                    <RotateCcwIcon size={12} />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(e) => handleDelete(conversation.thread_id, e)}
                    className="h-6 w-6 text-destructive hover:text-destructive"
                    title="删除"
                  >
                    <TrashIcon size={12} />
                  </Button>
                </div>
              </div>
            )}
          </div>
        ))}
      </ScrollArea>

      {/* Footer */}
      <div className="p-4 border-t">
        <div className="text-xs text-muted-foreground">
          {searchQuery ? (
            <>找到 {filteredConversations.length} 个对话</>
          ) : (
            <>共 {conversations.length} 个对话</>
          )}
        </div>
      </div>

      {/* Delete Dialog */}
      <Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>删除对话</DialogTitle>
            <DialogDescription>
              确定要删除这个对话吗？此操作不可恢复。
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDeleteDialogOpen(false)}>
              取消
            </Button>
            <Button variant="destructive" onClick={confirmDelete}>
              确定删除
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Reset Dialog */}
      <Dialog open={resetDialogOpen} onOpenChange={setResetDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>重置对话</DialogTitle>
            <DialogDescription>
              确定要重置这个对话吗？所有消息将被清空，此操作不可恢复。
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setResetDialogOpen(false)}>
              取消
            </Button>
            <Button variant="destructive" onClick={confirmReset}>
              确定重置
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};
