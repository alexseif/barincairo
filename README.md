# barincairo.com (الأصول / Downtown Cairo Nightlife Index)

> A decoupled geospatial directory and community routing platform indexing, mapping, and facilitating navigation of nightlife establishments within downtown Cairo (*Wust El Balad*).

---

## 🏛️ Project Overview

**barincairo.com** is a specialized cartographic and cultural index dedicated to the historic establishments, rooftop hideouts, hotel lounges, and backroom cocktail bars of Downtown Cairo. Built with a rich historical aesthetic rejecting sterile SaaS/Material design, the platform combines modern geospatial rendering with 1950s cinematic hand-painted typography and weathered urban cartography.

### Visual Identity & "Osool" (الأصول)
- **Palette**: Khedivial Limestone (`#ede7d8`), Weathered Concrete (`#b9ae96`), Faded Vintage Gold (`#ad793b`), Deep Nile Green (`#24332d`), and Dark Mahogany.
- **Typography**: Dual bilingual typography (Arabic & English) featuring serif/script fonts (`Cormorant Garamond`) echoing classic Talaat Harb signage paired with clean monospace/sans-serif (`DM Mono`, `DM Sans`) for spatial precision.
- **Texture**: Archival cartography styling, custom noise overlay, and linework simulating hand-drawn urban grids.

---

## 📐 System Architecture

The system is designed as a **decoupled geospatial directory**:

```
 ┌─────────────────────────────────────────┐
 │     Next.js 16 / React 19 Frontend      │
 │  (MapLibre GL JS / Leaflet Vector Tiles)│
 └────────────────────┬────────────────────┘
                      │
            GeoJSON Stream API (HTTPS)
                      │
 ┌────────────────────▼────────────────────┐
 │         Python (FastAPI) Backend        │
 └────────────────────┬────────────────────┘
                      │
               SQL / PostGIS Spatial
                      │
 ┌────────────────────▼────────────────────┐
 │  PostgreSQL + PostGIS Database (SRID 4326) │
 └─────────────────────────────────────────┘
```

- **Frontend**: Next.js 16 (App Router), React 19, Tailwind CSS v4, MapLibre GL JS / Leaflet spatial rendering engine.
- **Backend API**: Python (FastAPI) serving pure GeoJSON object collections.
- **Geospatial Engine**: PostgreSQL with PostGIS extension operating under **SRID 4326 (WGS 84)**.

For full architectural details, see [`ARCHITECTURE.md`](./ARCHITECTURE.md).  
For functional requirements and phase milestones, see [`REQUIREMENTS.md`](./REQUIREMENTS.md).

---

## 🚀 Quick Start (Frontend Prototype)

### Prerequisites
- Node.js 18+
- `npm` or `pnpm`

### Installation & Execution

```bash
# Install dependencies
npm install

# Run local development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the current frontend prototype.

---

## 🗺️ Roadmap & Milestones

- [x] **Phase 1: Scaffolding & Visual Scaffolding**: Lock DOM structure, Tailwind CSS tokens, bilingual typography, and responsive layout.
- [ ] **Phase 2: Database Provisioning**: Spin up PostgreSQL + PostGIS, define spatial schemas, and seed initial 15-20 Wust El Balad locations.
- [ ] **Phase 3: Python API Construction**: Implement FastAPI endpoints serving GeoJSON streams with bounding box and nearest-neighbor spatial queries.
- [ ] **Phase 4: Cartographic Integration**: Replace prototype CSS map layer with WebGL MapLibre GL / Leaflet spatial renderer bound to backend endpoints.
- [ ] **Phase 5: Production & Verification**: Execute type checking, bundle optimization, SEO verification, and launch deployment.

---

## 📜 License

Licensed under the MIT License. Copyright © 2026 barincairo.com.
