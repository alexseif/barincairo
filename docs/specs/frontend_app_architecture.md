# Architectural Specification: Frontend Application Architecture

**Feature Goal**: Document the Next.js 16 App Router frontend, MapLibre GL map integration, Khedivial visual matrix design system (`#ede7d8`, `#24332d`, `#ad793b`), responsive venue overlay card, resilient fallback dataset client (`lib/api.ts`), and Vitest TDD test harness.  
**Author**: `cairo-architect`  
**Date**: 2026-08-13  
**Status**: Implemented  

---

## 1. Architectural Scope, Isolation & Design Patterns

### 1.1 Scope Boundaries & Isolation
- **In-Scope Target Modules**:
  - `app/page.tsx`
  - `app/globals.css`
  - `components/map/MapLibreMap.tsx`
  - `components/map/VenueTooltipCard.tsx`
  - `lib/api.ts`
  - `__tests__/api.test.ts`
  - `__tests__/VenueTooltipCard.test.tsx`
- **Out-of-Scope / Non-Goals**:
  - Raw HTML positioning (`top: %`, `left: %`) for cartographic markers (all spatial markers MUST be rendered on the MapLibre GL WebGL canvas).

### 1.2 Layered Architecture & Separation of Concerns
- **Application Page (`app/page.tsx`)**: Reactive client component controlling hero header, active filter pill states (Vibes & Price tier), dynamic MapLibre canvas integration, venue selection drawer, and WhatsApp dispatch form.
- **Cartographic Component (`MapLibreMap.tsx`)**: Manages MapLibre GL JS canvas lifecycle, GeoJSON source updates, venue point layer rendering, hover tooltips, and click selection listeners.
- **Overlay Component (`VenueTooltipCard.tsx`)**: Floating venue card presenting bilingual venue details, vibe tags, price tier, direction link, and close button.
- **API Client & Resilient Fallback (`lib/api.ts`)**: `fetchVenuesGeoJSON` client that attempts live API fetching with automated failover to `FALLBACK_VENUES` GeoJSON collection if backend is offline.

---

## 2. Component Interfaces & Visual Tokens

### 2.1 Component Props & Data Types
```typescript
export interface GeoJSONFeature {
  type: 'Feature'
  geometry: {
    type: 'Point'
    coordinates: [number, number] // [longitude, latitude]
  }
  properties: {
    id: number | string
    slug: string
    name_en: string
    name_ar: string
    description_en?: string
    description_ar?: string
    address_en: string
    address_ar?: string
    price_range: string
    category_slug?: string
    category_name?: string
    vibes?: string[]
  }
}

export interface VenueTooltipCardProps {
  venue: GeoJSONFeature
  onClose: () => void
}
```

### 2.2 Khedivial Design Token Matrix
- **Base Canvas (`bg-[#ede7d8]`)**: Warm Parchment background.
- **Primary / Border (`text-[#24332d]`, `border-[#24332d]`)**: Deep Khedivial Olive.
- **Accent / Details (`text-[#ad793b]`)**: Egyptian Gold accent highlights.
- **Touch Targets**: Minimum **44px $\times$ 44px** touch target area for interactive control elements (`aria-label` explicit on buttons).

---

## 3. Zero-Trust Security & Design Compliance Checklist

- [x] **SEC-1.1**: External direction links restricted to `rel="noopener noreferrer"` and `target="_blank"`.
- [x] **SEC-1.2**: Arabic text explicitly isolated with `lang="ar"` and `dir="rtl"` attributes.
- [x] **SEC-1.3**: Fallback dataset (`FALLBACK_VENUES`) validated to prevent layout or runtime breaks when offline.
- [x] **SEC-1.4**: Zero hardcoded API keys or secret tokens present in frontend code.
- [x] **SEC-1.5**: Minimum 44px touch targets enforced for all interactive components.

---

## 4. Verification & Testing

- **Vitest Test Suite**: `npm test -- --run`
- Implemented tests:
  - `__tests__/api.test.ts`: Verifies GeoJSON structures and fallback payload formatting.
  - `__tests__/VenueTooltipCard.test.tsx`: Verifies component render, bilingual text output, and close click handler.
