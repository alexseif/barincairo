# System Architecture Specification: BARINCAIRO.COM

**System Type**: Decoupled Geospatial Directory & Community Routing Platform  
**Target Region**: Downtown Cairo (*Wust El Balad*) — Latitude 30°02′N, Longitude 31°14′E  
**Status**: Active Architecture Specification  

---

## 1. Core Architectural Directives

1. **Decoupled Architecture**: The platform strictly separates spatial data querying and API delivery from presentation cartography.
2. **Initial Launch Scope**: Launch is constrained strictly to the Downtown Cairo perimeter (Tahrir Square, Talaat Harb, Sherif St, Adly St, Champollion, El-Alfy) to enforce data density and establish community engagement before regional expansion.
3. **Data Transport**: All spatial endpoints must return pure GeoJSON collections (`FeatureCollection` and `Feature` objects) to minimize serialization overhead and allow direct ingestion by spatial rendering engines.

---

## 2. Data Infrastructure & Spatial Logic

### Database Specification
- **Engine**: PostgreSQL (v15+)
- **Spatial Extension**: PostGIS (v3.3+) *Mandatory; standard MySQL or non-spatial relational engines are disqualified due to spatial indexing limitations.*
- **Coordinate Reference System (CRS)**: Spatial attributes stored and queried strictly in **SRID 4326 (WGS 84)**.

### Data Model Schema (Conceptual PostGIS Schema)

```sql
-- Establish Spatial Extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Venue Taxonomies & Establishments
CREATE TABLE venues (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(150) NOT NULL,
    category_id INT NOT NULL REFERENCES categories(id),
    address TEXT NOT NULL,
    description TEXT,
    vibe_description VARCHAR(255),
    price_range VARCHAR(10) DEFAULT '$$' NOT NULL,
    working_hours VARCHAR(100),
    photo_url VARCHAR(500),
    google_maps_url TEXT,
    location GEOMETRY(Point, 4326) NOT NULL,
    is_active BOOLEAN DEFAULT true NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_venues_location ON venues USING GIST (location);

-- Subscriptions / Registration Funnel
CREATE TABLE subscribers (
    id SERIAL PRIMARY KEY,
    whatsapp_number VARCHAR(50) UNIQUE NOT NULL,
    source VARCHAR(50) DEFAULT 'website',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Hybrid Ingestion Staging Queue
CREATE TABLE venue_staging (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    place_id VARCHAR(255) UNIQUE NOT NULL,
    google_maps_url TEXT NOT NULL,
    name_raw VARCHAR(255) NOT NULL,
    address_raw TEXT NOT NULL,
    location GEOMETRY(Point, 4326) NOT NULL,
    working_hours VARCHAR(100),
    raw_payload JSONB NOT NULL,
    enriched_payload JSONB,
    status VARCHAR(50) DEFAULT 'PENDING_CURATION',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_staging_location ON venue_staging USING GIST (location);
CREATE INDEX idx_staging_status ON venue_staging(status);
```

### Spatial Queries & Algorithms
1. **Bounding Box Intersections (Viewport Streaming)**:
   ```sql
   SELECT jsonb_build_object(
       'type', 'FeatureCollection',
       'features', jsonb_agg(ST_AsGeoJSON(v.*)::jsonb)
   )
   FROM venues v
   WHERE ST_Intersects(v.location, ST_MakeEnvelope(:xmin, :ymin, :xmax, :ymax, 4326));
   ```
2. **Nearest Neighbor Routing & Bar Hop Clustering**:
   Utilizes PostGIS `ST_DWithin` and `ST_Distance` (or `ST_DistanceSphere`) for proximity routing:
   ```sql
   SELECT *, ST_Distance(location, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography) AS distance_meters
   FROM venues
   WHERE ST_DWithin(location::geography, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography, :max_radius_meters)
   ORDER BY distance_meters ASC;
   ```

---

## 3. Backend Runtime & Admin Panel Specification (FastAPI + SQLAdmin)

- **Framework**: Python FastAPI + AsyncPG + GeoAlchemy2.
- **Admin Panel**: **SQLAdmin** mounted directly at `/admin`.
  - *Engineering Rationale*: Eliminates bespoke React admin development cycles while generating responsive CRUD views for all entities: `User`, `Category`, `VibeTag`, `Venue`, `VenueStaging`, `VenuePhoto`, and `Subscriber`.
  - *Spatial Input & 500 Error Resolution*: To resolve WTForms/SQLAdmin internal server errors on `Venue` and `VenueStaging` edit views, PostGIS `location` (`Geometry`) is excluded from automatic form generation. Dedicated `latitude` and `longitude` float inputs are exposed in view models, automatically generating PostGIS `POINT(lng lat)` geometries upon creation/editing.
  - *Subscriber & Staging Edit 500 Error Resolution*: Explicit `form_columns` (and `form_excluded_columns` excluding auto-populated primary keys and timezone-aware timestamps) are defined across `SubscriberAdmin`, `VenueAdmin`, and `VenueStagingAdmin`.
  - *Full Entity CRUD*: All 7 entities support complete List, View, Create, Edit, and Delete operations.
  - *Admin TDD*: Pytest suite (`backend/tests/test_admin.py`) validates authenticated admin session authorization and full CRUD functionality (List, View, Create, Edit, Delete) across all 7 views.
- **Endpoints**:
  - `GET /api/v1/venues?bbox={xmin},{ymin},{xmax},{ymax}`: Stream GeoJSON vector data.
  - `GET /api/v1/venues/{slug}`: Detailed establishment metadata.
  - `POST /api/v1/subscribe`: WhatsApp registration.
  - `GET/POST /admin`: SQLAdmin dashboard & entity management endpoints.

---

## 4. Frontend & Cartographic Engine Specification

- **Framework**: Vite 6 + React 19 + TypeScript (Client-Side SPA)
- **Styling**: Tailwind CSS v4 with custom visual theme tokens and `rem` typography scale (`2rem` site title, `0.6875rem` tagline, `0.75rem` menu links).
- **Cartographic Engine**: WebGL Spatial Renderer (MapLibre GL JS vector tiles).
  * Consumes pure GeoJSON from Python FastAPI (`GET /api/v1/venues`).
  * Mobile viewports feature compact combobox dropdown filters for Price & Vibe and an expanded map height (`min-h-[420px]`).
  * Custom vector tile styling stripping generic map icons and applying the "Osool" color taxonomy.

---

## 5. Visual Identity & "Osool" (الأصول) Design Token Matrix

| Design Token | Hex Code / Value | Usage |
| :--- | :--- | :--- |
| **Khedivial Limestone** | `#ede7d8` | Core background / base canvas |
| **Weathered Concrete** | `#b9ae96` | Borders, dividers, subtle frames |
| **Faded Vintage Gold** | `#ad793b` | Accent highlights, active states, CTAs |
| **Deep Nile Green** | `#24332d` | Headers, primary navigation, primary text |
| **Card Background** | `#d9cfb8` | Elevated listing detail panels |
| **Muted Text** | `#657067` | Secondary data labels, coordinates |

---

## 6. Infrastructure Isolation & Containerization (Docker)

- **Isolation Strategy**: All components run within an isolated Docker network (`barincairo_net`) managed by `docker-compose.yml`.
- **Co-location Safety**: Prevents runtime or library conflicts with host-level WordPress and Symfony applications.
- **Services**:
  - `barincairo_db`: `postgis/postgis:15-3.3-alpine` (Internal port 5432, 512MB RAM cap).
  - `barincairo_api`: Python FastAPI + SQLAdmin (Local port 127.0.0.1:8000).
  - `barincairo_frontend`: Vite React 19 SPA static bundle / dev server (Local port 127.0.0.1:3000).
- **Host Reverse Proxy**: Host-level Nginx (`nginx.conf.example`) handles SSL termination via Let's Encrypt and proxies `barincairo.com` to `127.0.0.1:3000` and `api.barincairo.com` to `127.0.0.1:8000`.

---

## 7. CI/CD Pipeline & Deployment Strategy

- **Automated Trigger**: GitHub Actions workflow (`.github/workflows/deploy.yml`) on push to `main`.
- **Pipeline Workflow**:
  1. Automated linting and Next.js build verification in GitHub runner.
  2. SSH authentication into host server.
  3. Git pull and container redeployment via `docker compose up -d --build`.
