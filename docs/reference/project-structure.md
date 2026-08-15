# Project Structure Reference & Audit: barincairo.com

**Version**: 1.0.0  
**Framework Stack**: Decoupled Architecture (Next.js 14+ Frontend / FastAPI Python 3.11+ Backend)  
**Standard Compliance**: Grey Haven Studio Project Standards  

---

## 1. High-Level Repository Layout

`barincairo.com` implements a **Decoupled Geospatial Platform Architecture**, hosting the Next.js presentation engine in the repository root and the Python spatial API & ingestion service under `backend/`.

```
barincairo.com/
├── app/                         # Next.js App Router Pages & Layouts
│   ├── layout.tsx               # Root application shell & font loading
│   ├── page.tsx                 # Main interactive geospatial map view
│   ├── globals.css              # Core Tailwind & custom spatial CSS
│   ├── ai.txt/                  # AI crawler context endpoints
│   └── llm.txt/                 # LLM documentation endpoints
├── components/                  # React Presentation Components
│   ├── map/                     # Spatial Cartography & Interactive Map Components
│   │   ├── VenueMap.tsx         # Mapbox GL / MapLibre vector renderer
│   │   ├── BarHopDrawer.tsx     # Route planning drawer component
│   │   └── FilterPills.tsx      # Taxonomy & vibe filter controls
│   └── ui/                      # Reusable UI Controls (Shadcn / Radix)
├── lib/                         # Frontend Core Utilities & API Connectors
│   ├── api.ts                   # GeoJSON API client & fetch wrappers
│   ├── config.ts                # Client-side map & env settings
│   └── utils.ts                 # Classname merge & helper utilities
├── backend/                     # Decoupled Python FastAPI Backend
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── cli.py               # Ingestion CLI commands & data tasks
│   │   ├── seed.py              # Database seeding harness
│   │   ├── admin/               # SQLAdmin curation panel views
│   │   ├── api/                 # REST & GeoJSON API endpoint routers
│   │   ├── core/                # Database engine, session, & config settings
│   │   ├── models/              # SQLModel & PostGIS spatial entity schemas
│   │   └── schemas/             # Pydantic input/output validation schemas
│   ├── migrations/              # Alembic SQL & PostGIS migration scripts
│   ├── scripts/                 # Utility & automated extraction scripts
│   └── tests/                   # Pytest test suite (unit, integration, e2e)
├── docs/                        # Diátaxis Documentation Hub
│   ├── INDEX.md                 # Central documentation portal index
│   ├── tutorials/               # Learning guides (e.g. getting-started-dev.md)
│   ├── how-to/                  # Task-focused guides (e.g. ingestion-pipeline.md)
│   ├── reference/               # Technical specs & database schema reference
│   └── explanation/             # System architecture & design decision records
└── public/                      # Static web assets, markers, & favicon
```

---

## 2. Naming Conventions & Coding Standards

| Asset Type | Convention | Example File / Symbol |
| :--- | :--- | :--- |
| **React Components** | `PascalCase.tsx` | `components/map/VenueMap.tsx` |
| **Frontend Utilities** | `camelCase.ts` | `lib/api.ts`, `lib/utils.ts` |
| **Python Modules** | `snake_case.py` | `backend/app/models/venue.py` |
| **Python Classes / Models** | `PascalCase` | `class Venue(SQLModel)` |
| **Database Tables & Columns**| `snake_case` | `venues`, `location`, `price_range` |
| **TypeScript Path Aliases** | `@/*` (root alias) | `import { fetchVenues } from "@/lib/api"` |

---

## 3. Structural Compliance Matrix

| Architecture Dimension | Target Standard | Current Status | Alignment Notes |
| :--- | :--- | :--- | :--- |
| **Decoupled Architecture** | Spatial API separated from UI cartography | ✅ Fully Compliant | FastAPI serves GeoJSON; Next.js handles presentation. |
| **Backend Layering** | Routers → Services → Models → Schemas | ✅ Fully Compliant | `app/api/`, `app/models/`, `app/schemas/`, `app/core/` cleanly isolated. |
| **Frontend Component Organization** | UI components in `components/ui`, feature components in `components/map` | ✅ Fully Compliant | High cohesion; map controls separated from UI elements. |
| **Documentation Alignment** | Diátaxis 4-Quadrant documentation hub in `docs/` | ✅ Fully Compliant | Structured under `docs/` with central index at `docs/INDEX.md`. |

---

## 4. Maintenance Guidelines

1. **Adding Backend Endpoints**: Add router files to `backend/app/api/v1/endpoints/` and register them in `backend/app/api/v1/api.py`.
2. **Adding Database Models**: Define SQLModel schemas in `backend/app/models/` using PostGIS `Geometry` types and snake_case fields.
3. **Adding React Components**: Place UI controls in `components/ui/` using `PascalCase.tsx`.
