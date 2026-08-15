import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { Button } from '@/components/ui/button'

describe('Button Component', () => {
  it('renders children and default classes correctly', () => {
    render(<Button>Click me</Button>)
    const button = screen.getByRole('button', { name: /click me/i })
    expect(button).toBeInTheDocument()
    expect(button).toHaveAttribute('data-slot', 'button')
    expect(button.className).toContain('bg-primary')
  })

  it('applies variant classes correctly', () => {
    const { rerender } = render(<Button variant="outline">Outline</Button>)
    let button = screen.getByRole('button', { name: /outline/i })
    expect(button.className).toContain('border-border')

    rerender(<Button variant="destructive">Destructive</Button>)
    button = screen.getByRole('button', { name: /destructive/i })
    expect(button.className).toContain('bg-destructive/10')

    rerender(<Button variant="ghost">Ghost</Button>)
    button = screen.getByRole('button', { name: /ghost/i })
    expect(button.className).toContain('hover:bg-muted')
  })

  it('applies size classes correctly', () => {
    const { rerender } = render(<Button size="sm">Small</Button>)
    let button = screen.getByRole('button', { name: /small/i })
    expect(button.className).toContain('h-7')

    rerender(<Button size="lg">Large</Button>)
    button = screen.getByRole('button', { name: /large/i })
    expect(button.className).toContain('h-9')
  })

  it('handles click events when enabled', () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Action</Button>)
    const button = screen.getByRole('button', { name: /action/i })
    fireEvent.click(button)
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('merges custom className props', () => {
    render(<Button className="custom-class-name">Custom</Button>)
    const button = screen.getByRole('button', { name: /custom/i })
    expect(button.className).toContain('custom-class-name')
  })
})
