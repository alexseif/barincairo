import { describe, it, expect, vi } from 'vitest'
import { fetchVenuesGeoJSON, FALLBACK_VENUES } from '@/lib/api'

describe('Frontend API & Fallback Filter Engine', () => {
  it('returns all fallback venues when fetch fails or backend is unreachable', async () => {
    // Mock fetch to simulate network error
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('Network error')))

    const data = await fetchVenuesGeoJSON()
    expect(data.type).toBe('FeatureCollection')
    expect(data.features.length).toBe(15)
  })

  it('filters fallback venues correctly by price range ($)', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('Network error')))

    const data = await fetchVenuesGeoJSON({ price_range: '$' })
    expect(data.features.length).toBeGreaterThan(0)
    data.features.forEach((feature) => {
      expect(feature.properties.price_range).toBe('$')
    })
  })

  it('filters fallback venues correctly by vibe tag (fancy)', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('Network error')))

    const data = await fetchVenuesGeoJSON({ vibe: 'fancy' })
    expect(data.features.length).toBeGreaterThan(0)
    data.features.forEach((feature) => {
      expect(feature.properties.vibes).toContain('fancy')
    })
  })
})
