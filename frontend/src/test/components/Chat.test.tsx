/**
 * Tests for Chat component
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { beforeEach, describe, it, expect, vi } from 'vitest'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import Chat from '../../components/Chat/Chat'
import chatSlice from '../../store/slices/chatSlice'

const { i18nState } = vi.hoisted(() => ({
  i18nState: {
    language: 'en-US',
    changeLanguage: vi.fn(),
  },
}))

vi.mock('react-i18next', () => ({
  useTranslation: () => ({
    t: (_key: string, fallback?: string) => fallback ?? _key,
    i18n: i18nState,
  }),
}))

vi.mock('../../components/common/VoiceInput', () => ({
  default: ({
    onTranscriptionComplete,
    disabled,
  }: {
    onTranscriptionComplete: (text: string) => void
    disabled?: boolean
  }) => (
    <button
      type="button"
      disabled={disabled}
      onClick={() => onTranscriptionComplete('Voice message about condoms')}
    >
      Use voice
    </button>
  ),
}))

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
    i18nState.language = 'en-US'
    i18nState.changeLanguage.mockClear()
    vi.mocked(fetch).mockClear()
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
            doi: '10.1000/example',
            pmid: '12345678',
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

  it('sends Simplified Chinese when the active UI locale is Chinese', async () => {
    i18nState.language = 'zh-CN'
    render(<ChatWithProvider />)

    fireEvent.change(screen.getByRole('textbox'), {
      target: { value: '安全套如何帮助预防艾滋？' },
    })
    fireEvent.click(screen.getByRole('button', { name: /send/i }))

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          body: expect.stringContaining('"language":"zh-CN"'),
        }),
      )
    })
  })

  it('sends message when Enter is pressed without Shift', async () => {
    render(<ChatWithProvider />)

    const input = screen.getByRole('textbox')
    fireEvent.change(input, { target: { value: 'Enter key message' } })
    fireEvent.keyPress(input, { key: 'Enter', code: 'Enter', charCode: 13 })

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          body: expect.stringContaining('Enter key message'),
        }),
      )
    })
  })

  it('keeps multiline input when Shift Enter is pressed', () => {
    render(<ChatWithProvider />)

    const input = screen.getByRole('textbox')
    fireEvent.change(input, { target: { value: 'Draft message' } })
    fireEvent.keyPress(input, { key: 'Enter', code: 'Enter', shiftKey: true })

    expect(fetch).not.toHaveBeenCalled()
    expect(input).toHaveValue('Draft message')
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

  it('sends voice transcription text through chat', async () => {
    render(<ChatWithProvider />)

    fireEvent.click(screen.getByRole('button', { name: 'Use voice' }))

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          body: expect.stringContaining('Voice message about condoms'),
        }),
      )
    })
  })

  it('shows an assistant error message when the request fails', async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error('network unavailable'))
    render(<ChatWithProvider />)

    fireEvent.change(screen.getByRole('textbox'), {
      target: { value: 'How do condoms help prevent STIs?' },
    })
    fireEvent.click(screen.getByRole('button', { name: /send/i }))

    expect(
      await screen.findByText('Sorry, I encountered an error. Please try again.', {}, { timeout: 2500 }),
    ).toBeInTheDocument()
  })

  it('shows an assistant error message when the response is not ok', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: false,
      status: 503,
      json: async () => ({}),
    } as Response)
    render(<ChatWithProvider />)

    fireEvent.change(screen.getByRole('textbox'), {
      target: { value: 'How do condoms help prevent STIs?' },
    })
    fireEvent.click(screen.getByRole('button', { name: /send/i }))

    expect(
      await screen.findByText('Sorry, I encountered an error. Please try again.', {}, { timeout: 2500 }),
    ).toBeInTheDocument()
  })

  it('uses publisher name when no compact citation label exists', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => ({
        response: 'Searchable biomedical literature can support reviewable answers.',
        language: 'en',
        language_detected: 'en',
        confidence: 0.95,
        safety_score: 0.98,
        status: 'answered',
        citations: [
          {
            id: 'ncbi-sexual-health-literature',
            title: 'NCBI Literature Resources',
            publisher: 'National Center for Biotechnology Information',
            language: 'en',
            source_type: 'peer_reviewed',
            url: 'https://www.ncbi.nlm.nih.gov/home/literature/',
            excerpt: 'NCBI literature resources provide searchable biomedical literature records.',
          },
        ],
      }),
    } as Response)

    render(<ChatWithProvider />)

    fireEvent.change(screen.getByRole('textbox'), {
      target: { value: 'What literature supports sexual health answers?' },
    })
    fireEvent.click(screen.getByRole('button', { name: /send/i }))

    expect(
      await screen.findByText('National Center for Biotechnology Information', {}, { timeout: 2500 }),
    ).toBeInTheDocument()
  })

  it('clears rendered messages from the conversation', async () => {
    render(<ChatWithProvider />)

    fireEvent.change(screen.getByRole('textbox'), {
      target: { value: 'How do condoms help prevent STIs?' },
    })
    fireEvent.click(screen.getByRole('button', { name: /send/i }))

    expect(
      await screen.findByText('Condoms can reduce STI risk when used correctly.', {}, { timeout: 2500 }),
    ).toBeInTheDocument()

    fireEvent.click(screen.getByLabelText('Clear Chat'))

    expect(screen.queryByText('Condoms can reduce STI risk when used correctly.')).not.toBeInTheDocument()
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
    expect(screen.getByText('PMID: 12345678')).toBeInTheDocument()
    expect(screen.getByText('DOI: 10.1000/example')).toBeInTheDocument()
  })

  it('uses compact labels for Chinese official sources', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => ({
        response: '正确使用安全套有助于降低相关健康风险。',
        language: 'zh-CN',
        language_detected: 'zh-CN',
        confidence: 0.95,
        safety_score: 0.98,
        status: 'answered',
        citations: [
          {
            id: 'nhc-reproductive-health',
            title: '生殖健康相关信息',
            publisher: '国家卫生健康委员会',
            language: 'zh-CN',
            source_type: 'official',
            url: 'https://www.nhc.gov.cn/',
            excerpt: '生殖健康信息应以官方卫生健康资料为依据。',
          },
          {
            id: 'china-cdc-hiv-prevention',
            title: '艾滋病防治知识要点',
            publisher: '中国疾病预防控制中心',
            language: 'zh-CN',
            source_type: 'official',
            url: 'https://ncaids.chinacdc.cn/fazl/zsyd/index_4.htm',
            excerpt: '正确了解艾滋病和性传播疾病预防知识。',
          },
        ],
      }),
    } as Response)

    render(<ChatWithProvider />)

    fireEvent.change(screen.getByRole('textbox'), {
      target: { value: '安全套如何帮助预防艾滋？' },
    })
    fireEvent.click(screen.getByRole('button', { name: /send/i }))

    expect(await screen.findByText('国家卫健委', {}, { timeout: 2500 })).toBeInTheDocument()
    expect(screen.getByText('中国疾控')).toBeInTheDocument()
  })
})
