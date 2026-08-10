# barincairo.com (الأصول / Downtown Cairo Nightlife Index)

> A decoupled geospatial directory and community routing platform indexing, mapping, and facilitating navigation of nightlife establishments within downtown Cairo (*Wust El Balad*).

---

## 🏛️ Project Overview

**barincairo.com** is a specialized cartographic and cultural index dedicated to the historic establishments, rooftop hideouts, hotel lounges, and backroom cocktail bars of Downtown Cairo. Built with a rich historical aesthetic rejecting sterile SaaS/Material design, the platform combines modern geospatial rendering with 1950s cinematic hand-painted typography and weathered urban cartography.

---

## 📜 Architectural Standards & Documentation

The project governance and architectural standards are codified across four primary specification files:

1. **[`STANDARDS.md`](./STANDARDS.md)**: Coding standards, security protocols, 3NF database schema, Star Schema analytics analysis, framework directory layouts, and the **Planner/Building Agent token protocol**.
2. **[`ARCHITECTURE.md`](./ARCHITECTURE.md)**: Technical specs for decoupled Next.js + FastAPI + PostGIS infrastructure, Docker container isolation, SQLAdmin dashboard, host Nginx proxy, and spatial query patterns.
3. **[`REQUIREMENTS.md`](./REQUIREMENTS.md)**: Functional/non-functional requirements, Web Vitals performance targets ($LCP \le 1.2s$), JSON-LD SEO schemas, `/llm.txt` GEO endpoints, and agent orchestration directives.
4. **[`README.md`](./README.md)**: Quick start guide, repository layout, and project status.

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

## 🗺️ Dynamic Data Evolution & Agent Protocol

> **Prototype Note**: Phase 1 uses sample static venue data to validate DOM hierarchy, visual tokens, and machine-readable `/llm.txt` endpoints.

### Two-Phase Agent Orchestration Protocol
- **Planner Agent**: Responsible for analyzing specifications, creating granular step-by-step tasks, calculating **Token Cost & Resource Estimates**, and obtaining **Human Approval** before any building agent executes code.
- **Building Agent**: Responsible for executing approved task breakdowns while adhering strictly to token budget constraints and quality gates.

### Development Roadmap
- [x] **Phase 1: Scaffolding & Visual Prototype**: DOM structure, CSS tokens, bilingual typography, static `/llm.txt` GEO route, and Docker/CI infrastructure.
- [ ] **Phase 2: Platform Engineering & Infrastructure Build**: PostGIS 3NF schema, FastAPI GeoJSON streaming API, SQLAdmin dashboard, and WebGL MapLibre GL JS cartography integration.
- [ ] **Phase 3: Data Ingestion & Content Population**: Historic Downtown venue curation, WGS84 spatial coordinate verification, and WhatsApp community dispatch integration.

---

## 📜 License

Licensed under the MIT License. Copyright © 2026 barincairo.com.
