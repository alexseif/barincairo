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
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(100) UNIQUE NOT NULL,
    name_en VARCHAR(150) NOT NULL,
    name_ar VARCHAR(150) NOT NULL,
    venue_type VARCHAR(50) NOT NULL, -- e.g., 'Live music', 'Cocktail bar', 'Rooftop', 'Cafe bar'
    address_en TEXT NOT NULL,
    address_ar TEXT NOT NULL,
    vibe_tags TEXT[] DEFAULT '{}',
    description_en TEXT NOT NULL,
    description_ar TEXT,
    cover_image_url TEXT,
    location GEOMETRY(Point, 4326) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_premium BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_venues_location ON venues USING GIST (location);

-- Community Bar Hops / Curated Trails
CREATE TABLE bar_hops (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(150) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    estimated_duration_minutes INT NOT NULL,
    stops_count INT NOT NULL,
    route_linestring GEOMETRY(LineString, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Subscriptions / Registration Funnel
CREATE TABLE subscribers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    whatsapp_number VARCHAR(50) UNIQUE NOT NULL,
    source VARCHAR(50) DEFAULT 'whatsapp_dispatch',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Hybrid Ingestion Staging Queue
CREATE TABLE venue_staging (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    place_id VARCHAR(255) UNIQUE NOT NULL,
    google_maps_url TEXT NOT NULL,
    name_raw VARCHAR(255) NOT NULL,
    address_raw TEXT NOT NULL,
    location GEOMETRY(Point, 4326) NOT NULL,
    raw_payload JSONB NOT NULL,
    enriched_payload JSONB,
    status VARCHAR(50) DEFAULT 'PENDING_CURATION',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
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
- **Admin Panel**: **SQLAdmin** / **Starlette-Admin** mounted directly at `/admin`.
  - *Engineering Rationale*: Eliminates bespoke React admin development cycles. Automatically generates responsive CRUD views for `Venue`, `BarHop`, and `Subscriber` models.
  - *Spatial Input Mitigation*: Custom latitude/longitude float helpers are exposed in the view model to automatically generate PostGIS `Point(lng lat)` geometries without requiring manual WKT string entry.
- **Endpoints**:
  - `GET /api/v1/venues?bbox={xmin},{ymin},{xmax},{ymax}`: Stream GeoJSON vector data.
  - `GET /api/v1/venues/{slug}`: Detailed establishment metadata.
  - `GET /api/v1/hops`: Retrieve curated bar hop routes.
  - `POST /api/v1/subscribe`: Asynchronous WhatsApp registration.
  - `GET/POST /admin`: SQLAdmin dashboard.

---

## 4. Frontend & Cartographic Engine Specification

- **Framework**: Next.js 16 (App Router) + React 19 + TypeScript
- **Styling**: Tailwind CSS v4 with custom visual theme tokens (`app/globals.css`).
- **Cartographic Engine**: WebGL Spatial Renderer (MapLibre GL JS / Leaflet vector tiles).
  - *Production Rule*: HTML/CSS absolute positioning (`top: %`, `left: %`) is strictly prohibited for production map rendering; it is used only for static visual prototyping.
  - Custom vector tile styling stripping generic map icons and applying the "Osool" color taxonomy.

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
  - `barincairo_frontend`: Next.js 16 standalone server (Local port 127.0.0.1:3000).
- **Host Reverse Proxy**: Host-level Nginx (`nginx.conf.example`) handles SSL termination via Let's Encrypt and proxies `barincairo.com` to `127.0.0.1:3000` and `api.barincairo.com` to `127.0.0.1:8000`.

---

## 7. CI/CD Pipeline & Deployment Strategy

- **Automated Trigger**: GitHub Actions workflow (`.github/workflows/deploy.yml`) on push to `main`.
- **Pipeline Workflow**:
  1. Automated linting and Next.js build verification in GitHub runner.
  2. SSH authentication into host server.
  3. Git pull and container redeployment via `docker compose up -d --build`.
