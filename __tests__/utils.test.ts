import { describe, it, expect } from 'vitest'
import { cn } from '@/lib/utils'

describe('cn utility function', () => {
  it('combines simple class names', () => {
    const result = cn('bg-red-500', 'text-white')
    expect(result).toBe('bg-red-500 text-white')
  })

  it('handles conditional class names correctly', () => {
    const isTrue = true
    const isFalse = false
    const result = cn(
      'base-class',
      isTrue && 'active',
      isFalse && 'hidden',
      null,
      undefined
    )
    expect(result).toBe('base-class active')
  })

  it('resolves conflicting tailwind classes using tailwind-merge', () => {
    const result = cn('px-2 py-1', 'px-4')
    expect(result).toBe('py-1 px-4')
  })

  it('handles array inputs and objects', () => {
    const result = cn(['font-bold', 'text-center'], { 'italic': true, 'underline': false })
    expect(result).toBe('font-bold text-center italic')
  })
})
