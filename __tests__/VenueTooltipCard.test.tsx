import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import VenueTooltipCard from '@/components/map/VenueTooltipCard'
import type { GeoJSONFeature } from '@/lib/api'

const mockVenue: GeoJSONFeature = {
  type: 'Feature',
  geometry: { type: 'Point', coordinates: [31.2392, 30.0418] },
  properties: {
    id: 1,
    slug: 'cap-d-or-el-horeya',
    name: "Cap D'Or (El Horeya)",
    name_en: "Cap D'Or (El Horeya)",
    name_ar: 'بار الحرية (كاب دور)',
    description: 'High-ceilinged 1930s Greek-Egyptian institution.',
    description_en: 'High-ceilinged 1930s Greek-Egyptian institution.',
    description_ar: 'بار ومقهى كلاسيكي تاريخي.',
    address: '12 El-Horeya Street',
    address_en: '12 El-Horeya Street',
    address_ar: '١٢ شارع الحرية',
    price_range: '$',
    vibe_description: '1930s Greek-Egyptian atmosphere',
    category_slug: 'historic-pub',
    category_name: 'Historic Pub',
    vibes: ['old-times', 'ambient-music'],
  },
}

describe('VenueTooltipCard Component', () => {
  it('renders venue title, Arabic name, address, and vibe badges correctly', () => {
    const handleClose = vi.fn()
    render(<VenueTooltipCard venue={mockVenue} onClose={handleClose} />)

    expect(screen.getByText("Cap D'Or (El Horeya)")).toBeInTheDocument()
    expect(screen.getByText('بار الحرية (كاب دور)')).toBeInTheDocument()
    expect(screen.getByText('12 El-Horeya Street')).toBeInTheDocument()
    expect(screen.getByText('old times')).toBeInTheDocument()
    expect(screen.getByText('ambient music')).toBeInTheDocument()
  })

  it('triggers onClose when close button is clicked', () => {
    const handleClose = vi.fn()
    render(<VenueTooltipCard venue={mockVenue} onClose={handleClose} />)

    const closeBtn = screen.getByRole('button', { name: /close tooltip/i })
    fireEvent.click(closeBtn)

    expect(handleClose).toHaveBeenCalledTimes(1)
  })
})
