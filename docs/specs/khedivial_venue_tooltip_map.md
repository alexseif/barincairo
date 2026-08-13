# Architectural Specification: Khedivial Venue Tooltip & Map Visual Matrix

**Feature Goal**: Define the cartographic rendering specification, interactive map event handling, responsive layout overlay, and Khedivial color token matrix for Downtown Cairo establishment markers (`REQ-9.1 Option A`).  
**Author**: `cairo-architect`  
**Date**: 2026-08-13  
**Status**: Implemented  

---

## 1. Architectural Scope, Isolation & Design Patterns

### 1.1 Scope Boundaries & Isolation
- **In-Scope Target Modules**:
  - `components/map/VenueTooltipCard.tsx`
  - `components/map/MapLibreMap.tsx`
  - `__tests__/VenueTooltipCard.test.tsx`
- **Out-of-Scope / Non-Goals**:
  - Direct mutation of third-party DOM nodes created by MapLibre GL JS (popups or markers must be handled through React state overlays).
  - Global CSS overrides outside of Tailwind / custom design tokens.

### 1.2 Layered Architecture & Separation of Concerns
- **Client Component Layer (`'use client'`)**:
  - `MapLibreMap.tsx`: Controls MapLibre canvas lifecycle, WebGL context, vector tile source loading, and mouse event dispatching (`click`, `mouseenter`, `mouseleave`).
  - `VenueTooltipCard.tsx`: Floating React overlay component presenting venue details (English/Arabic names, category, description, vibes, price tier, direction link).

---

## 2. Data Schema & Component Specifications

### 2.1 Component Props & Types (TypeScript)
```typescript
import type { GeoJSONFeature } from '@/lib/api'

export interface VenueTooltipCardProps {
  venue: GeoJSONFeature
  onClose: () => void
}
```

### 2.2 GeoJSON Feature Property Contract
```typescript
export interface GeoJSONFeature {
  type: 'Feature'
  geometry: {
    type: 'Point'
    coordinates: [number, number] // [longitude, latitude]
  }
  properties: {
    id: string
    name_en: string
    name_ar: string
    slug: string
    category_name?: string
    address_en: string
    address_ar?: string
    description_en?: string
    description_ar?: string
    price_range: '$' | '$$' | '$$$' | '$$$$'
    vibes?: string[]
    cover_image_url?: string
  }
}
```

---

## 3. Cartography & Visual Matrix Guidelines

### 3.1 Khedivial Palette Tokens
- **Canvas / Background**: `#ede7d8` (Warm Parchment / Sand)
- **Primary / Borders**: `#24332d` (Deep Khedivial Olive)
- **Accent / Micro-Details**: `#ad793b` (Egyptian Gold)

### 3.2 UI Specifications & Interactive Targets
- **Container Styling**: `border-2 border-[#24332d] bg-[#ede7d8] p-5 shadow-[4px_4px_0px_#24332d]`
- **Touch Targets**: Minimum **44px $\times$ 44px** for all interactive buttons (close button: `h-11 w-11`, direction link: `h-11`).
- **Typography & Alignment**:
  - Category Badge: `font-mono text-[9px] uppercase tracking-[0.22em] text-[#ad793b]`
  - Primary Name (EN): `font-serif text-xl font-bold tracking-tight text-[#24332d]`
  - Arabic Name (AR): `font-serif text-sm text-[#24332d]/80` (`lang="ar" dir="rtl"`)
  - Coordinates Display: `font-mono text-[9px] text-[#24332d]/60` formatted as `${lat.toFixed(4)}°N, ${lng.toFixed(4)}°E`

---

## 4. Zero-Trust Security & Design Compliance Checklist

- [x] **SEC-1.1**: Incoming GeoJSON properties sanitized before rendering in DOM.
- [x] **SEC-1.2**: No string concatenation in direction URLs (parameterized query string `lat,lng`).
- [x] **SEC-1.3**: Arabic text correctly encapsulated with `dir="rtl"` and proper font family.
- [x] **SEC-1.4**: Zero secrets or API keys hardcoded in frontend component templates.
- [x] **SEC-1.5**: External directions link restricted to `rel="noopener noreferrer"` and `target="_blank"`.
- [x] **Khedivial Matrix**: Hex colors `#ede7d8`/`#24332d`/`#ad793b`, 44px touch targets, and typography standards strictly met.

---

## 5. Verification & Testing

- **Vitest Test Suite**: `__tests__/VenueTooltipCard.test.tsx`
- Verification standard: 100% pass rate with clean component lifecycle and event callback invocation.
