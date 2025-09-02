/**
 * Tests for Chat component
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import Chat from '../../components/Chat/Chat'
import chatSlice from '../../store/slices/chatSlice'

const mockStore = configureStore({
  reducer: {
    chat: chatSlice
  }
})

const ChatWithProvider = () => (
  <Provider store={mockStore}>
    <Chat />
  </Provider>
)

describe('Chat Component', () => {
  it('renders chat interface', () => {
    render(<ChatWithProvider />)
    expect(screen.getByRole('textbox')).toBeInTheDocument()
  })

  it('sends message on form submit', async () => {
    render(<ChatWithProvider />)
    
    const input = screen.getByRole('textbox')
    const submitButton = screen.getByRole('button', { name: /send/i })
    
    fireEvent.change(input, { target: { value: 'Test message' } })
    fireEvent.click(submitButton)
    
    await waitFor(() => {
      expect(input).toHaveValue('')
    })
  })

  it('displays chat messages', () => {
    render(<ChatWithProvider />)
    expect(screen.getByTestId('chat-messages')).toBeInTheDocument()
  })

  it('handles empty message submission', () => {
    render(<ChatWithProvider />)
    
    const submitButton = screen.getByRole('button', { name: /send/i })
    fireEvent.click(submitButton)
    
    expect(screen.getByRole('textbox')).toHaveValue('')
  })
})