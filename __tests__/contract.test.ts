import { describe, it, expect } from 'vitest'
import openapi from '../openapi.json'
import { getVenueName, getVenueDescription, getVenueAddress, type VenueProperties } from '@/lib/api'

describe('Backend/Frontend Schema Contract Enforcement', () => {
  const venueSchemaProps = openapi.components.schemas.VenueProperties.properties
  const requiredFields = openapi.components.schemas.VenueProperties.required || []

  it('validates that FastAPI backend exports required VenueProperties fields in OpenAPI spec', () => {
    // Assert critical properties exist in the OpenAPI schema
    expect(venueSchemaProps).toHaveProperty('name')
    expect(venueSchemaProps).toHaveProperty('description')
    expect(venueSchemaProps).toHaveProperty('address')
    expect(venueSchemaProps).toHaveProperty('price_range')
    expect(venueSchemaProps).toHaveProperty('category_slug')
    expect(venueSchemaProps).toHaveProperty('category_name')
    expect(venueSchemaProps).toHaveProperty('vibes')

    // Assert that 'name' and 'address' are marked as non-null required fields in OpenAPI schema
    expect(requiredFields).toContain('name')
    expect(requiredFields).toContain('address')
  })

  it('ensures frontend helper functions correctly extract single-language backend schema properties', () => {
    const mockFromBackend: VenueProperties = {
      id: 1,
      slug: 'horeya',
      name: "Cap D'Or (El Horeya)",
      description: 'High-ceilinged 1930s Greek-Egyptian institution.',
      address: '12 El-Horeya Street',
      price_range: '$',
      category_slug: 'pub',
      category_name: 'Pub',
      vibes: ['old-times'],
    }

    expect(getVenueName(mockFromBackend)).toBe("Cap D'Or (El Horeya)")
    expect(getVenueDescription(mockFromBackend)).toBe('High-ceilinged 1930s Greek-Egyptian institution.')
    expect(getVenueAddress(mockFromBackend)).toBe('12 El-Horeya Street')
  })

  it('fails if backend removes essential properties without frontend adaptation', () => {
    const keys = Object.keys(venueSchemaProps)
    // If backend removes 'name' or 'address', this contract assertion fails immediately
    expect(keys).toContain('name')
    expect(keys).toContain('address')
    expect(keys).toContain('description')
  })
})
