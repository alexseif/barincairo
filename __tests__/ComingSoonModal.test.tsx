import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import ComingSoonModal from '@/components/ui/ComingSoonModal'

vi.mock('@/lib/api', () => ({
  subscribeUser: vi.fn(),
}))

import { subscribeUser } from '@/lib/api'

describe('ComingSoonModal Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    sessionStorage.clear()
  })

  it('renders the coming soon message and input fields when open', () => {
    render(<ComingSoonModal isOpen={true} />)

    expect(screen.getByText(/I'm working on this now, it's coming soon\./i)).toBeInTheDocument()
    expect(screen.getByText(/If you want to get notified when it's up, drop me a line below!/i)).toBeInTheDocument()

    expect(screen.getByLabelText(/Name/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/WhatsApp/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/Email/i)).toBeInTheDocument()
  })

  it('displays error if submitted with neither WhatsApp nor Email', async () => {
    render(<ComingSoonModal isOpen={true} />)

    const submitBtn = screen.getByRole('button', { name: /Notify Me/i })
    fireEvent.click(submitBtn)

    expect(await screen.findByText(/Please provide at least a WhatsApp number or Email/i)).toBeInTheDocument()
    expect(subscribeUser).not.toHaveBeenCalled()
  })

  it('submits successfully when email is provided', async () => {
    vi.mocked(subscribeUser).mockResolvedValueOnce(true)

    render(<ComingSoonModal isOpen={true} />)

    const nameInput = screen.getByLabelText(/Name/i)
    const emailInput = screen.getByLabelText(/Email/i)
    const submitBtn = screen.getByRole('button', { name: /Notify Me/i })

    fireEvent.change(nameInput, { target: { value: 'Alex' } })
    fireEvent.change(emailInput, { target: { value: 'alex@example.com' } })
    fireEvent.click(submitBtn)

    await waitFor(() => {
      expect(subscribeUser).toHaveBeenCalledWith({
        name: 'Alex',
        whatsapp_number: undefined,
        email: 'alex@example.com',
        source: 'coming_soon_modal',
      })
    })

    expect(await screen.findByText(/You're on the list!/i)).toBeInTheDocument()
  })

  it('dismisses modal on close click and sets sessionStorage', () => {
    const handleClose = vi.fn()
    render(<ComingSoonModal isOpen={true} onClose={handleClose} />)

    const closeBtn = screen.getByLabelText(/Close modal/i)
    fireEvent.click(closeBtn)

    expect(handleClose).toHaveBeenCalled()
    expect(sessionStorage.getItem('bar_in_cairo_coming_soon_dismissed')).toBe('true')
  })
})
