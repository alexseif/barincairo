# Architectural Standards & Operational Guidelines: BARINCAIRO.COM

**Status**: Active Guidelines & Architecture Framework  
**Scope**: Standards for Human Developers & AI Agents  

---

## 1. Prototype Context & Dynamic Data Roadmap

> **Current State**: The Phase 1 frontend prototype utilizes static sample venue data and a mock map layout to lock in the visual identity, DOM hierarchy, and Tailwind CSS design tokens.

### Future Dynamic Data Pipeline (Phase 2 & 3 Evolution)
1. **Dynamic Spatial API**: The static array will be replaced by live FastAPI endpoints streaming GeoJSON collections from PostGIS (`GET /api/v1/venues?bbox=...`).
2. **Dynamic Machine Routes**: `/llm.txt` and `/ai.txt` routes will dynamically fetch venue records from PostGIS (with server-side revalidation caching) rather than serving static text.
3. **Admin Panel Management**: SQLAdmin (`/admin`) will allow adding, updating, and categorizing Cairo establishments in real time without code modifications or redeployments.

---

## 2. Security Patterns & Git Hygiene

### 2.1 Secrets & Credentials Management
- **Zero Credentials in Version Control**: `.env` files, API keys, database passwords, and SSH keys must NEVER be committed.
- **Environment Template**: Maintain a sanitized `.env.example` in the repository containing dummy keys. `docker-compose.yml` must read variables exclusively from `.env`.
- **Automated Scanning**: Enforce GitHub Secret Scanning or `gitleaks` in the CI/CD pipeline to block accidental key leaks.

### 2.2 API Security & Network Boundary
- **CORS Configuration**: Restrict FastAPI CORS middleware strictly to `https://barincairo.com` and `http://localhost:3000` (development).
- **Content Security Policy (CSP)**: Send strict HTTP security headers from Next.js and host Nginx to mitigate XSS and injection attacks.
- **Authentication**: SQLAdmin dashboard authenticated via bcrypt-hashed admin passwords using secure HTTP-only cookies.

---

## 3. Database Architecture: 3NF & Dimensional Star Schema Analysis

### 3.1 3rd Normal Form (3NF) Relational Schema (Transactional OLTP)

To ensure data integrity, eliminate redundancy, and maintain clean spatial relationships, the primary database schema follows **3NF**:

```
 ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
 │   categories    │       │     venues      │       │  venue_photos   │
 ├─────────────────┤       ├─────────────────┤       ├─────────────────┤
 │ id (PK)         │1     *│ id (PK)         │1     *│ id (PK)         │
 │ slug (UQ)       ├───────┤ category_id(FK) ├───────┤ venue_id (FK)   │
 │ name_en         │       │ slug (UQ)       │       │ photo_url       │
 │ name_ar         │       │ name_en/ar      │       │ caption         │
 └─────────────────┘       │ location (Pt)   │       └─────────────────┘
                           │ is_active       │
                           └────────┬────────┘
                                    │1
                                    │
                                   *│ (Junction)
                           ┌────────┴────────┐
                           │   venue_vibes   │
                           ├─────────────────┤
                           │ venue_id (FK)   │
                           │ vibe_id (FK)    │
                           └─────────────────┘
```

#### Core Entities:
- **`venues`**: Primary establishment records containing PostGIS `Point` geometry (SRID 4326).
- **`categories`**: Venue taxonomies (`Live music`, `Cocktail bar`, `Rooftop`, `Cafe bar`).
- **`vibe_tags` & `venue_vibes`**: Many-to-many relationship supporting flexible filtering tags (e.g. *Golden Hour*, *Late-Night*, *Intimate*).
- **`venue_photos`**: One-to-many photography gallery.
- **`bar_hops` & `bar_hop_stops`**: Ordered junction table connecting venues into curated trail routes.
- **`subscribers`**: WhatsApp registration data (`whatsapp_number`, `source`, `created_at`).

### 3.2 Dimensional Modeling (Star Schema for Analytics)

If analytics scaling is required in future phases (e.g., tracking spatial heatmaps, pin click density, or hop route conversions):

- **OLTP vs OLAP Separation**: Transactional queries run on 3NF + PostGIS spatial indexes. Analytics should be isolated into read-only materialized views or a separate Star Schema data model:
  - **Fact Table**: `fact_venue_interactions` (interaction_id, venue_id, interaction_type, timestamp_id, location_id).
  - **Dimension Tables**: `dim_venue`, `dim_time`, `dim_location`.

---

## 4. Architectural Design Patterns & Separation of Concerns

### 4.1 Layered Backend Architecture (FastAPI)
```
API Routers (Pydantic Validation & HTTP Contracts)
      │
  Service Layer (Business Logic & Spatial Calculations)
      │
Repository / DAO Layer (GeoAlchemy2 & PostGIS Queries)
      │
Database (PostgreSQL + PostGIS)
```

### 4.2 Frontend Component Architecture (Next.js 16)
- **React Server Components (RSC)**: Used by default for initial HTML generation, SEO JSON-LD injection, and static layouts.
- **Client Components (`'use client'`)**: Restricted strictly to interactive UI boundaries (WebGL map canvas, touch filter toggles, search inputs).

---

## 5. Framework Directory Standards & Git Workflow

### 5.1 Backend Directory Layout Standard
```
backend/
├── app/
│   ├── core/          # Config, security, DB session setup
│   ├── models/        # GeoAlchemy2 & SQLAlchemy 3NF models
│   ├── schemas/       # Pydantic request/response schemas
│   ├── repositories/  # PostGIS database access layer
│   ├── services/      # Spatial logic & business operations
│   ├── api/           # FastAPI v1 route controllers
│   └── admin/         # SQLAdmin dashboard views
├── migrations/        # Alembic database migration scripts
└── tests/             # Pytest suite
```

### 5.2 Frontend Directory Layout Standard
```
barincairo/
├── app/               # Next.js App Router (pages, layouts, /llm.txt)
├── components/
│   ├── ui/            # Reusable primitive controls (buttons, inputs)
│   ├── map/           # WebGL spatial map rendering components
│   └── venue/         # Listing cards & detail panels
├── lib/               # API clients, spatial helpers, formatting
└── public/            # Static compressed visual assets
```

### 5.3 Git Branching & Commit Workflow
- **Branch Strategy**: `main` (protected branch). Development occurs on `feature/*` and `fix/*` branches.
- **Conventional Commits**:
  - `feat:` New features or UI components.
  - `fix:` Bug fixes or type error corrections.
  - `docs:` Documentation or architectural spec updates.
  - `infra:` Docker, CI/CD, or Nginx configuration changes.

---

## 6. Development Do's and Don'ts Matrix

| Category | Do's ✅ | Don'ts ❌ |
| :--- | :--- | :--- |
| **Security** | Validate all API inputs via Pydantic; use parameterized GeoAlchemy2 queries; read credentials from `.env`. | Never run raw SQL strings; never commit API keys or passwords; never hardcode default pass fallbacks. |
| **Frontend** | Enforce 44x44px minimum touch targets; use RSC for static HTML; target mobile viewports first. | Never use TypeScript `any`; never mix client state into server components; do not use SaaS rounded radii. |
| **Backend** | Annotate explicit return types; maintain 100% PEP-8 via `ruff`/`mypy`. | Never bypass Pydantic validation; never expose PostGIS port 5432 to the public internet. |
| **Git & CI** | Write descriptive conventional commits; test builds before pushing. | Never push directly to `main` without build verification. |

---

## 7. Planner & Building Agent Token Protocol & Next Steps

### 7.1 Planner vs Building Agent Workflow Rules
1. **Planner Agent Responsibilities**:
   - Analyze requirements and break down features into explicit, sequential sub-tasks.
   - Calculate and publish an estimated **Token Cost & Resource Budget** for the task.
   - Present the breakdown to the user for **Explicit Human Approval** ("Proceed" or feedback) before any Building Agent starts writing code.
2. **Building Agent Responsibilities**:
   - Execute approved tasks within the allocated token budget.
   - Run verification builds (`npm run build`, `pytest`, `mypy`) after every task step.

### 7.2 Two-Phase Execution Plan

#### Phase 1: Engineering & Infrastructure Build
- **Subagents**: `backend-specialist` (FastAPI/PostGIS/Alembic), `frontend-specialist` (MapLibre GL JS/RSC), `devops-engineer` (Docker/Nginx/CI).
- **Deliverables**: Live database migrations, GeoJSON endpoints, WebGL spatial map rendering, and SQLAdmin setup.

#### Phase 2: Data Ingestion & Content Population
- **Subagents**: `researcher` (Cairo Wust El Balad establishment curation & Arabic metadata), `spatial-verifier` (WGS84 precision coordinate verification).
- **Deliverables**: Seed dataset of 15–20 Downtown Cairo venues, photo asset optimization, and WhatsApp dispatch integration.
