# Requirement & Operational Axioms Specification: BARINCAIRO.COM

**Project Name**: barincairo.com (Bar in Cairo)  
**Version**: 1.3.0  
**Target Scope**: Downtown Cairo (*Wust El Balad*) — Latitude 30°02′N, Longitude 31°14′E  

---

## 1. Security Protocols: Secure by Design

- **SEC-1.1 (Zero-Trust Data Ingestion)**: All spatial coordinates, JSON inputs, and string data entering the Python (FastAPI) backend must be mathematically validated via Pydantic schemas. Malformed payloads must be rejected with HTTP 422 immediately.
- **SEC-1.2 (SQL Injection Immunity)**: Direct raw SQL string execution is strictly prohibited. All spatial operations must execute through GeoAlchemy2 parameterized ORM methods.
- **SEC-1.3 (Network Isolation)**: Next.js frontend to FastAPI communication occurs strictly via the internal Docker bridge network (`barincairo_net`). PostGIS must be bound exclusively to `127.0.0.1` / internal container interfaces and never exposed externally.
- **SEC-1.4 (Zero-Secrets in Code Control)**: No hardcoded database passwords, secret keys, or credentials are allowed in source code or `docker-compose.yml`. Secrets must be loaded exclusively via `.env` configured from `.env.example`.
- **SEC-1.5 (Token-Bucket Rate Limiting)**: Implement token-bucket rate limiting on all public GeoJSON and venue endpoints to prevent scraping bots from consuming server resources.

---

## 2. Structural Integrity & Coding Standards

- **CODE-2.1 (Python Strictness)**: Backend Python codebase must maintain 100% PEP-8 compliance enforced via `ruff` and strict static typing via `mypy`. All functions must explicitly declare return types.
- **CODE-2.2 (TypeScript & CI Enforcement)**: Frontend TypeScript configuration must enforce `"strict": true` in `tsconfig.json`. Use of the `any` type is banned. ESLint + Prettier verification is enforced in GitHub Actions (`.github/workflows/deploy.yml`). Linting failures trigger an immediate deployment abort.
- **CODE-2.3 (State Management & RSC)**: React components must be decoupled from data fetching. Leverage React Server Components (RSC) for initial static HTML generation, isolating client state strictly to the interactive cartography container (MapLibre GL JS / Leaflet).

---

## 3. Geometric Rules & Mobile-First Design

- **GEO-3.1 (Mobile Axiom)**: Baseline CSS targets mobile viewports first (street-level foot navigation via smartphones in Cairo).
- **GEO-3.2 (Progressive Enhancement)**: Desktop views are applied strictly as geometric overrides using Tailwind CSS breakpoints (e.g. `md:grid-cols-2`).
- **GEO-3.3 (Touch Target Geometry)**: All interactive map pins, navigation buttons, category toggles, and CTAs must possess a physical touch target of at least **44x44 CSS pixels** to satisfy WCAG standards.

---

## 4. The Mechanical Truth: Web Vitals & Performance

- **PERF-4.1 (Performance Benchmarks)**: Target 100/100 Lighthouse Mobile score with LCP (Largest Contentful Paint) $\le 1.2$ seconds and TTFB (Time to First Byte) under 200ms.
- **PERF-4.2 (Static Site Generation for Listings)**: Venue detail views must be pre-compiled via Next.js SSG. PostGIS spatial stream data is fetched dynamically *only* when the interactive map renders.
- **PERF-4.3 (Asset Compression)**: All visual assets (Khedivial textures, photography) must be compressed in WebP/AVIF formats capped at $\le 80\text{KB}$ per asset.

---

## 5. Search Engine Optimization (SEO) & Knowledge Graph

- **SEO-5.1 (JSON-LD Structured Data)**: Every venue page and index view must inject `LocalBusiness` and `BarOrPub` JSON-LD schemas into `<head>`, including exact `geo` coordinates, `openingHoursSpecification`, `addressLocality: Downtown / Wust El Balad`, and `priceRange`.
- **SEO-5.2 (Semantic Hierarchy)**: Use semantic HTML5 `<article>`, `<aside>`, `<nav>`, `<header>`, and `<footer>` elements with strict `H1` $\rightarrow$ `H2` $\rightarrow$ `H3` heading cascades.
- **SEO-5.3 (Entity Linking)**: Utilize the `sameAs` schema property to link Cairo establishments to their Wikipedia pages or official cultural records.

---

## 6. Generative Engine Optimization (GEO): LLM Ingestion

- **GEO-6.1 (Dedicated Machine Routes `/llm.txt` & `/ai.txt`)**: Expose raw, compressed, markdown-formatted directory routes at `/llm.txt` and `/ai.txt` for AI web crawlers (ChatGPT, Gemini, Claude) without requiring JavaScript execution.
- **GEO-6.2 (High-Density Factual Structuring)**: Operational data (Vibe, Music Genre, Smoking Policy, Proximity) must be structured in HTML `<table>` or `<ul>` formats for optimal LLM retrieval-augmented generation (RAG).

---

## 7. Session Resume & Agent Execution Protocol

- **SER-7.1 (Trigger Recognition)**: When a new agent session is initialized, the trigger prompt `"Proceed with Phase 1 Planning"` (or `/plan`) instructs the agent to enter Planner Agent mode.
- **SER-7.2 (Mandatory Task & Token Estimate)**: The Planner Agent must parse `REQUIREMENTS.md` and `STANDARDS.md`, create an atomic task list, calculate **Token Cost & Resource Estimates**, and request **Human Approval** before any building agent executes code.

---

## 8. Next Steps & Agent/Skill Orchestration Plan

The project development must follow a two-phase agent orchestration plan:

### Phase 1: Engineering & Infrastructure Build (Agents & Skills)
- **FastAPI / PostGIS Specialist Agent**: Provision PostgreSQL + PostGIS 3NF database schema, Alembic migrations, and GeoJSON endpoints.
- **WebGL MapLibre Specialist Agent**: Replace prototype CSS map with MapLibre GL JS vector tiles consuming live GeoJSON streams.
- **DevOps Engineer Agent**: Finalize Docker Compose orchestration, SSL certificates, and GitHub Actions CD deployment.

### Phase 2: Data Ingestion & Content Population (Agents & Skills)
- **Cairo Content Researcher Agent**: Curate initial 15–20 historic Downtown Cairo establishments, English/Arabic descriptions, and vibe taxonomies.
- **Spatial Coordinate Verifier Agent**: Cross-reference exact WGS84 lat/lng coordinates against OpenStreetMap/Google Maps for precision PostGIS entry.

---

## 9. Planner & Building Agent Protocol (Cost & Approval Rule)

- **PLN-9.1 (Mandatory Task Breakdown)**: Before any code is written or modified, a **Planner Agent** must break down the scope into clear, atomic, sub-task steps.
- **PLN-9.2 (Token & Resource Estimate)**: The Planner Agent must calculate and disclose an estimated token cost and resource scope for both Phase 1 (Engineering Build) and Phase 2 (Data Ingestion).
- **PLN-9.3 (Human Approval Gate)**: A Building Agent is **forbidden** from executing commands or creating files until explicit human approval ("Proceed", "Yes", or approved option) is granted.

---

## 10. The Immutable Aesthetic Matrix (System Directive for UI Subagents)

Future LLM subagents and developers modifying frontend UI files are bound to the following system directive:

```
SYSTEM DIRECTIVE FOR UI AGENTS:
You are strictly bound to the 'Bar in Cairo' design matrix. Reject all Material Design, flat SaaS, or hyper-modern aesthetics.

- Palette: Khedivial Limestone (#ede7d8), Weathered Concrete (#b9ae96), Faded Vintage Gold (#ad793b), Deep Nile Green (#24332d), Dark Mahogany (#24332d text).
- Textures: Apply CSS noise/grain filters simulating archival weathered paper.
- Typography: Bilingual (Arabic/English). Serif/Script for primary headers evoking 1950s cinematic signage. Highly legible sans-serif for geographic data.
- Geometry: Sharp, archaic, hand-drawn cartographic linework. Do not use rounded SaaS border-radii.
- Tone: The visual weight must reflect the Osool (الأصول) and historical gravity of Wust El Balad, Cairo.
```
