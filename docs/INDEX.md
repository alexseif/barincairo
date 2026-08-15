# barincairo.com Technical Documentation Portal

Welcome to the **barincairo.com** documentation hub. Our documentation architecture follows the **Diátaxis framework**, organizing information into four distinct quadrants based on your goals.

---

## 🗺️ Diátaxis Documentation Navigation

```
                        LEARNING              PROBLEM
                           │                     │
                           ▼                     ▼
              ┌─────────────────────────┬─────────────────────────┐
              │  🎓 TUTORIALS           │  🛠️ HOW-TO GUIDES        │
  PRACTICAL ──┤  Learning-oriented      │  Problem-oriented       ├── PRACTICAL
              │  Step-by-step onboarding│  Task & workflow guides │
              ├─────────────────────────┼─────────────────────────┤
              │  📖 REFERENCE           │  💡 EXPLANATION          │
 theoretical ──┤  Information-oriented   │  Understanding-oriented │── theoretical
              │  APIs, schemas, config  │  Architecture & concepts│
              └─────────────────────────┴─────────────────────────┘
                           ▲                     ▲
                           │                     │
                      INFORMATION           UNDERSTANDING
```

---

## 1. 🎓 Tutorials (Learning-Oriented)

*Step-by-step lessons for getting up and running with the codebase.*

- **[Getting Started with Local Development](tutorials/getting-started-dev.md)**: Set up PostgreSQL, PostGIS, FastAPI backend, Next.js frontend, and local environment.

---

## 2. 🛠️ How-To Guides (Problem-Oriented)

*Recipes and instructions for solving specific development and operational tasks.*

- **[Running the Data Ingestion Pipeline](how-to/ingestion-pipeline.md)**: Ingest, stage, and enrich Google Maps place data into PostGIS.
- **[Database Migrations Guide](how-to/database-migrations.md)**: Manage SQL schema changes and PostGIS spatial extensions.
- **[Deployment & Infrastructure Guide](how-to/deployment.md)**: Deploy containerized stack using Docker Compose and Nginx.

---

## 3. 📖 Technical Reference (Information-Oriented)

*Detailed technical specifications, APIs, schemas, and configurations.*

- **[REST API Specifications](reference/api-endpoints.md)**: Comprehensive endpoint contracts, GeoJSON payloads, and error models.
- **[PostGIS Database Schema](reference/database-schema.md)**: Spatial tables (`venues`, `venue_staging`), spatial indexes, and CRS specifications.
- **[Environment & Configuration Matrix](reference/environment-variables.md)**: Environment variable definitions and deployment settings.
- **[Development & Code Style Standards](reference/code-standards.md)**: Code style, linting, and project conventions.

---

## 4. 💡 Architecture & Explanation (Understanding-Oriented)

*Background, architectural concepts, decision records, and domain models.*

- **[System Architecture Overview](explanation/architecture-overview.md)**: High-level C4 diagrams, decoupled cartography & spatial backend logic.
- **[Geospatial Querying Strategy](explanation/geospatial-model.md)**: PostGIS bounding box filtering, SRID 4326 projections, and spatial indexing.
- **[Multilingual JSONB Harness](explanation/multilingual-strategy.md)**: Multi-language content modeling for Downtown Cairo venues.
- **[Architectural Decision Records (ADRs)](explanation/adr/INDEX.md)**: Documented architectural choices (e.g. PostGIS vs. standard relational engine).

---

## 📄 Existing Root Architecture Files (Quick Access)

For legacy cross-reference:
- [`ARCHITECTURE.md`](../ARCHITECTURE.md) - System architecture specification
- [`REQUIREMENTS.md`](../REQUIREMENTS.md) - Functional and non-functional requirements
- [`SPEC.md`](../SPEC.md) - Functional specifications
- [`STANDARDS.md`](../STANDARDS.md) - Code standards and rules
- [`DEPLOYMENT.md`](../DEPLOYMENT.md) - Production deployment guide
