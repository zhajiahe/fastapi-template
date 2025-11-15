import { useState } from 'react';
import { PlusIcon, MessageSquareIcon, TrashIcon, EditIcon, CheckIcon, XIcon } from 'lucide-react';
import { useConversations } from '@/hooks/useConversations';
import { ConversationResponse } from '@/api/aPIDoc';

export const Sidebar = () => {
  const {
    conversations,
    currentConversation,
    createConversation,
    selectConversation,
    updateConversationTitle,
    removeConversation,
  } = useConversations();

  const [editingId, setEditingId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState('');

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
    if (window.confirm('确定要删除这个对话吗？')) {
      try {
        await removeConversation(threadId);
      } catch (error) {
        console.error('Failed to delete conversation:', error);
      }
    }
  };

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col h-screen">
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <button
          onClick={handleCreateConversation}
          className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors"
        >
          <PlusIcon size={20} />
          <span>新建对话</span>
        </button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto">
        {conversations.map((conversation) => (
          <div
            key={conversation.thread_id}
            className={`group relative px-3 py-3 cursor-pointer hover:bg-gray-800 transition-colors ${
              currentConversation?.thread_id === conversation.thread_id
                ? 'bg-gray-800'
                : ''
            }`}
            onClick={() => selectConversation(conversation)}
          >
            {editingId === conversation.thread_id ? (
              <div className="flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
                <input
                  type="text"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  className="flex-1 px-2 py-1 bg-gray-700 rounded text-sm"
                  autoFocus
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      handleSaveEdit(conversation.thread_id);
                    } else if (e.key === 'Escape') {
                      handleCancelEdit();
                    }
                  }}
                />
                <button
                  onClick={() => handleSaveEdit(conversation.thread_id)}
                  className="p-1 hover:bg-gray-600 rounded"
                >
                  <CheckIcon size={16} />
                </button>
                <button
                  onClick={handleCancelEdit}
                  className="p-1 hover:bg-gray-600 rounded"
                >
                  <XIcon size={16} />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <MessageSquareIcon size={16} className="flex-shrink-0" />
                <span className="flex-1 text-sm truncate">{conversation.title}</span>
                <div className="hidden group-hover:flex items-center gap-1">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleStartEdit(conversation);
                    }}
                    className="p-1 hover:bg-gray-700 rounded"
                  >
                    <EditIcon size={14} />
                  </button>
                  <button
                    onClick={(e) => handleDelete(conversation.thread_id, e)}
                    className="p-1 hover:bg-gray-700 rounded text-red-400"
                  >
                    <TrashIcon size={14} />
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-700">
        <div className="text-xs text-gray-400">
          共 {conversations.length} 个对话
        </div>
      </div>
    </div>
  );
};
