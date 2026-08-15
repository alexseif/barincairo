import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import Home from '@/app/page'
import * as api from '@/lib/api'

// Mock MapLibre component to avoid WebGL context requirements in jsdom
vi.mock('@/components/map/MapLibreMap', () => ({
  default: ({ selectedVenue }: { selectedVenue: any }) => (
    <div data-testid="mock-map">
      Map Component Loaded - {selectedVenue?.properties?.name || 'No selection'}
    </div>
  ),
}))

const mockBackendVenuesResponse: api.GeoJSONFeatureCollection = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2392, 30.0418] },
      properties: {
        id: 101,
        slug: 'horeya-bar',
        name: 'El Horeya Pub & Cafe',
        description: 'Iconic 1930s high-ceilinged Downtown institution with cold beers.',
        address: '12 El-Horeya Street, Downtown Cairo',
        working_hours: '12:00 PM - 2:00 AM',
        price_range: '$',
        vibe_description: 'High ceilings & vintage atmosphere',
        photo_url: 'https://example.com/horeya.jpg',
        category_slug: 'historic-pub',
        category_name: 'Historic Pub',
        vibes: ['old-times', 'ambient-music'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2385, 30.0435] },
      properties: {
        id: 102,
        slug: 'estoril-bistro',
        name: 'Estoril Bistro',
        description: 'Tucked away passage bistro favored by artists and intellectuals since 1957.',
        address: '12 Talaat Harb Street, Downtown Cairo',
        working_hours: '1:00 PM - 11:30 PM',
        price_range: '$$',
        vibe_description: 'Artistic retreat in historic passage',
        photo_url: 'https://example.com/estoril.jpg',
        category_slug: 'bistro-lounge',
        category_name: 'Bistro Lounge',
        vibes: ['fancy', 'old-times'],
      },
    },
  ],
}

describe('Home Page Component API Integration', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('renders venue name, description, address, and category from backend Python API schema', async () => {
    vi.spyOn(api, 'fetchVenuesGeoJSON').mockResolvedValue(mockBackendVenuesResponse)

    render(<Home />)

    // Wait for async Python API fetch to update state
    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'El Horeya Pub & Cafe' })).toBeInTheDocument()
    })

    expect(
      screen.getByText('Iconic 1930s high-ceilinged Downtown institution with cold beers.')
    ).toBeInTheDocument()
    expect(screen.getByText('12 El-Horeya Street, Downtown Cairo')).toBeInTheDocument()
    expect(screen.getByText('Historic Pub')).toBeInTheDocument()
    expect(screen.getByText('Selected for the night')).toBeInTheDocument()
  })

  it('cycles through 3-venue carousel correctly when next/prev buttons are clicked', async () => {
    vi.spyOn(api, 'fetchVenuesGeoJSON').mockResolvedValue(mockBackendVenuesResponse)

    render(<Home />)

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'El Horeya Pub & Cafe' })).toBeInTheDocument()
    })

    // Click Next venue button
    const nextBtn = screen.getByRole('button', { name: /next venue/i })
    fireEvent.click(nextBtn)

    expect(screen.getByRole('heading', { name: 'Estoril Bistro' })).toBeInTheDocument()
    expect(
      screen.getByText('Tucked away passage bistro favored by artists and intellectuals since 1957.')
    ).toBeInTheDocument()
    expect(screen.getByText('12 Talaat Harb Street, Downtown Cairo')).toBeInTheDocument()

    // Click Previous venue button
    const prevBtn = screen.getByRole('button', { name: /previous venue/i })
    fireEvent.click(prevBtn)

    expect(screen.getByRole('heading', { name: 'El Horeya Pub & Cafe' })).toBeInTheDocument()
  })

  it('displays fallback state gracefully when API returns no venues', async () => {
    vi.spyOn(api, 'fetchVenuesGeoJSON').mockResolvedValue({
      type: 'FeatureCollection',
      features: [],
    })

    render(<Home />)

    await waitFor(() => {
      expect(
        screen.getByText(/No venues found matching selected filters/i)
      ).toBeInTheDocument()
    })
  })
})
