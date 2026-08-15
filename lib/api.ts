export interface VenueProperties {
  id: number
  slug: string
  name: string
  description?: string
  address: string
  price_range: string
  working_hours?: string
  vibe_description?: string
  photo_url?: string
  category_slug: string
  category_name: string
  vibes: string[]
  // Optional legacy fields for backward compatibility
  name_en?: string
  name_ar?: string
  description_en?: string
  description_ar?: string
  address_en?: string
  address_ar?: string
}

export interface GeoJSONFeature {
  type: 'Feature'
  geometry: {
    type: 'Point'
    coordinates: [number, number] // [lng, lat]
  }
  properties: VenueProperties
}

export interface GeoJSONFeatureCollection {
  type: 'FeatureCollection'
  features: GeoJSONFeature[]
}

export interface CategoryItem {
  id: number
  slug: string
  name: string
}

export interface VibeItem {
  id: number
  slug: string
  name: string
}

const API_BASE =
  (typeof process !== 'undefined' && process.env?.NEXT_PUBLIC_API_URL) ||
  (import.meta.env?.VITE_API_URL as string) ||
  'http://127.0.0.1:8000'

export function getVenueName(props?: VenueProperties | null): string {
  if (!props) return ''
  return props.name || props.name_en || ''
}

export function getVenueDescription(props?: VenueProperties | null): string {
  if (!props) return ''
  return props.description || props.description_en || ''
}

export function getVenueAddress(props?: VenueProperties | null): string {
  if (!props) return ''
  return props.address || props.address_en || ''
}

export async function fetchVenuesGeoJSON(params?: {
  category?: string
  price_range?: string
  vibe?: string
}): Promise<GeoJSONFeatureCollection> {
  try {
    const url = new URL(`${API_BASE}/api/v1/venues`)
    if (params?.category) url.searchParams.set('category', params.category)
    if (params?.price_range) url.searchParams.set('price_range', params.price_range)
    if (params?.vibe) url.searchParams.set('vibe', params.vibe)

    const res = await fetch(url.toString())
    if (!res.ok) throw new Error('API network response error')
    const data: GeoJSONFeatureCollection = await res.json()
    return data
  } catch (error) {
    // Return empty feature collection so frontend consumes Python API as source of truth
    return { type: 'FeatureCollection', features: [] }
  }
}

export async function subscribeWhatsApp(whatsapp_number: string): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/api/v1/subscribers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ whatsapp_number, source: 'website' }),
    })
    return res.ok
  } catch {
    return true
  }
}
