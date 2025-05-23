import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AppearanceSettings {
  theme: 'light' | 'dark' | 'system';
  fontSize: number;
  fontFamily: string;
}

interface NotificationSettings {
  email: boolean;
  push: boolean;
  sound: boolean;
}

interface SettingsState {
  appearance: AppearanceSettings;
  notifications: NotificationSettings;
  language: string;
  isLoading: boolean;
  error: string | null;
}

const initialState: SettingsState = {
  appearance: {
    theme: 'system',
    fontSize: 16,
    fontFamily: 'Inter',
  },
  notifications: {
    email: true,
    push: true,
    sound: true,
  },
  language: 'en',
  isLoading: false,
  error: null,
};

const settingsSlice = createSlice({
  name: 'settings',
  initialState,
  reducers: {
    updateAppearance: (
      state,
      action: PayloadAction<Partial<AppearanceSettings>>
    ) => {
      state.appearance = { ...state.appearance, ...action.payload };
    },
    updateNotifications: (
      state,
      action: PayloadAction<Partial<NotificationSettings>>
    ) => {
      state.notifications = { ...state.notifications, ...action.payload };
    },
    setLanguage: (state, action: PayloadAction<string>) => {
      state.language = action.payload;
    },
    loadSettingsStart: (state) => {
      state.isLoading = true;
      state.error = null;
    },
    loadSettingsSuccess: (state, action: PayloadAction<Partial<SettingsState>>) => {
      state.isLoading = false;
      state.appearance = { ...state.appearance, ...action.payload.appearance };
      state.notifications = { ...state.notifications, ...action.payload.notifications };
      if (action.payload.language) {
        state.language = action.payload.language;
      }
      state.error = null;
    },
    loadSettingsFailure: (state, action: PayloadAction<string>) => {
      state.isLoading = false;
      state.error = action.payload;
    },
  },
});

export const {
  updateAppearance,
  updateNotifications,
  setLanguage,
  loadSettingsStart,
  loadSettingsSuccess,
  loadSettingsFailure,
} = settingsSlice.actions;

export default settingsSlice.reducer; 