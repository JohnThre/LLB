import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ModalState {
  isOpen: boolean;
  type: string | null;
  props?: Record<string, any>;
}

interface UIState {
  sidebarOpen: boolean;
  activeModal: ModalState;
  snackbar: {
    open: boolean;
    message: string;
    severity: 'success' | 'error' | 'info' | 'warning';
  };
}

const initialState: UIState = {
  sidebarOpen: true,
  activeModal: {
    isOpen: false,
    type: null,
    props: undefined,
  },
  snackbar: {
    open: false,
    message: '',
    severity: 'info',
  },
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
    },
    setSidebarOpen: (state, action: PayloadAction<boolean>) => {
      state.sidebarOpen = action.payload;
    },
    openModal: (
      state,
      action: PayloadAction<{ type: string; props?: Record<string, any> }>
    ) => {
      state.activeModal = {
        isOpen: true,
        type: action.payload.type,
        props: action.payload.props,
      };
    },
    closeModal: (state) => {
      state.activeModal = {
        isOpen: false,
        type: null,
        props: undefined,
      };
    },
    showSnackbar: (
      state,
      action: PayloadAction<{
        message: string;
        severity?: 'success' | 'error' | 'info' | 'warning';
      }>
    ) => {
      state.snackbar = {
        open: true,
        message: action.payload.message,
        severity: action.payload.severity || 'info',
      };
    },
    hideSnackbar: (state) => {
      state.snackbar.open = false;
    },
  },
});

export const {
  toggleSidebar,
  setSidebarOpen,
  openModal,
  closeModal,
  showSnackbar,
  hideSnackbar,
} = uiSlice.actions;

export default uiSlice.reducer; 