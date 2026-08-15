import { describe, it, expect, vi, beforeEach } from 'vitest'
import { fetchVenuesGeoJSON, subscribeWhatsApp, FALLBACK_VENUES } from '@/lib/api'

describe('Frontend API & Fallback Filter Engine', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  describe('fetchVenuesGeoJSON', () => {
    it('returns remote data when API request succeeds', async () => {
      const mockResponse = {
        type: 'FeatureCollection',
        features: [FALLBACK_VENUES.features[0]],
      }

      vi.stubGlobal(
        'fetch',
        vi.fn().mockResolvedValue({
          ok: true,
          json: async () => mockResponse,
        })
      )

      const data = await fetchVenuesGeoJSON()
      expect(data).toEqual(mockResponse)
      expect(fetch).toHaveBeenCalledTimes(1)
    })

    it('applies query parameters when fetching remote API', async () => {
      const fetchMock = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ type: 'FeatureCollection', features: [] }),
      })
      vi.stubGlobal('fetch', fetchMock)

      await fetchVenuesGeoJSON({ category: 'historic-pub', price_range: '$', vibe: 'fancy' })

      expect(fetchMock).toHaveBeenCalledTimes(1)
      const callUrl = fetchMock.mock.calls[0][0] as string
      expect(callUrl).toContain('category=historic-pub')
      expect(callUrl).toContain('price_range=%24')
      expect(callUrl).toContain('vibe=fancy')
    })

    it('returns all fallback venues when fetch fails or backend is unreachable', async () => {
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

    it('ignores "all" values when filtering fallback venues', async () => {
      vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('Network error')))

      const data = await fetchVenuesGeoJSON({ price_range: 'all', vibe: 'all' })
      expect(data.features.length).toBe(15)
    })
  })

  describe('subscribeWhatsApp', () => {
    it('returns true when API request succeeds', async () => {
      vi.stubGlobal(
        'fetch',
        vi.fn().mockResolvedValue({
          ok: true,
        })
      )

      const result = await subscribeWhatsApp('+201234567890')
      expect(result).toBe(true)
    })

    it('returns false when API server responds with an error status', async () => {
      vi.stubGlobal(
        'fetch',
        vi.fn().mockResolvedValue({
          ok: false,
        })
      )

      const result = await subscribeWhatsApp('+201234567890')
      expect(result).toBe(false)
    })

    it('returns true fallback when fetch throws a network exception', async () => {
      vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('Connection failure')))

      const result = await subscribeWhatsApp('+201234567890')
      expect(result).toBe(true)
    })
  })
})
