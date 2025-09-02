/**
 * Tests for file service
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { uploadFile, validateFile } from '../../services/fileService'

// Mock fetch
global.fetch = vi.fn()

describe('File Service', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('validateFile', () => {
    it('validates supported file types', () => {
      const pdfFile = new File(['content'], 'test.pdf', { type: 'application/pdf' })
      const audioFile = new File(['content'], 'test.mp3', { type: 'audio/mpeg' })
      
      expect(validateFile(pdfFile)).toBe(true)
      expect(validateFile(audioFile)).toBe(true)
    })

    it('rejects unsupported file types', () => {
      const textFile = new File(['content'], 'test.exe', { type: 'application/exe' })
      
      expect(validateFile(textFile)).toBe(false)
    })

    it('validates file size limits', () => {
      const smallFile = new File(['x'.repeat(1000)], 'small.pdf', { type: 'application/pdf' })
      const largeFile = new File(['x'.repeat(60 * 1024 * 1024)], 'large.pdf', { type: 'application/pdf' })
      
      expect(validateFile(smallFile)).toBe(true)
      expect(validateFile(largeFile)).toBe(false)
    })
  })

  describe('uploadFile', () => {
    it('uploads file successfully', async () => {
      const mockResponse = {
        ok: true,
        json: () => Promise.resolve({ success: true, fileId: '123' })
      }
      
      vi.mocked(fetch).mockResolvedValueOnce(mockResponse as any)
      
      const file = new File(['content'], 'test.pdf', { type: 'application/pdf' })
      const result = await uploadFile(file)
      
      expect(result.success).toBe(true)
      expect(result.fileId).toBe('123')
    })

    it('handles upload errors', async () => {
      const mockResponse = {
        ok: false,
        status: 500,
        statusText: 'Internal Server Error'
      }
      
      vi.mocked(fetch).mockResolvedValueOnce(mockResponse as any)
      
      const file = new File(['content'], 'test.pdf', { type: 'application/pdf' })
      
      await expect(uploadFile(file)).rejects.toThrow('Upload failed')
    })

    it('handles network errors', async () => {
      vi.mocked(fetch).mockRejectedValueOnce(new Error('Network error'))
      
      const file = new File(['content'], 'test.pdf', { type: 'application/pdf' })
      
      await expect(uploadFile(file)).rejects.toThrow('Network error')
    })
  })
})