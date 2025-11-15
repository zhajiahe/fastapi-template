import { useCallback, useEffect } from 'react';
import { useChatStore } from '@/stores/chatStore';
import request from '@/utils/request';
import {
  ConversationResponse,
  ConversationCreate,
  ConversationUpdate,
  MessageResponse,
} from '@/api/aPIDoc';

export const useConversations = () => {
  const {
    conversations,
    currentConversation,
    setConversations,
    addConversation,
    updateConversation,
    deleteConversation,
    setCurrentConversation,
    setMessages,
    setIsLoading,
  } = useChatStore();

  // 加载会话列表
  const loadConversations = useCallback(async () => {
    try {
      setIsLoading(true);
      const response = await request.get<ConversationResponse[]>('/conversations');
      setConversations(response.data);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    } finally {
      setIsLoading(false);
    }
  }, [setConversations, setIsLoading]);

  // 创建新会话
  const createConversation = useCallback(
    async (title?: string) => {
      try {
        const data: ConversationCreate = {
          title: title || '新对话',
        };
        const response = await request.post<ConversationResponse>('/conversations', data);
        addConversation(response.data);
        setCurrentConversation(response.data);
        return response.data;
      } catch (error) {
        console.error('Failed to create conversation:', error);
        throw error;
      }
    },
    [addConversation, setCurrentConversation]
  );

  // 选择会话
  const selectConversation = useCallback(
    async (conversation: ConversationResponse) => {
      try {
        setIsLoading(true);
        setCurrentConversation(conversation);

        // 加载会话消息
        const response = await request.get<MessageResponse[]>(
          `/conversations/${conversation.thread_id}/messages`
        );
        setMessages(response.data);
      } catch (error) {
        console.error('Failed to load messages:', error);
      } finally {
        setIsLoading(false);
      }
    },
    [setCurrentConversation, setMessages, setIsLoading]
  );

  // 更新会话标题
  const updateConversationTitle = useCallback(
    async (threadId: string, title: string) => {
      try {
        const data: ConversationUpdate = { title };
        await request.patch(`/conversations/${threadId}`, data);
        updateConversation(threadId, { title });
      } catch (error) {
        console.error('Failed to update conversation:', error);
        throw error;
      }
    },
    [updateConversation]
  );

  // 删除会话
  const removeConversation = useCallback(
    async (threadId: string) => {
      try {
        await request.delete(`/conversations/${threadId}`);
        deleteConversation(threadId);
      } catch (error) {
        console.error('Failed to delete conversation:', error);
        throw error;
      }
    },
    [deleteConversation]
  );

  // 重置会话
  const resetConversation = useCallback(
    async (threadId: string) => {
      try {
        await request.post(`/conversations/${threadId}/reset`);
        setMessages([]);
      } catch (error) {
        console.error('Failed to reset conversation:', error);
        throw error;
      }
    },
    [setMessages]
  );

  // 初始化时加载会话列表
  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  return {
    conversations,
    currentConversation,
    loadConversations,
    createConversation,
    selectConversation,
    updateConversationTitle,
    removeConversation,
    resetConversation,
  };
};
