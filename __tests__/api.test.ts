import { describe, it, expect, vi, beforeEach } from 'vitest'
import { fetchVenuesGeoJSON, subscribeWhatsApp, getVenueName, getVenueDescription, getVenueAddress } from '@/lib/api'

describe('Frontend API Engine', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  describe('fetchVenuesGeoJSON', () => {
    it('returns remote data when API request succeeds', async () => {
      const mockResponse = {
        type: 'FeatureCollection',
        features: [
          {
            type: 'Feature',
            geometry: { type: 'Point', coordinates: [31.2392, 30.0418] },
            properties: {
              id: 1,
              slug: 'cap-d-or-el-horeya',
              name: "Cap D'Or (El Horeya)",
              address: '12 El-Horeya Street',
              price_range: '$',
              category_slug: 'historic-pub',
              category_name: 'Historic Pub',
              vibes: ['old-times'],
            },
          },
        ],
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

    it('returns empty feature collection when fetch fails or backend is unreachable', async () => {
      vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('Network error')))

      const data = await fetchVenuesGeoJSON()
      expect(data.type).toBe('FeatureCollection')
      expect(data.features.length).toBe(0)
    })
  })

  describe('venue property helpers', () => {
    it('returns single language name or legacy name_en fallback', () => {
      expect(getVenueName({ id: 1, slug: 'test', name: 'Bar Cairo', address: 'Cairo', price_range: '$', category_slug: 'pub', category_name: 'Pub', vibes: [] })).toBe('Bar Cairo')
      expect(getVenueName({ id: 1, slug: 'test', name: '', name_en: 'Bar Cairo EN', address: 'Cairo', price_range: '$', category_slug: 'pub', category_name: 'Pub', vibes: [] })).toBe('Bar Cairo EN')
    })

    it('returns single language description or legacy description_en fallback', () => {
      expect(getVenueDescription({ id: 1, slug: 'test', name: 'Bar', description: 'Cozy spot', address: 'Cairo', price_range: '$', category_slug: 'pub', category_name: 'Pub', vibes: [] })).toBe('Cozy spot')
      expect(getVenueDescription({ id: 1, slug: 'test', name: 'Bar', description_en: 'Cozy EN', address: 'Cairo', price_range: '$', category_slug: 'pub', category_name: 'Pub', vibes: [] })).toBe('Cozy EN')
    })

    it('returns single language address or legacy address_en fallback', () => {
      expect(getVenueAddress({ id: 1, slug: 'test', name: 'Bar', address: 'Downtown', price_range: '$', category_slug: 'pub', category_name: 'Pub', vibes: [] })).toBe('Downtown')
      expect(getVenueAddress({ id: 1, slug: 'test', name: 'Bar', address: '', address_en: 'Downtown EN', price_range: '$', category_slug: 'pub', category_name: 'Pub', vibes: [] })).toBe('Downtown EN')
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
