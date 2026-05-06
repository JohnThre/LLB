/**
 * Tests for general settings.
 */

import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi, beforeEach } from 'vitest'
import GeneralSettings from '../../pages/Settings/GeneralSettings'

const { i18nState } = vi.hoisted(() => ({
  i18nState: {
    language: 'en-US',
    changeLanguage: vi.fn(),
  },
}))

vi.mock('react-i18next', () => ({
  useTranslation: () => ({
    t: (key: string) => key,
    i18n: i18nState,
  }),
}))

describe('GeneralSettings', () => {
  beforeEach(() => {
    i18nState.language = 'en-US'
    i18nState.changeLanguage.mockClear()
  })

  it('renders the supported language choices and toggles', () => {
    render(<GeneralSettings />)

    expect(screen.getByText('settings.general')).toBeInTheDocument()
    expect(screen.getByText('English')).toBeInTheDocument()
    expect(screen.getByText('settings.darkMode')).toBeInTheDocument()
    expect(screen.getByText('settings.notifications')).toBeInTheDocument()
    expect(screen.getByText('settings.autoUpdate')).toBeInTheDocument()
  })

  it('changes the active i18n language from the selector', () => {
    render(<GeneralSettings />)

    fireEvent.mouseDown(screen.getByRole('combobox'))
    fireEvent.click(screen.getByRole('option', { name: '简体中文' }))

    expect(i18nState.changeLanguage).toHaveBeenCalledWith('zh-CN')
  })

  it('updates boolean settings when switches are toggled', () => {
    render(<GeneralSettings />)

    const darkModeSwitch = screen.getByLabelText('settings.darkMode')
    expect(darkModeSwitch).not.toBeChecked()

    fireEvent.click(darkModeSwitch)

    expect(darkModeSwitch).toBeChecked()
  })
})
