import { create } from 'zustand';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
}

interface ChatState {
  messages: Message[];
  isStreaming: boolean;
  isLoadingFirstToken: boolean;
  currentStreamingMessage: Message | null;
}

let messageIdCounter = 0;

const generateMessageId = (): string => {
  return `msg_${Date.now()}_${++messageIdCounter}`;
};

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  isStreaming: false,
  isLoadingFirstToken: false,
  currentStreamingMessage: null,

  addMessage: (role, content) => {
    const newMessage: Message = {
      id: generateMessageId(),
      role,
      content,
      timestamp: Date.now(),
    };
    set((state) => ({ messages: [...state.messages, newMessage] }));
  },

  startStreaming: (messageId) => {
    const streamingMessage: Message = {
      id: messageId,
      role: 'assistant',
      content: '',
      timestamp: Date.now(),
    };
    set({
      isStreaming: true,
      isLoadingFirstToken: true,
      currentStreamingMessage: streamingMessage,
    });
  },

  appendStreamingContent: (content) => {
    set((state) => {
      if (!state.currentStreamingMessage) return state;
      const updatedMessage = {
        ...state.currentStreamingMessage,
        content: state.currentStreamingMessage.content + content,
      };
      return {
        currentStreamingMessage: updatedMessage,
        isLoadingFirstToken: false,
      };
    });
  },

  finishStreaming: () => {
    const { currentStreamingMessage, messages } = get();
    if (currentStreamingMessage) {
      set({
        messages: [...messages, currentStreamingMessage],
        isStreaming: false,
        isLoadingFirstToken: false,
        currentStreamingMessage: null,
      });
    } else {
      set({ isStreaming: false, isLoadingFirstToken: false });
    }
  },

  cancelStreaming: () => {
    set({
      isStreaming: false,
      isLoadingFirstToken: false,
      currentStreamingMessage: null,
    });
  },

  clearMessages: () => {
    set({
      messages: [],
      isStreaming: false,
      isLoadingFirstToken: false,
      currentStreamingMessage: null,
    });
  },
}));

export const selectors = {
  useMessages: () => useChatStore((state) => state.messages),
  useIsStreaming: () => useChatStore((state) => state.isStreaming),
  useIsLoadingFirstToken: () => useChatStore((state) => state.isLoadingFirstToken),
  useCurrentStreamingMessage: () => useChatStore((state) => state.currentStreamingMessage),
};