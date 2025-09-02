/**
 * Tests for main App component
 */

import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { Provider } from 'react-redux'
import { BrowserRouter } from 'react-router-dom'
import { configureStore } from '@reduxjs/toolkit'
import App from '../App'
import authSlice from '../store/slices/authSlice'
import chatSlice from '../store/slices/chatSlice'
import settingsSlice from '../store/slices/settingsSlice'
import uiSlice from '../store/slices/uiSlice'

// Mock i18n
vi.mock('react-i18next', () => ({
  useTranslation: () => ({
    t: (key: string) => key,
    i18n: { changeLanguage: vi.fn() }
  })
}))

const mockStore = configureStore({
  reducer: {
    auth: authSlice,
    chat: chatSlice,
    settings: settingsSlice,
    ui: uiSlice
  }
})

const AppWithProviders = () => (
  <Provider store={mockStore}>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </Provider>
)

describe('App Component', () => {
  it('renders without crashing', () => {
    render(<AppWithProviders />)
    expect(document.body).toBeInTheDocument()
  })

  it('renders main navigation', () => {
    render(<AppWithProviders />)
    expect(screen.getByRole('navigation')).toBeInTheDocument()
  })

  it('renders chat interface by default', () => {
    render(<AppWithProviders />)
    expect(screen.getByTestId('chat-container')).toBeInTheDocument()
  })

  it('applies theme correctly', () => {
    render(<AppWithProviders />)
    const app = screen.getByTestId('app-container')
    expect(app).toHaveClass('theme-default')
  })
})