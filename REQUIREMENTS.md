# Requirement Specification Sheet: BARINCAIRO.COM

**Project Name**: barincairo.com (Bar in Cairo)  
**Version**: 1.0.0-draft  
**Target Scope**: Downtown Cairo (*Wust El Balad*)  

---

## 1. Functional Requirements

### 1.1 Cartographic & Map Interface
- **FR-1.1**: The application must render an interactive vector map of Downtown Cairo with custom tiles suppressing default commercial labels.
- **FR-1.2**: The map must ingest GeoJSON streams from the backend API dynamically based on viewport bounding box changes.
- **FR-1.3**: Establishments must be represented as custom vector pins with active/hover animation effects styled according to the "Osool" color matrix.
- **FR-1.4**: Non-establishment landmark markers (Tahrir Square, Egyptian Museum, Talaat Harb Square) must be rendered as reference points.

### 1.2 Detail Panel & Establishment Listing
- **FR-2.1**: Clicking a bar pin must select the venue and update the detail panel without triggering a full page reload.
- **FR-2.2**: The detail panel must display:
  - Venue English and Arabic titles (e.g., Cairo Jazz Club 610 / كايرو جاز كلوب).
  - Venue category taxonomy (Live music, Cocktail bar, Rooftop, Cafe bar).
  - Absolute coordinate address and neighbourhood.
  - Atmosphere/Vibe tag.
  - High-resolution photography.
  - Narrative description.

### 1.3 Filtering Mechanics
- **FR-3.1**: Users must be able to filter map pins by category (e.g., live music, rooftop, dive bars, historic spots).
- **FR-3.2**: Filtering toggles must update the rendered GeoJSON layer client-side or re-query spatial endpoints cleanly.

### 1.4 Bar Hops & Community Layer
- **FR-4.1**: The platform must present curated bar hop routes (e.g., 4 stops, 4-hour guided/self-guided trails).
- **FR-4.2**: Users must have access to a registration interest funnel for upcoming bar hop events.

### 1.5 Subscriptions & Dispatch
- **FR-5.1**: An asynchronous POST form must accept WhatsApp phone numbers for direct message notifications and dispatch updates.
- **FR-5.2**: The UI must display an instant feedback state upon successful subscription ("You’re on the list. Ahla wa sahla.").

### 1.6 Future Scope (Dormant Module)
- **FR-6.1**: Premium sponsor venue listings with priority map marker placement (Module locked until traffic threshold met).

---

## 2. Non-Functional Requirements

### 2.1 Performance
- **NFR-1.1**: Page load time under 1.5s on mobile and desktop over standard 4G connections.
- **NFR-1.2**: GeoJSON stream responses payload optimized (<50KB for viewport queries).

### 2.2 Aesthetics & User Experience
- **NFR-2.1**: Compliance with the "Osool" identity palette (Khedivial Limestone `#ede7d8`, Nile Green `#24332d`, Weathered Gold `#ad793b`).
- **NFR-2.2**: Bilingual typography support for Arabic and English rendering.
- **NFR-2.3**: Smooth CSS noise/grain texture overlay simulating weathered archival urban paper.

### 2.3 SEO & Accessibility
- **NFR-3.1**: Semantic HTML5 markup structure with proper ARIA attributes for interactive map elements and inputs.
- **NFR-3.2**: Open Graph and Twitter Card metadata configured for Cairo tourism and nightlife sharing.

---

## 3. Development Phase Milestones

| Phase | Title | Key Deliverables | Status |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Visual & Technical Scaffolding | Next.js 16 setup, CSS tokens, font loading, layout scaffolding, prototype map | **Completed** |
| **Phase 2** | Database & Spatial Schema | PostgreSQL + PostGIS setup, spatial schema creation, seed dataset (15-20 Downtown spots) | *Pending* |
| **Phase 3** | Python GeoJSON API Construction | FastAPI setup, GeoJSON bounding box endpoints, spatial proximity queries | *Pending* |
| **Phase 4** | WebGL Cartographic Integration | MapLibre GL JS / Leaflet vector map integration replacing CSS prototype | *Pending* |
| **Phase 5** | Production Readiness & Audit | Type safety verification, bundle size reduction, SEO tags, deployment pipelines | *Pending* |
