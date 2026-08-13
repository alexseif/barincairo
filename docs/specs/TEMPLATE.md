# Architectural Specification: [Feature Name]

**Feature Goal**: [Brief summary of the feature, business value, and architectural scope]  
**Author**: `cairo-architect`  
**Date**: [YYYY-MM-DD]  
**Status**: Draft | Approved | Implemented  

## 1. Architectural Scope, Isolation & Design Patterns

### 1.1 Scope Boundaries & Isolation
- **In-Scope Target Modules**: [Explicit list of directories/files allowed for modification or creation]
- **Out-of-Scope / Non-Goals**: [Adjacent systems or legacy files that MUST NOT be touched or refactored]
- **Side-Effect Isolation**: Ensure state mutations and data flows are strictly localized without mutating global or shared third-party DOM/state.

### 1.2 Layered Architecture & Separation of Concerns
- **Backend Layering (FastAPI)**:
  - `API Routers` (`backend/app/api/`): HTTP parsing, OpenAPI contracts, Pydantic validation (SEC-1.1). Zero business logic.
  - `Service Layer` (`backend/app/services/`): Business logic, GIS spatial calculations, i18n mapping. Zero direct SQL/DB queries.
  - `Repository / DAO Layer` (`backend/app/repositories/`): PostGIS / GeoAlchemy2 ORM queries. Zero HTTP/request awareness.
- **Frontend Layering (Next.js)**:
  - `Server Components (RSC)`: Default for data fetching, static rendering, and SEO injection.
  - `Client Components ('use client')`: Strictly restricted to interactive map canvases, filter state, and touch controls.

---

## 2. Data Schema & Model Specifications

### 2.1 Database Models (PostGIS & PostgreSQL)
```python
# FastAPI / SQLAlchemy ORM Definition
# Insert SQL / PostGIS table DDL and ORM models here
```

### 1.2 API Request/Response Payloads (Pydantic)
```python
# FastAPI Pydantic Schemas (SEC-1.1 Validation)
```

### 1.3 Frontend Type Definitions (TypeScript)
```typescript
// Next.js RSC & Client Component Interface Definitions
```

---

## 2. API Endpoint Contracts & Integration Specs

| Method | Endpoint Path | Description | Authentication / Access | Rate Limit |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/...` | | Public / Auth | 60 req/min |

### 2.1 Request & Response Format
```json
{
  "type": "FeatureCollection",
  "features": []
}
```

---

## 3. Cartography & Visual Matrix Guidelines

- **Primary Colors**: Khedivial Palette (`#ede7d8` Canvas, `#24332d` Primary Green, `#ad793b` Gold Accent)
- **Map Layer Styling**: MapLibre GL vector layer specs, icons, zoom levels, and popups
- **Touch Target Threshold**: Minimum 44px $\times$ 44px for all interactive cartography elements
- **Texture**: Grain texture overlays applied to container cards

---

## 4. Zero-Trust Security & Design Compliance Checklist

- [ ] **SEC-1.1**: All incoming request payloads validated strictly via Pydantic models.
- [ ] **SEC-1.2**: All database interactions use parameterized ORM / prepared statements (no string interpolation in SQL).
- [ ] **SEC-1.3**: i18n JSONB dictionaries sanitized and validated prior to API delivery.
- [ ] **SEC-1.4**: Zero hardcoded secrets, passwords, or sensitive code committed to git; all secrets managed via `.env` and processed with conditional fallback guards (`if env_var: ...`) so missing environment variables do not cause build breaks or container failure.
- [ ] **SEC-1.5**: Endpoint rate-limiting and CORS boundaries explicitly defined.
- [ ] **Khedivial Matrix**: Hex colors `#ede7d8`/`#24332d`/`#ad793b`, 44px touch targets, and typography standards strictly met.

---

## 5. Handoff & Developer Instructions

- **Target Files for `cairo-developer`**:
  - Backend: `backend/app/...`
  - Frontend: `app/...` or `components/...`
  - Unit/Integration Tests: `__tests__/...` or `backend/tests/...`
- **Verification Gate**: All Vitest and Pytest test suites must pass cleanly with 0 type errors (`"strict": true`) and 0 lint warnings.
