# Architectural Specification: Multilingual Data Schema & TDD Test Harness

**Feature Goal**: Define the bilingual Arabic/English data structures (`REQ-1.4`), PostGIS seed establishment dataset (15 Downtown Cairo venues), and Vitest/Pytest TDD test harness specifications (`REQ-8.2`).  
**Author**: `cairo-architect`  
**Date**: 2026-08-13  
**Status**: Implemented  

---

## 1. Architectural Scope, Isolation & Design Patterns

### 1.1 Scope Boundaries & Isolation
- **In-Scope Target Modules**:
  - `backend/app/seed.py`
  - `backend/app/schemas/venue.py`
  - `__tests__/api.test.ts`
  - `vitest.config.mts`
  - `vitest.setup.ts`
- **Out-of-Scope / Non-Goals**:
  - Auto-translation APIs (all bilingual data must be curated and stored statically in the PostGIS DB or JSONB structures).

### 1.2 Layered Architecture & Separation of Concerns
- **Data Models**: Explicit dual-field localization (`name_en`, `name_ar`, `description_en`, `description_ar`, `address_en`, `address_ar`) stored as first-class columns or structured JSONB objects.
- **Test Harness**: Decoupled unit and integration harnesses using Vitest for React components & API mocks, and Pytest for async FastAPI endpoints.

---

## 2. Seed Data Schema & Establishment Specification

### 2.1 Seed Establishments (Downtown Cairo Perimeter)
The dataset comprises 15 curated establishments centered around Wust El Balad (Latitude 30.0444, Longitude 31.2357):
1. **Cap d'Or (Al-Liva)**: Historic Art Deco bar on Abdel Khalek Sarwat St.
2. **Stella Bar**: Classic Downtown drinking establishment on Talaat Harb St.
3. **Café Riche**: Historic literary venue on Talaat Harb St.
4. **Le Grillon**: Secluded courtyard venue off Qasr El Nil St.
5. **Horus House Rooftop**: Viewpoint venue on 26th of July St.
*(And 10 additional Downtown venues seeded in `backend/app/seed.py`)*

### 2.2 Seed Data Structure (`seed.py`)
```python
SEED_VENUES = [
    {
        "slug": "cap-d-or",
        "name_en": "Cap d'Or (Al-Liva)",
        "name_ar": "كاب دور",
        "category_slug": "historic-bar",
        "address_en": "22 Abdel Khalek Sarwat St, Downtown Cairo",
        "address_ar": "٢٢ شارع عبد الخالق ثروت، وسط البلد، القاهرة",
        "description_en": "Iconic vintage bar featuring original neo-classical woodwork and historic downtown atmosphere.",
        "description_ar": "بار تاريخي ذو طابع عريق يقع في قلب وسط البلد.",
        "price_range": "$$",
        "latitude": 30.0398,
        "longitude": 31.2391,
        "vibes": ["historic", "retro", "cozy"],
    },
    ...
]
```

---

## 3. Test Harness Specification & Verification Rules

### 3.1 Vitest Setup (`vitest.config.mts`)
- Environment: `jsdom`
- Transpiler: `@vitejs/plugin-react`
- Alias: `@/` mapped to project root `/`

### 3.2 Test Requirements (TDD Harness)
- **Component Tests**: Assert complete render of English and Arabic localized content without DOM throwing exceptions (`__tests__/VenueTooltipCard.test.tsx`).
- **API Mocks**: Validate GeoJSON payload structure and coordinates format (`__tests__/api.test.ts`).

---

## 4. Zero-Trust Security & Design Compliance Checklist

- [x] **SEC-1.1**: Seed script validates coordinates within valid lat/lng ranges (-90 to 90 lat, -180 to 180 lng).
- [x] **SEC-1.2**: Async DB seed insertion uses SQLAlchemy session ORM bindings (`session.add(...)`).
- [x] **SEC-1.3**: Arabic strings validated to prevent encoding anomalies or RTL layout breaks.
- [x] **SEC-1.4**: Zero plain-text passwords or secret keys present in `seed.py`.
- [x] **SEC-1.5**: Test harnesses execute in isolated test environments without hitting live production database instances.

---

## 5. Handoff & Developer Instructions

- Execute tests via: `npm test -- --run`
- Execute seed via: `python3 -m backend.app.seed`
