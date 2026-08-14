# barincairo.com (الأصول / Downtown Cairo Nightlife Index)

> A decoupled geospatial directory and community routing platform indexing, mapping, and facilitating navigation of nightlife establishments within downtown Cairo (*Wust El Balad*).

---

## 🏛️ Project Overview

**barincairo.com** is a specialized cartographic and cultural index dedicated to the historic establishments, rooftop hideouts, hotel lounges, and backroom cocktail bars of Downtown Cairo. Built with a rich historical aesthetic rejecting sterile SaaS/Material design, the platform combines modern geospatial rendering with 1950s cinematic hand-painted typography and weathered urban cartography.

---

## 📜 Architectural Standards & Documentation

The project governance and architectural standards are codified across primary specification files:

1. **[`DEPLOYMENT.md`](./DEPLOYMENT.md)**: Secure Ubuntu server setup guide, host co-location safety (WordPress/Symfony protection), and GitHub Actions SSH deployment configuration.
2. **[`STANDARDS.md`](./STANDARDS.md)**: Coding standards, security protocols, 3NF database schema, Star Schema analytics analysis, framework directory layouts, and the **Planner/Building Agent token protocol**.
3. **[`ARCHITECTURE.md`](./ARCHITECTURE.md)**: Technical specs for decoupled Next.js + FastAPI + PostGIS infrastructure, Docker container isolation, SQLAdmin dashboard, host Nginx proxy, and spatial query patterns.
4. **[`REQUIREMENTS.md`](./REQUIREMENTS.md)**: Functional/non-functional requirements, Web Vitals performance targets ($LCP \le 1.2s$), JSON-LD SEO schemas, `/llm.txt` GEO endpoints, and agent orchestration directives.
5. **[`docs/ingestion-pipeline.md`](./docs/ingestion-pipeline.md)**: Operational guide for Google Places/Maps extraction, PostGIS staging, AI cultural enrichment, main hero photo selection, 2-citation verification gate, and production promotion.

---

## 🔐 Security & Environment Configuration

Zero credentials or secret keys are committed to version control.

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Populate `.env` with strong, generated passwords (`POSTGRES_PASSWORD`, `SECRET_KEY`).
3. Run container orchestration safely:
   ```bash
   docker compose up -d
   ```

---

## 📐 System Architecture Overview

```
 ┌─────────────────────────────────────────┐
 │     Next.js 16 / React 19 Frontend      │
 │  (MapLibre GL JS / Leaflet Vector Tiles)│
 └────────────────────┬────────────────────┘
                      │
            GeoJSON Stream API (HTTPS)
                      │
 ┌────────────────────▼────────────────────┐
 │  Python (FastAPI) + SQLAdmin Backend    │
 └────────────────────┬────────────────────┘
                      │
               SQL / PostGIS Spatial
                      │
 ┌────────────────────▼────────────────────┐
 │  PostgreSQL + PostGIS Database (SRID 4326) │
 └─────────────────────────────────────────┘
```

---

## 🔌 Hybrid Content Ingestion Pipeline

Continuous venue discovery, extraction, enrichment, and promotion pipeline:

```bash
# 1. Deterministic Google Maps Extraction (Phase 1)
PYTHONPATH=. venv/bin/python scripts/extract_gmaps_venues.py --bbox "30.0380,31.2300,30.0520,31.2480"

# 2. AI Cultural Enrichment & 2-Citation Gate (Phase 2)
PYTHONPATH=. venv/bin/python -m app.cli enrich-staged

# 3. Production Promotion & PostGIS Ingestion (Phase 3)
PYTHONPATH=. venv/bin/python -m app.cli promote-staged --all
```

For detailed bounding box parameters, custom neighborhood configuration, and deduplication rules, see **[`docs/ingestion-pipeline.md`](./docs/ingestion-pipeline.md)**.

---

## 🤖 Session Resume & Agent Execution Directive

When starting a new session or resuming work on this codebase, AI Agents must adhere to the following protocol:

- **Phase 1 Planning Trigger**: The user prompt `"Proceed with Phase 1 Planning"` (or `/plan`) triggers the **Planner Agent**.
- **Planner Agent Protocol**: The Planner Agent must parse the specifications, break Phase 1 into sequential tasks, estimate **Token Cost & Resource Scope**, and obtain explicit **Human Approval** before any Building Agent starts coding.

### Development Roadmap
- [x] **Phase 1: Scaffolding & Visual Prototype**: DOM structure, CSS tokens, bilingual typography, static `/llm.txt` GEO route, and Docker/CI deployment guide.
- [ ] **Phase 2: Platform Engineering & Infrastructure Build**: PostGIS 3NF schema, FastAPI GeoJSON streaming API, SQLAdmin dashboard, and WebGL MapLibre GL JS cartography integration.
- [ ] **Phase 3: Data Ingestion & Content Population**: Historic Downtown venue curation, WGS84 spatial coordinate verification, and WhatsApp community dispatch integration.

---

## 📜 License

Licensed under the MIT License. Copyright © 2026 barincairo.com.
