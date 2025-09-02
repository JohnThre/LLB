/**
 * Tests for chat slice
 */

import { describe, it, expect } from 'vitest'
import { configureStore } from '@reduxjs/toolkit'
import chatSlice, { 
  sendMessageSuccess, 
  clearChat, 
  sendMessageStart, 
  sendMessageFailure 
} from '../../store/slices/chatSlice'

const createTestStore = () => {
  return configureStore({
    reducer: {
      chat: chatSlice
    }
  })
}

describe('Chat Slice', () => {
  it('should have initial state', () => {
    const store = createTestStore()
    const state = store.getState().chat
    
    expect(state.messages).toEqual([])
    expect(state.isLoading).toBe(false)
    expect(state.error).toBeNull()
  })

  it('should add message', () => {
    const store = createTestStore()
    
    const message = {
      id: '1',
      role: 'user' as const,
      content: 'Hello',
      timestamp: new Date().toISOString()
    }
    
    store.dispatch(sendMessageSuccess(message))
    
    const state = store.getState().chat
    expect(state.messages).toHaveLength(1)
    expect(state.messages[0]).toEqual(message)
  })

  it('should clear messages', () => {
    const store = createTestStore()
    
    // Add some messages first
    store.dispatch(sendMessageSuccess({
      id: '1',
      role: 'user',
      content: 'Hello',
      timestamp: new Date().toISOString()
    }))
    
    store.dispatch(clearChat())
    
    const state = store.getState().chat
    expect(state.messages).toHaveLength(0)
  })

  it('should set loading state', () => {
    const store = createTestStore()
    
    store.dispatch(sendMessageStart())
    
    const state = store.getState().chat
    expect(state.isLoading).toBe(true)
  })

  it('should set error state', () => {
    const store = createTestStore()
    
    const error = 'Something went wrong'
    store.dispatch(sendMessageFailure(error))
    
    const state = store.getState().chat
    expect(state.error).toBe(error)
  })

  it('should handle multiple messages in order', () => {
    const store = createTestStore()
    
    const message1 = {
      id: '1',
      role: 'user' as const,
      content: 'First message',
      timestamp: new Date().toISOString()
    }
    
    const message2 = {
      id: '2',
      role: 'assistant' as const,
      content: 'Second message',
      timestamp: new Date(Date.now() + 1000).toISOString()
    }
    
    store.dispatch(sendMessageSuccess(message1))
    store.dispatch(sendMessageSuccess(message2))
    
    const state = store.getState().chat
    expect(state.messages).toHaveLength(2)
    expect(state.messages[0]).toEqual(message1)
    expect(state.messages[1]).toEqual(message2)
  })
})