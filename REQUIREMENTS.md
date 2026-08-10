# Requirement & Operational Axioms Specification: BARINCAIRO.COM

**Project Name**: barincairo.com (Bar in Cairo)  
**Version**: 1.1.0  
**Target Scope**: Downtown Cairo (*Wust El Balad*) — Latitude 30°02′N, Longitude 31°14′E  

---

## 1. Security Protocols: Secure by Design

- **SEC-1.1 (Zero-Trust Data Ingestion)**: All spatial coordinates, JSON inputs, and string data entering the Python (FastAPI) backend must be mathematically validated via Pydantic schemas. Malformed payloads must be rejected with HTTP 422 immediately.
- **SEC-1.2 (SQL Injection Immunity)**: Direct raw SQL string execution is strictly prohibited. All spatial operations must execute through GeoAlchemy2 parameterized ORM methods.
- **SEC-1.3 (Network Isolation)**: Next.js frontend to FastAPI communication occurs strictly via the internal Docker bridge network (`barincairo_net`). PostGIS must be bound exclusively to `127.0.0.1` / internal container interfaces and never exposed externally.
- **SEC-1.4 (Token-Bucket Rate Limiting)**: Implement token-bucket rate limiting on all public GeoJSON and venue endpoints to prevent scraping bots from consuming server resources.

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

## 7. Dark Social & Physical Street Protocol

- **PHYS-7.1 (WhatsApp Dispatch Conversion)**: The primary subscriber funnel is routed through WhatsApp direct messaging instead of email.
- **PHYS-7.2 (NFC & QR Street Integration)**: Physical NFC tags and QR codes in Downtown venues route patrons directly to individual venue URLs on `barincairo.com` to drive high-intent direct search traffic.

---

## 8. The Immutable Aesthetic Matrix (System Directive for UI Subagents)

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
