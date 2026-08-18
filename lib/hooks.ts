import { useQuery, useMutation } from '@tanstack/react-query'
import { fetchVenuesGeoJSON, fetchVenueBySlug, subscribeWhatsApp, GeoJSONFeatureCollection, GeoJSONFeature } from '@/lib/api'

export interface VenueFilters {
  category?: string
  price_range?: string
  vibe?: string
}

export function useVenuesQuery(filters?: VenueFilters) {
  return useQuery<GeoJSONFeatureCollection>({
    queryKey: ['venues', filters || {}],
    queryFn: () => fetchVenuesGeoJSON(filters),
    staleTime: 60 * 1000,
  })
}

export function useVenueDetailQuery(slug: string) {
  return useQuery<GeoJSONFeature | null>({
    queryKey: ['venue', slug],
    queryFn: () => fetchVenueBySlug(slug),
    enabled: !!slug,
    staleTime: 60 * 1000,
  })
}

export function useSubscribeMutation() {
  return useMutation({
    mutationFn: (whatsappNumber: string) => subscribeWhatsApp(whatsappNumber),
  })
}
