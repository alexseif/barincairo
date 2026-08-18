import { render, screen, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import VenueDetailPage from '@/app/venue/page'
import * as api from '@/lib/api'

vi.mock('@/components/map/MapLibreMap', () => ({
  default: () => <div data-testid="mock-map">Map Component Loaded</div>,
}))

vi.mock('@tanstack/react-router', () => ({
  useParams: () => ({ slug: 'horeya-bar' }),
  Link: ({ children, to, ...props }: any) => <a href={to} {...props}>{children}</a>,
}))

const mockVenueDetail: api.GeoJSONFeature = {
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
    google_maps_url: 'https://maps.google.com/?q=place_id:101',
    category_slug: 'historic-pub',
    category_name: 'Historic Pub',
    vibes: ['old-times', 'ambient-music'],
  },
}

function renderWithQueryClient(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  })
  return render(
    <QueryClientProvider client={queryClient}>
      {ui}
    </QueryClientProvider>
  )
}

describe('Venue Detail Page Component Integration', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('renders venue detail page with full metadata, title, vibes, address and directions link', async () => {
    vi.spyOn(api, 'fetchVenueBySlug').mockResolvedValue(mockVenueDetail)

    renderWithQueryClient(<VenueDetailPage />)

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'El Horeya Pub & Cafe' })).toBeInTheDocument()
    })

    expect(screen.getByText('Iconic 1930s high-ceilinged Downtown institution with cold beers.')).toBeInTheDocument()
    expect(screen.getByText('12 El-Horeya Street, Downtown Cairo')).toBeInTheDocument()
    expect(screen.getAllByText('Historic Pub')[0]).toBeInTheDocument()
    expect(screen.getByText('"High ceilings & vintage atmosphere"')).toBeInTheDocument()

    const directionsLinks = screen.getAllByRole('link', { name: /directions|google maps/i })
    expect(directionsLinks.length).toBeGreaterThan(0)
    expect(directionsLinks[0]).toHaveAttribute('href', 'https://maps.google.com/?q=place_id:101')
  })

  it('displays not found message when venue slug does not exist', async () => {
    vi.spyOn(api, 'fetchVenueBySlug').mockResolvedValue(null)

    renderWithQueryClient(<VenueDetailPage />)

    await waitFor(() => {
      expect(screen.getByText(/Establishment Not Found/i)).toBeInTheDocument()
    })
  })
})
