# Architectural Specification: API Backend Architecture

**Feature Goal**: Document the FastAPI async backend framework, PostGIS spatial queries, GeoJSON vector tile streaming endpoints (`GET /api/v1/venues?bbox=...`), WhatsApp subscriber registration (`POST /api/v1/subscribers/`), and 15-venue Downtown Cairo dataset seeding.  
**Author**: `cairo-architect`  
**Date**: 2026-08-13  
**Status**: Implemented  

---

## 1. Architectural Scope, Isolation & Design Patterns

### 1.1 Scope Boundaries & Isolation
- **In-Scope Target Modules**:
  - `backend/app/main.py`
  - `backend/app/api/v1/endpoints/venues.py`
  - `backend/app/api/v1/endpoints/subscribers.py`
  - `backend/app/schemas/venue.py`
  - `backend/app/seed.py`
- **Out-of-Scope / Non-Goals**:
  - Direct HTML rendering in API endpoints (API strictly delivers GeoJSON `FeatureCollection` and JSON objects).

### 1.2 Layered Architecture & Separation of Concerns
- **API Router Layer (`backend/app/api/v1/endpoints/`)**: Pydantic input validation, HTTP status code handling, query parameter parsing.
- **Data Access & Spatial Layer**: GeoAlchemy2 and PostGIS spatial functions (`ST_MakeEnvelope`, `ST_AsGeoJSON`) operating strictly in SRID 4326.
- **Core Configuration (`backend/app/core/`)**: Environment settings, CORS origins, and async database engine initialization.

---

## 2. API Endpoint & Schema Specifications

### 2.1 API Endpoint Registry

| Method | Path | Summary | Query / Body Params | Response Type | Access |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/venues` | Stream GeoJSON features | `bbox`, `vibe`, `price_range` | `GeoJSON FeatureCollection` | Public |
| `POST` | `/api/v1/subscribers/` | Register WhatsApp number | `{"whatsapp_number": "..."}` | `{"status": "subscribed"}` | Public |
| `GET` | `/health` | System health check | None | `{"status": "ok", "version": "0.1.0"}` | Public |

### 2.2 PostGIS Spatial Query (`venues.py`)
```sql
SELECT jsonb_build_object(
    'type', 'FeatureCollection',
    'features', jsonb_agg(
        jsonb_build_object(
            'type', 'Feature',
            'geometry', ST_AsGeoJSON(v.location)::jsonb,
            'properties', jsonb_build_object(
                'id', v.id,
                'slug', v.slug,
                'name_en', v.name_en,
                'name_ar', v.name_ar,
                'address_en', v.address_en,
                'address_ar', v.address_ar,
                'description_en', v.description_en,
                'description_ar', v.description_ar,
                'price_range', v.price_range
            )
        )
    )
)
FROM venues v
WHERE ST_Intersects(v.location, ST_MakeEnvelope(:xmin, :ymin, :xmax, :ymax, 4326));
```

### 2.3 Downtown Cairo Seed Dataset (`seed.py`)
Seeded with 15 historic and active venues centered in Downtown Cairo (*Wust El Balad*, 30.0444°N, 31.2357°E) including Cap d'Or (Al-Liva), Estoril, Café Riche, Odeon Palace Rooftop, and Stella Bar.

---

## 3. Zero-Trust Security Compliance Checklist

- [x] **SEC-1.1**: Query parameters (`bbox`, `vibe`, `price_range`) parsed and validated via Pydantic schemas.
- [x] **SEC-1.2**: All PostGIS spatial envelope queries parameterized to prevent SQL injection.
- [x] **SEC-1.3**: i18n JSON strings sanitized prior to serialization into GeoJSON properties.
- [x] **SEC-1.4**: Zero database passwords or secret keys hardcoded; all loaded dynamically via `backend/app/core/config.py`.
- [x] **SEC-1.5**: CORS origins restricted to allowed application domains.

---

## 4. Verification & Developer Instructions

- **Run API Server**: `uvicorn backend.app.main:app --reload --port 8000`
- **Interactive OpenAPI Docs**: `http://127.0.0.1:8000/docs`
