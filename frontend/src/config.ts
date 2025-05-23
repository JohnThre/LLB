// API Configuration
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// File Upload Configuration
export const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB
export const ALLOWED_FILE_TYPES = {
  audio: ['.mp3', '.wav', '.ogg', '.m4a'],
  document: ['.pdf', '.doc', '.docx', '.txt'],
  image: ['.jpg', '.jpeg', '.png', '.gif'],
};

// Feature Flags
export const FEATURES = {
  voiceInput: true,
  fileUpload: true,
  documentProcessing: true,
  multiLanguage: true,
};

// UI Configuration
export const UI_CONFIG = {
  maxMessageLength: 1000,
  maxChatHistory: 100,
  defaultLanguage: 'en',
  supportedLanguages: ['en', 'zh-CN'],
}; 