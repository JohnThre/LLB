/**
 * Tests for chat slice
 */

import { describe, it, expect } from 'vitest'
import { configureStore } from '@reduxjs/toolkit'
import chatSlice, { 
  addMessage, 
  clearMessages, 
  setLoading, 
  setError 
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
      text: 'Hello',
      sender: 'user' as const,
      timestamp: Date.now()
    }
    
    store.dispatch(addMessage(message))
    
    const state = store.getState().chat
    expect(state.messages).toHaveLength(1)
    expect(state.messages[0]).toEqual(message)
  })

  it('should clear messages', () => {
    const store = createTestStore()
    
    // Add some messages first
    store.dispatch(addMessage({
      id: '1',
      text: 'Hello',
      sender: 'user',
      timestamp: Date.now()
    }))
    
    store.dispatch(clearMessages())
    
    const state = store.getState().chat
    expect(state.messages).toHaveLength(0)
  })

  it('should set loading state', () => {
    const store = createTestStore()
    
    store.dispatch(setLoading(true))
    
    const state = store.getState().chat
    expect(state.isLoading).toBe(true)
  })

  it('should set error state', () => {
    const store = createTestStore()
    
    const error = 'Something went wrong'
    store.dispatch(setError(error))
    
    const state = store.getState().chat
    expect(state.error).toBe(error)
  })

  it('should handle multiple messages in order', () => {
    const store = createTestStore()
    
    const message1 = {
      id: '1',
      text: 'First message',
      sender: 'user' as const,
      timestamp: Date.now()
    }
    
    const message2 = {
      id: '2',
      text: 'Second message',
      sender: 'ai' as const,
      timestamp: Date.now() + 1000
    }
    
    store.dispatch(addMessage(message1))
    store.dispatch(addMessage(message2))
    
    const state = store.getState().chat
    expect(state.messages).toHaveLength(2)
    expect(state.messages[0]).toEqual(message1)
    expect(state.messages[1]).toEqual(message2)
  })
})