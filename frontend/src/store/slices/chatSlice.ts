import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

interface ChatState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  activeChatId: string | null;
  chatHistory: {
    id: string;
    title: string;
    lastMessage: string;
    timestamp: string;
  }[];
}

const initialState: ChatState = {
  messages: [],
  isLoading: false,
  error: null,
  activeChatId: null,
  chatHistory: [],
};

const chatSlice = createSlice({
  name: "chat",
  initialState,
  reducers: {
    sendMessageStart: (state) => {
      state.isLoading = true;
      state.error = null;
    },
    sendMessageSuccess: (state, action: PayloadAction<Message>) => {
      state.isLoading = false;
      state.messages.push(action.payload);
      state.error = null;
    },
    sendMessageFailure: (state, action: PayloadAction<string>) => {
      state.isLoading = false;
      state.error = action.payload;
    },
    setMessages: (state, action: PayloadAction<Message[]>) => {
      state.messages = action.payload;
    },
    setActiveChat: (state, action: PayloadAction<string>) => {
      state.activeChatId = action.payload;
    },
    updateChatHistory: (
      state,
      action: PayloadAction<ChatState["chatHistory"]>,
    ) => {
      state.chatHistory = action.payload;
    },
    clearChat: (state) => {
      state.messages = [];
      state.activeChatId = null;
    },
  },
});

export const {
  sendMessageStart,
  sendMessageSuccess,
  sendMessageFailure,
  setMessages,
  setActiveChat,
  updateChatHistory,
  clearChat,
} = chatSlice.actions;

export default chatSlice.reducer;
