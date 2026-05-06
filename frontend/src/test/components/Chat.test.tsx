/**
 * Tests for Chat component
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { beforeEach, describe, it, expect, vi } from 'vitest'
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
  beforeEach(() => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        response: 'Condoms can reduce STI risk when used correctly.',
        language: 'en',
        language_detected: 'en',
        confidence: 0.95,
        safety_score: 0.98,
        status: 'answered',
        citations: [
          {
            id: 'cdc-condoms-sti',
            title: 'Condom Use and STI Prevention',
            publisher: 'Centers for Disease Control and Prevention',
            language: 'en',
            source_type: 'official',
            url: 'https://www.cdc.gov/condom-use/index.html',
            excerpt: 'Condoms reduce the risk of many sexually transmitted infections.',
          },
        ],
      }),
    } as Response)
  })

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

  it('shows citations returned with an assistant answer', async () => {
    render(<ChatWithProvider />)

    fireEvent.change(screen.getByRole('textbox'), {
      target: { value: 'How do condoms help prevent STIs?' },
    })
    fireEvent.click(screen.getByRole('button', { name: /send/i }))

    expect(
      await screen.findByText('Condoms can reduce STI risk when used correctly.', {}, { timeout: 2500 }),
    ).toBeInTheDocument()
    expect(screen.getByText('CDC')).toBeInTheDocument()

    fireEvent.click(screen.getByText('CDC'))

    expect(screen.getByText('Condom Use and STI Prevention')).toBeInTheDocument()
    expect(screen.getByText('Centers for Disease Control and Prevention')).toBeInTheDocument()
  })
})
