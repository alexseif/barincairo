# System Architecture Specification: BARINCAIRO.COM

**System Type**: Decoupled Geospatial Directory & Community Routing Platform  
**Target Region**: Downtown Cairo (*Wust El Balad*) — Latitude 30°02′N, Longitude 31°14′E  
**Status**: Draft / Active Architecture  

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
    email VARCHAR(255) UNIQUE NOT NULL,
    source VARCHAR(50) DEFAULT 'web_dispatch',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
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

## 3. Backend Runtime Specification (Python FastAPI)

- **Framework**: FastAPI / AsyncPG (or GeoDjango)
- **Serialization**: `pydantic-geojson` / Native GeoJSON response builders.
- **Endpoints**:
  - `GET /api/v1/venues?bbox={xmin},{ymin},{xmax},{ymax}`: Stream GeoJSON vector data.
  - `GET /api/v1/venues/{slug}`: Detailed establishment metadata.
  - `GET /api/v1/hops`: Retrieve curated bar hop routes.
  - `POST /api/v1/subscribe`: Asynchronous dispatch registration.

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

### Typography Guidelines
- **Primary Script & Serif**: `Cormorant Garamond` (replacing 1950s cinematic hand-painted signage for headings and branding).
- **Geospatial & Technical**: `DM Mono` (coordinates, timestamps, tags, filter toggles).
- **Body & UI**: `DM Sans` / Arabic typography support.
