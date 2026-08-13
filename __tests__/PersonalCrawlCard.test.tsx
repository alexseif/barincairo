import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import PersonalCrawlCard from '@/components/ui/PersonalCrawlCard'
import { CONTACT_CONFIG } from '@/lib/config'

describe('PersonalCrawlCard Component', () => {
  const defaultProps = {
    whatsappNumber: '+201000000000',
    contactEmail: 'hello@barincairo.com',
  }

  it('renders headline and warm welcoming body copy', () => {
    render(<PersonalCrawlCard {...defaultProps} />)

    expect(
      screen.getByRole('heading', {
        name: /Want a Personal Downtown Cairo Bar Hop\?/i,
      })
    ).toBeInTheDocument()

    expect(
      screen.getByText(/We love Downtown Cairo's historic bars/i)
    ).toBeInTheDocument()
  })

  it('renders WhatsApp CTA link with encoded pre-filled message and target blank', () => {
    render(<PersonalCrawlCard {...defaultProps} />)

    const waLink = screen.getByRole('link', { name: /Chat on WhatsApp/i })
    expect(waLink).toBeInTheDocument()
    expect(waLink).toHaveAttribute('target', '_blank')
    expect(waLink).toHaveAttribute('rel', 'noopener noreferrer')

    const href = waLink.getAttribute('href')
    expect(href).toContain('https://wa.me/201000000000')
    expect(href).toContain(encodeURIComponent(CONTACT_CONFIG.DEFAULT_WA_MESSAGE))
  })

  it('renders Email CTA link with encoded mailto parameters and target blank', () => {
    render(<PersonalCrawlCard {...defaultProps} />)

    const mailLink = screen.getByRole('link', { name: /Send an email/i })
    expect(mailLink).toBeInTheDocument()
    expect(mailLink).toHaveAttribute('target', '_blank')
    expect(mailLink).toHaveAttribute('rel', 'noopener noreferrer')

    const href = mailLink.getAttribute('href')
    expect(href).toContain('mailto:hello%40barincairo.com')
    expect(href).toContain(`subject=${encodeURIComponent('Curated Cairo Bar Hop')}`)
  })

  it('includes aria-label and touch target classes on CTAs', () => {
    render(<PersonalCrawlCard {...defaultProps} />)

    const waLink = screen.getByRole('link', { name: /Chat on WhatsApp/i })
    const mailLink = screen.getByRole('link', { name: /Send an email/i })

    expect(waLink).toHaveAttribute(
      'aria-label',
      'Chat on WhatsApp to plan a curated Cairo bar crawl'
    )
    expect(mailLink).toHaveAttribute(
      'aria-label',
      'Send an email to organize a Cairo bar crawl'
    )

    expect(waLink.className).toContain('min-h-[44px]')
    expect(mailLink.className).toContain('min-h-[44px]')
  })
})
