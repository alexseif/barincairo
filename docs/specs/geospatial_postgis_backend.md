# Architectural Specification: Geospatial PostGIS Backend & Zero-Trust Admin

**Feature Goal**: Define the PostgreSQL + PostGIS spatial schema, GeoJSON bounding box API streaming contract (`GET /api/v1/venues?bbox=...`), and zero-trust SQLAdmin authentication dashboard (`SEC-1.1` to `SEC-1.5`).  
**Author**: `cairo-architect`  
**Date**: 2026-08-13  
**Status**: Implemented  

---

## 1. Architectural Scope, Isolation & Design Patterns

### 1.1 Scope Boundaries & Isolation
- **In-Scope Target Modules**:
  - `backend/app/main.py`
  - `backend/app/api/v1/endpoints/venues.py`
  - `backend/app/admin/auth.py`
  - `backend/app/core/config.py`
  - `backend/app/models/venue.py`
- **Out-of-Scope / Non-Goals**:
  - Public authentication endpoints for end users (admin panel uses isolated session authentication).
  - Non-spatial relational engines (MySQL/SQLite disqualified for production PostGIS spatial queries).

### 1.2 Layered Architecture & Separation of Concerns
- **API Routers (`backend/app/api/v1/`)**: Pure Pydantic payload parsing and HTTP routing. Zero business or spatial logic.
- **Service Layer (`backend/app/services/`)**: Bounding-box Envelope geometry creation (`ST_MakeEnvelope`) and PostGIS query execution.
- **DAO / Repository Layer (`backend/app/repositories/`)**: GeoAlchemy2 / SQLAlchemy ORM parameterized queries.

---

## 2. Data Schema & Model Specifications

### 2.1 PostGIS DDL Specification
```sql
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE venues (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(100) UNIQUE NOT NULL,
    name_en VARCHAR(150) NOT NULL,
    name_ar VARCHAR(150) NOT NULL,
    category_id UUID REFERENCES categories(id),
    address_en TEXT NOT NULL,
    address_ar TEXT NOT NULL,
    description_en TEXT NOT NULL,
    description_ar TEXT,
    price_range VARCHAR(10) DEFAULT '$$',
    cover_image_url TEXT,
    location GEOMETRY(Point, 4326) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_venues_location ON venues USING GIST (location);
```

### 2.2 API Endpoint Contracts

| Method | Endpoint Path | Description | Access | Rate Limit |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/venues?bbox={xmin},{ymin},{xmax},{ymax}` | Viewport GeoJSON vector tile streaming | Public | 120 req/min |
| `GET` | `/admin` | SQLAdmin management dashboard | Admin Auth | Session Guard |

### 2.3 GeoJSON Response Payload Format
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [31.2384, 30.0444]
      },
      "properties": {
        "id": "c1f7b880-...",
        "slug": "cap-d-or",
        "name_en": "Cap d'Or (Al-Liva)",
        "name_ar": "كاب دور",
        "category_name": "Historic Bar",
        "address_en": "22 Abdel Khalek Sarwat St, Downtown Cairo",
        "price_range": "$$",
        "vibes": ["historic", "retro"]
      }
    }
  ]
}
```

---

## 3. SQLAdmin Zero-Trust Authentication Architecture

- **Session Security**: Starlette session middleware with `secret_key` loaded strictly from `settings.SECRET_KEY`.
- **Credential Validation**: Admin authentication checks `ADMIN_USERNAME` and `ADMIN_PASSWORD` from `.env`.
- **Defensive Guard**: If environment variables are missing, fallback functions set local debug defaults with explicit warning logs (`SEC-1.4`).

---

## 4. Zero-Trust Security Compliance Checklist

- [x] **SEC-1.1**: All incoming query parameters (`bbox`, limits) validated strictly using Pydantic / FastAPI query models.
- [x] **SEC-1.2**: All spatial queries use parameterized PostGIS functions (`ST_MakeEnvelope(:xmin, :ymin, :xmax, :ymax, 4326)`).
- [x] **SEC-1.3**: i18n field dictionary mappings validated against SQL schemas before API output.
- [x] **SEC-1.4**: Secrets loaded dynamically via `backend/app/core/config.py` with defensive `if env_var:` guards.
- [x] **SEC-1.5**: CORS origins configured strictly via `settings.CORS_ORIGINS`.

---

## 5. Verification & Testing

- **Backend Health Check**: `GET /health` returns `{"status": "ok", "version": "0.1.0"}`.
- **Integration Test Suite**: `__tests__/api.test.ts` mock API contract validation.
