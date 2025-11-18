import { create } from 'zustand';
import request from '@/utils/request';

interface UserSettings {
  show_tool_calls: boolean;
  llm_model?: string;
  max_tokens?: number;
  config?: Record<string, any>;
  context?: Record<string, any>;
}

interface UserSettingsState {
  settings: UserSettings;
  loading: boolean;
  error: string | null;
  loadSettings: () => Promise<void>;
  updateShowToolCalls: (show: boolean) => Promise<void>;
}

export const useUserSettingsStore = create<UserSettingsState>((set, get) => ({
  settings: {
    show_tool_calls: true, // 默认值
  },
  loading: false,
  error: null,

  loadSettings: async () => {
    set({ loading: true, error: null });
    try {
      const response = await request.get<any>('/users/settings');
      if (response.data.success && response.data.data) {
        const data = response.data.data;
        const settingsJson = data.settings || {};
        set({
          settings: {
            show_tool_calls: settingsJson.show_tool_calls !== undefined ? settingsJson.show_tool_calls : true,
            llm_model: data.llm_model,
            max_tokens: data.max_tokens,
            config: data.config,
            context: data.context,
          },
          loading: false,
        });
      }
    } catch (err) {
      console.error('Failed to load user settings:', err);
      set({ error: '加载设置失败', loading: false });
    }
  },

  updateShowToolCalls: async (show: boolean) => {
    try {
      // 先乐观更新 UI
      set((state) => ({
        settings: {
          ...state.settings,
          show_tool_calls: show,
        },
      }));

      // 获取当前完整设置
      const response = await request.get<any>('/users/settings');
      if (response.data.success && response.data.data) {
        const data = response.data.data;
        const currentSettings = data.settings || {};

        // 更新后端设置
        await request.put('/users/settings', {
          llm_model: data.llm_model || null,
          max_tokens: data.max_tokens || null,
          settings: {
            ...currentSettings,
            show_tool_calls: show,
          },
          config: data.config || {},
          context: data.context || {},
        });
      }
    } catch (error) {
      console.error('Failed to update tool calls setting:', error);
      // 如果失败，回滚到之前的状态
      await get().loadSettings();
      throw error;
    }
  },
}));
