/**
 * Tests for useVoiceChat hook
 */

import { renderHook, act } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import useVoiceChat from '../../hooks/useVoiceChat'

// Mock Web APIs
const mockMediaRecorder = {
  start: vi.fn(),
  stop: vi.fn(),
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
  state: 'inactive'
}

const mockGetUserMedia = vi.fn().mockResolvedValue({
  getTracks: () => [{ stop: vi.fn() }]
})

Object.defineProperty(global, 'MediaRecorder', {
  writable: true,
  value: vi.fn().mockImplementation(() => mockMediaRecorder)
})

Object.defineProperty(global.navigator, 'mediaDevices', {
  writable: true,
  value: { getUserMedia: mockGetUserMedia }
})

describe('useVoiceChat Hook', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('initializes with correct default state', () => {
    const { result } = renderHook(() => useVoiceChat())
    
    expect(result.current.isRecording).toBe(false)
    expect(result.current.isProcessing).toBe(false)
    expect(result.current.transcript).toBe('')
    expect(result.current.error).toBeNull()
  })

  it('starts recording when startRecording is called', async () => {
    const { result } = renderHook(() => useVoiceChat())
    
    await act(async () => {
      await result.current.startRecording()
    })
    
    expect(mockGetUserMedia).toHaveBeenCalled()
    expect(mockMediaRecorder.start).toHaveBeenCalled()
  })

  it('stops recording when stopRecording is called', async () => {
    const { result } = renderHook(() => useVoiceChat())
    
    await act(async () => {
      await result.current.startRecording()
    })
    
    act(() => {
      result.current.stopRecording()
    })
    
    expect(mockMediaRecorder.stop).toHaveBeenCalled()
  })

  it('handles permission denied error', async () => {
    mockGetUserMedia.mockRejectedValueOnce(new Error('Permission denied'))
    
    const { result } = renderHook(() => useVoiceChat())
    
    await act(async () => {
      await result.current.startRecording()
    })
    
    expect(result.current.error).toBeTruthy()
  })

  it('clears transcript when clearTranscript is called', () => {
    const { result } = renderHook(() => useVoiceChat())
    
    act(() => {
      result.current.clearTranscript()
    })
    
    expect(result.current.transcript).toBe('')
  })
})