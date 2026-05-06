/**
 * Tests for literature management UI.
 */

import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import Literature from '../../pages/Literature'

describe('Literature page', () => {
  beforeEach(() => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        sources: [
          {
            id: 'cdc-condoms-sti',
            title: 'Condom Use and STI Prevention',
            publisher: 'Centers for Disease Control and Prevention',
            language: 'en',
            source_type: 'official',
            url: 'https://www.cdc.gov/condom-use/index.html',
            topics: ['sti', 'condom'],
            excerpt: 'Condoms reduce the risk of many sexually transmitted infections.',
            status: 'approved',
            jurisdiction: 'US',
          },
        ],
      }),
    } as Response)
  })

  it('renders approved sources for review', async () => {
    render(<Literature />)

    await waitFor(() => {
      expect(screen.getByText('Condom Use and STI Prevention')).toBeInTheDocument()
    })

    expect(screen.getByText('Centers for Disease Control and Prevention')).toBeInTheDocument()
    expect(screen.getByText('approved')).toBeInTheDocument()
  })

  it('clears loading state when source loading fails', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => ({}),
    } as Response)

    render(<Literature />)

    await waitFor(() => {
      expect(screen.getByText('Literature')).toBeInTheDocument()
    })
    expect(screen.queryByText('Condom Use and STI Prevention')).not.toBeInTheDocument()
  })

  it('submits a source for admin review', async () => {
    render(<Literature />)

    await screen.findByText('Condom Use and STI Prevention')

    fireEvent.change(screen.getByLabelText('Title'), {
      target: { value: 'New Official Source' },
    })
    fireEvent.change(screen.getByLabelText('Publisher'), {
      target: { value: 'Public Health Agency' },
    })
    fireEvent.change(screen.getByLabelText('URL'), {
      target: { value: 'https://example.org/source' },
    })
    fireEvent.change(screen.getByLabelText('Topics'), {
      target: { value: 'sti, prevention' },
    })
    fireEvent.change(screen.getByLabelText('Excerpt'), {
      target: { value: 'This reviewed public health source supports STI prevention education.' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Submit source' }))

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/v1/literature/sources'),
        expect.objectContaining({ method: 'POST' }),
      )
    })
  })

  it('approves pending sources from the review list', async () => {
    vi.mocked(fetch)
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ sources: [] }),
      } as Response)
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          sources: [
            {
              id: 'pending-source',
              title: 'Pending STI Source',
              publisher: 'Review Publisher',
              language: 'en',
              source_type: 'official',
              url: 'https://example.org/pending',
              topics: ['sti'],
              excerpt: 'This pending source needs approval before use.',
              status: 'pending',
              jurisdiction: 'US',
            },
          ],
        }),
      } as Response)
      .mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => ({ sources: [] }),
      } as Response)

    render(<Literature />)

    fireEvent.click(await screen.findByRole('button', { name: 'Pending' }))
    await screen.findByText('Pending STI Source')
    fireEvent.click(screen.getByRole('button', { name: 'Approve' }))

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/v1/literature/sources/pending-source/approve'),
        expect.objectContaining({ method: 'POST' }),
      )
    })
  })
})
