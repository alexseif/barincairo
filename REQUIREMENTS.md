# Requirement & Operational Axioms Specification: BARINCAIRO.COM

**Project Name**: barincairo.com (Bar in Cairo)  
**Version**: 1.4.0  
**Target Scope**: Downtown Cairo (*Wust El Balad*) — Latitude 30°02′N, Longitude 31°14′E  

---

## 0. Version & Completed Milestones Log

- **Version 1.4.0 Release Notes**:
  - ✅ **Google Analytics (GA4)**: Integrated direct tracking via `@next/third-parties/google` (`NEXT_PUBLIC_GA_ID`).
  - ✅ **PostGIS Data Schema & Initial Seeding**: Populated 15 curated Downtown Cairo establishments, 7 Categories, and 7 Vibe tags in [`backend/app/seed.py`](file:///var/www/barincairo.com/backend/app/seed.py) & synchronized with [`lib/api.ts`](file:///var/www/barincairo.com/lib/api.ts).
  - ✅ **WebGL Vector Map & Filtering**: Interactive MapLibre GL JS map with 44x44px touch targets and in-memory/API filtering by Vibe & Price.

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

## 8. Immediate Feature Elicitation Requirements

- **REQ-8.1 (Interactive Map Selection & Custom Khedivial Tooltip Card)**:
  - **Behavior**: Clicking any venue pin on the map container must display a custom-styled popup/tooltip card.
  - **Aesthetic Alignment**: The popup must adhere to the Khedivial design matrix (`#ede7d8` limestone background, `#24332d` mahogany border, `#ad793b` gold accent linework, 44px minimum touch targets).
  - **Content**: Displays thumbnail photo, Arabic name (`name_ar`), localized name (`translations[lang].name`), vibe tags, price range (`$`–`$$$`), and a CTA link to the venue page.
  - **Architectural Trade-off**: MapLibre native canvas `Popup` vs. a responsive docked bottom card on mobile devices.

- **REQ-8.2 (Multilingual Data Architecture & Extensible i18n Strategy)**:
  - **Axiom**: Arabic (`_ar`) is the native language of Downtown Cairo (*Wust El Balad*) and is **always present** across all venues.
  - **Database & Payload Schema**:
    - Primary Arabic attributes: `name_ar`, `description_ar`, `address_ar`, `vibe_description_ar`.
    - Extensible translation dictionary: `translations` column (JSONB) storing localized key-value pairs for optional languages:
      ```json
      {
        "en": { "name": "Cap D'Or", "description": "...", "address": "..." },
        "nl": { "name": "Cap D'Or", "description": "...", "address": "..." },
        "fr": { "name": "Cap D'Or", "description": "...", "address": "..." }
      }
      ```
  - **Performance**: Prevents schema alteration when adding future languages (e.g. Dutch `nl`, French `fr`) while keeping queries hyper-performant.

- **REQ-8.3 (Vibe & Price Filter Integration)**:
  - **UI Control**: Filter pills for Vibe (`all`, `fancy`, `ambient-music`, `live-performance`, `oud-player`, `old-times`, `dancy`, `flirty`) and Price Range (`all`, `$`, `$$`, `$$$`) positioned above the map container.
  - **Client/Server Contract**: Changing filters triggers instant client-side MapLibre marker updates and re-renders the venue list without full page reloads.

- **REQ-8.4 (User Geolocation & Map Recenter Control)**:
  - **GPS Indicator**: Leverage Browser Geolocation API (`navigator.geolocation`) to render the user's current spatial position as a pulsing gold/emerald pin.
  - **Control Placement**: Add a dedicated "Center on My Location" button positioned directly above the MapLibre zoom controls (`+` / `-`) on the bottom-right corner of the map.

- **REQ-8.5 (Dedicated Venue Detail Pages `/venues/[slug]`)**:
  - Pre-compiled Next.js static pages for all 15 establishments featuring bilingual descriptions, opening hours, photo galleries, navigation links, and `BarOrPub` JSON-LD schemas.

- **REQ-8.6 (WhatsApp Bar Hop / Bar Crawl Subscription API)**:
  - Connect the subscription form to a dedicated backend endpoint for broadcasting curated weekend bar crawls and dispatch alerts to WhatsApp subscribers.

---

## 9. Harness-Friendly AI Subagents & Skills Specification

To enable any autonomous AI agent harness (Antigravity CLI, Gemini-Kit, Claude Code, AutoGen, CrewAI) to execute content ingestion, research, and translation deterministically, subagents are defined as structured harnesses:

### 9.1 Subagent: `cairo-content-researcher`
- **Role**: Cultural & Archival Data Researcher for Downtown Cairo Establishments.
- **Task**: Conduct deep archival and web research on historic Downtown Cairo bars, cafes, and rooftops.
- **Tools Needed**: `search_web`, `read_url_content`, `view_file`, `write_to_file`.
- **System Prompt Specification**:
  ```yaml
  name: cairo-content-researcher
  description: "Researches historical founding dates, literary connections, music genres, and operational details of Cairo nightlife venues."
  input_schema:
    venue_name: "string"
    district: "Downtown Cairo / Wust El Balad"
  output_schema:
    name_ar: "string"
    founding_year: "integer"
    historical_context_ar: "string"
    vibe_tags: ["string"]
    price_range: "string"
    address_ar: "string"
  verification_gate: "Must cite at least 2 independent historical or architectural references."
  ```

### 9.2 Subagent: `spatial-coordinate-verifier`
- **Role**: GIS Spatial Precision & Geocoding Specialist.
- **Task**: Verify exact WGS84 latitude/longitude coordinates and street addresses for establishments in Downtown Cairo.
- **Tools Needed**: `search_web`, `read_url_content`.
- **System Prompt Specification**:
  ```yaml
  name: spatial-coordinate-verifier
  description: "Cross-references establishment locations against OpenStreetMap and Google Maps WGS84 coordinate grids."
  input_schema:
    venue_name: "string"
    address_string: "string"
  output_schema:
    latitude: "float (WGS84)"
    longitude: "float (WGS84)"
    formatted_address_ar: "string"
    formatted_address_en: "string"
    proximity_landmark: "string"
  verification_gate: "Coordinates must fall strictly within 30.0300°N - 30.0600°N and 31.2300°E - 31.2500°E."
  ```

### 9.3 Subagent: `multilingual-translator`
- **Role**: Cultural Localization & i18n Translation Engineer.
- **Task**: Translate native Egyptian Arabic venue descriptions into natural English, Dutch, French, etc., preserving local Cairo atmosphere notes and terminology.
- **Tools Needed**: `view_file`, `write_to_file`.
- **System Prompt Specification**:
  ```yaml
  name: multilingual-translator
  description: "Translates venue attributes into target language dictionaries for JSONB ingestion."
  input_schema:
    name_ar: "string"
    description_ar: "string"
    target_languages: ["en", "nl", "fr"]
  output_schema:
    translations:
      en:
        name: "string"
        description: "string"
        address: "string"
      nl:
        name: "string"
        description: "string"
        address: "string"
  verification_gate: "Must preserve Cairo cultural nuances (e.g. 'Ahwa', 'Baladi Bar', 'Khedivial') without literal mistranslation."
  ```

---

## 10. Future Feature Roadmap & Milestones

- **FUTURE-10.1 (Curated Bar Hops & Spatial Walking Trails)**:
  - Interactive walking routes connecting 3–4 adjacent historic venues with MapLibre spatial polyline overlays.
- **FUTURE-10.2 (PWA & Offline Cartographic Cache)**:
  - Service Worker vector tile and venue data caching for offline street navigation in Downtown Cairo.

---

## 11. The Immutable Aesthetic Matrix (System Directive for UI Subagents)

Future LLM subagents and developers modifying frontend UI files are bound to the following system directive:

```
SYSTEM DIRECTIVE FOR UI AGENTS:
You are strictly bound to the 'Bar in Cairo' design matrix. Reject all Material Design, flat SaaS, or hyper-modern aesthetics.

- Palette: Khedivial Limestone (#ede7d8), Weathered Concrete (#b9ae96), Faded Vintage Gold (#ad793b), Deep Nile Green (#24332d), Dark Mahogany (#24332d text).
- Textures: Apply CSS noise/grain filters simulating archival weathered paper.
- Typography: Bilingual (Arabic/English/Dutch). Serif/Script for primary headers evoking 1950s cinematic signage. Highly legible sans-serif for geographic data.
- Geometry: Sharp, archaic, hand-drawn cartographic linework. Do not use rounded SaaS border-radii.
- Tone: The visual weight must reflect the Osool (الأصول) and historical gravity of Wust El Balad, Cairo.
```
