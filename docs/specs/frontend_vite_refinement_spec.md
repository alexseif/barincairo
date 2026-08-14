# Architectural Specification: Frontend Vite SPA Migration & Refinement

**Feature Goal**: Migrate frontend framework to Vite 6 + React 19 SPA, align GeoJSON schema with Python FastAPI backend, implement TDD via Vitest, convert pixel typography to `rem`, and execute UI/UX refinements.  
**Author**: `cairo-architect`  
**Date**: 2026-08-15  
**Status**: Approved  

---

## 1. Architectural Scope, Isolation & Design Patterns

### 1.1 Scope Boundaries & Isolation
- **In-Scope Target Modules**:
  - `vite.config.ts`, `index.html`, `src/` SPA tree (`main.tsx`, `App.tsx`, `components/`, `lib/`).
  - `vitest.config.mts` / Vitest TDD suites.
  - Component updates for Header, Hero, Map, Carousel, Ground Rules, and Mobile Navigation.
- **Out-of-Scope / Non-Goals**:
  - Python FastAPI backend (`backend/app/api/`, `backend/app/models/`, `backend/app/schemas/`).
  - PostgreSQL / PostGIS database schemas.
- **Side-Effect Isolation**:
  - MapLibre WebGL canvas isolation inside React refs (`useRef`) with strict cleanup lifecycle hooks on component unmount to prevent browser memory leaks and WebGL context losses.

### 1.2 Layered Architecture (Vite + React SPA)
- **Application Shell**: `index.html` root entrypoint mounting `src/main.tsx` and `src/App.tsx`.
- **Component Hierarchy**:
  - `src/components/header/`: Navigation bar, logo (`2rem`), tagline (`0.6875rem`), menu links (`0.75rem`), mobile drawer toggle.
  - `src/components/hero/`: Cinematic title section, WGS84 coordinates tag, and interactive "Wust El Balad" -> "Downtown" tooltip.
  - `src/components/map/`: MapLibre GL vector canvas (`MapLibreMap.tsx`), popup cards (`VenueTooltipCard.tsx`), and responsive filters (Desktop pills / Mobile comboboxes).
  - `src/components/carousel/`: "A good place to start" section with `"Selected for the night"` sub-header, 3-bar carousel controls, and mobile responsive card layout.
  - `src/components/rules/`: Ground rules section with 4-rule responsive grid (2x2 desktop, 1 col mobile) and minimum `0.75rem` font scale.
- **Data & API Layer**: `src/lib/api.ts` consuming `GET /api/v1/venues` with strict Pydantic-aligned TypeScript definitions (`VenueProperties`).

---

## 2. Data Schema & Model Specifications

### 2.1 Frontend Type Definitions (TypeScript)
```typescript
export interface VenueProperties {
  id: number
  slug: string
  name: string
  description?: string
  address: string
  price_range: string // '$' | '$$' | '$$$'
  working_hours?: string
  vibe_description?: string
  photo_url?: string
  category_slug: string
  category_name: string
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
```

### 2.2 Live API Stream Contract
- **Source Endpoint**: `GET /api/v1/venues`
- **Zero Fallback Overrides**: Static mock fallback array (`FALLBACK_VENUES`) is removed. The frontend map and carousel strictly render whatever features are delivered by the Python API response.

---

## 3. Cartography & Visual Matrix Guidelines

### 3.1 Rem Typography Scale

| Component Element | Previous PX Target | Target `rem` | CSS Specification |
| :--- | :--- | :--- | :--- |
| **Site Title** (`barincairo`) | 32px | `2rem` | `text-[2rem]` / `text-3xl` |
| **Site Tagline** (*The Downtown Index*) | 11px | `0.6875rem` | `text-[0.6875rem]` |
| **Header Navigation Menu** | 12px | `0.75rem` | `text-[0.75rem]` |
| **Ground Rules Minimum Text** | 12px min | `0.75rem` min | `text-[0.75rem]` minimum |

### 3.2 Feature UI Matrix
1. **Hero Tooltip**: Accessible hover/focus tooltip container around `"Wust El Balad"` displaying `"Downtown"`.
2. **Carousel Section**:
   - Sub-header label: `"Selected for the night"`.
   - Single hero venue card with Prev (`<`) / Next (`>`) arrows and `1 / 3` tab indicators to cycle between 3 handpicked bars.
   - Mobile card layout: Category tag, price badge, and search button in top 2 columns, venue name (`h3`) full-width underneath.
3. **Ground Rules Section**:
   - Minimum font size `0.75rem` (12px) or larger.
   - 4-rule responsive grid (2x2 on desktop `md:grid-cols-2`, 1 col on mobile).
   - Rule 4: *"Mindful Heritage & Neighborhood Respect: Many spots are historic landmarks—keep noise and photography respectful of the venue's heritage and local residents."*
4. **Mobile Map & UX Refinements**:
   - Filter controls: Two styled `<select>` combobox dropdowns (Price & Vibe) on viewports `< 768px`.
   - Map height: Expanded map height on mobile (`min-h-[420px]`).
   - Mobile menu anchor fix: Smooth scroll targeting for "Our Guide" (`#about`).

---

## 4. Zero-Trust Security & Design Compliance Checklist

- [x] **SEC-1.1**: All incoming GeoJSON API payloads validated against TypeScript `GeoJSONFeatureCollection` definitions.
- [x] **SEC-1.4**: Zero hardcoded secrets; API base URL loaded from `import.meta.env.VITE_API_URL` with default fallback `http://127.0.0.1:8000`.
- [x] **Khedivial Matrix**: Hex colors `#ede7d8`/`#24332d`/`#ad793b`, 44px touch targets, and `rem` typography standards strictly met.

---

## 5. Handoff & Developer Instructions

- **Target Files**:
  - `docs/specs/frontend_vite_refinement_spec.md`
  - `vite.config.ts`, `index.html`, `src/...`
- **Verification Gate**: All Vitest test suites must pass cleanly with 0 type errors (`"strict": true`) and 0 lint warnings before sign-off.
