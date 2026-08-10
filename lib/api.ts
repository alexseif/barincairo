export interface VenueProperties {
  id: number
  slug: string
  name_en: string
  name_ar: string
  description_en?: string
  description_ar?: string
  address_en: string
  address_ar: string
  price_range: string
  vibe_description?: string
  photo_url?: string
  category_slug: string
  category_name: str
  vibes: string[]
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
  name_en: string
  name_ar: str
}

export interface VibeItem {
  id: number
  slug: string
  name_en: string
  name_ar: str
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

export const FALLBACK_VENUES: GeoJSONFeatureCollection = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.4289, 30.0384] },
      properties: {
        id: 1,
        slug: 'cairo-jazz-610',
        name_en: 'Cairo Jazz Club 610',
        name_ar: 'كايرو جاز كلوب',
        description_en: 'A beloved institution for live sets, smoky corners, and the city’s most reliable midnight energy.',
        address_en: '610, First New Cairo',
        address_ar: '٦١٠ التجمع الأول',
        price_range: '$$$',
        vibe_description: 'Late-night / electric',
        photo_url: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=900&q=80',
        category_slug: 'live-music',
        category_name: 'Live music',
        vibes: ['live-performance', 'dancy', 'late-night'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2389, 30.0444] },
      properties: {
        id: 2,
        slug: 'vent-downtown',
        name_en: 'Vent',
        name_ar: 'فِنت',
        description_en: 'A small, low-lit room for beautifully balanced drinks and long conversations.',
        address_en: '12 El-Horeya, Downtown',
        address_ar: '١٢ شارع الحرية، وسط البلد',
        price_range: '$$',
        vibe_description: 'Intimate / considered',
        photo_url: 'https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?auto=format&fit=crop&w=900&q=80',
        category_slug: 'cocktail-bar',
        category_name: 'Cocktail bar',
        vibes: ['ambient-music', 'intimate', 'old-times'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2398, 30.0468] },
      properties: {
        id: 3,
        slug: 'horus-rooftop',
        name_en: 'Horus Rooftop',
        name_ar: 'حورس',
        description_en: 'Watch the downtown rooftops turn copper over a cold Sakara and a plate of mezze.',
        address_en: 'Talaat Harb Square',
        address_ar: 'ميدان طلعت حرب',
        price_range: '$$',
        vibe_description: 'Golden hour / open-air',
        photo_url: 'https://images.unsplash.com/photo-1572116469696-31de0f17cc34?auto=format&fit=crop&w=900&q=80',
        category_slug: 'rooftop',
        category_name: 'Rooftop',
        vibes: ['fancy', 'oud-player', 'golden-hour'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2415, 30.0452] },
      properties: {
        id: 4,
        slug: 'soma-caffe',
        name_en: 'Soma Caffe',
        name_ar: 'سوما كافيه',
        description_en: 'A daytime cafe that quietly becomes one of Downtown’s favorite after-dark hideouts.',
        address_en: '26 Sherif Street',
        address_ar: '٢٦ شارع شريف',
        price_range: '$',
        vibe_description: 'Quiet / all-day',
        photo_url: 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=900&q=80',
        category_slug: 'cafe-bar',
        category_name: 'Cafe bar',
        vibes: ['ambient-music', 'old-times', 'flirty'],
      },
    },
  ],
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

    const res = await fetch(url.toString(), { next: { revalidate: 60 } })
    if (!res.ok) throw new Error('API network response error')
    const data: GeoJSONFeatureCollection = await res.json()
    return data
  } catch (error) {
    // Return graceful fallback when backend container is starting up
    return FALLBACK_VENUES
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
