# Technical Specification & Execution Plan: Backend Entity & Admin Updates

**Document Version**: 1.0  
**Project**: Bar in Cairo (`barincairo.com`)  
**Status**: Approved Specification  

---

## 1. Overview & Objectives

Following the interactive `/grill-me` alignment session, the core objectives and technical specs have been defined and updated in [`OBJECTIVE.md`](file:///var/www/barincairo.com/OBJECTIVE.md), [`SPEC.md`](file:///var/www/barincairo.com/SPEC.md), and [`ARCHITECTURE.md`](file:///var/www/barincairo.com/ARCHITECTURE.md).

This document serves as the formal specification and step-by-step implementation plan for the backend edits.

---

## 2. Architectural & Technical Changes

### 2.1 Entity Schema Simplification (English-Only)
* **Rationale**: Simplify multi-language dictionary fields into single English attributes for launch speed and schema cleanliness.
* **Database & ORM Changes**:
  * `Category`: Rename `name_en` $\rightarrow$ `name`. Remove `name_ar`.
  * `VibeTag`: Rename `name_en` $\rightarrow$ `name`. Remove `name_ar`.
  * `Venue`: Rename `name_en` $\rightarrow$ `name`, `address_en` $\rightarrow$ `address`, `description_en` $\rightarrow$ `description`. Remove `name_ar`, `address_ar`, `description_ar`.
* **API Schemas & Endpoints**: Update Pydantic response models (`CategoryResponse`, `VibeTagResponse`, `VenueProperties`, `VenueIngestSchema`) and GeoJSON serializers to output single `name`, `address`, and `description` fields.

### 2.2 Working Hours Display Attribute
* **Rationale**: Provide a clean text representation of operating hours for user interface cards and admin management.
* **Schema Definition**:
  * Add `working_hours: Mapped[str | None] = mapped_column(String(100), nullable=True)` to `Venue` and `VenueStaging`.
  * Format: Simple text range `"from - to"` (e.g., `"5:00 PM - 3:00 AM"` or `"24/7"`).
* **Ingestion & Endpoints**: Include `working_hours` in `VenueIngestSchema`, CLI enrichment scripts, and `GeoJSONFeature` properties.

### 2.3 SQLAdmin Panel Management & 500 Internal Server Error Resolutions
* **Full Entity Management**: Expose List, View, Create, Edit, and Delete (CRUD) views across all 7 domain entities:
  1. `UserAdmin` (`User`)
  2. `CategoryAdmin` (`Category`)
  3. `VibeTagAdmin` (`VibeTag`)
  4. `VenueAdmin` (`Venue`)
  5. `VenueStagingAdmin` (`VenueStaging`)
  6. `VenuePhotoAdmin` (`VenuePhoto`)
  7. `SubscriberAdmin` (`Subscriber`)

* **Fix Venue & VenueStaging Edit 500 Error (PostGIS Geometry)**:
  * *Root Cause*: WTForms / SQLAdmin crashes when attempting to render or convert GeoAlchemy2 `Geometry(Point)` fields.
  * *Solution*: Exclude `location` from direct form columns (`form_columns`). Expose `latitude` and `longitude` float inputs using `wtforms.FloatField` and `@property` getters on `Venue` and `VenueStaging`. On form submit (`on_model_change`), parse `latitude` and `longitude` to automatically construct `WKTElement("POINT(lng lat)", srid=4326)`.

* **Fix Subscriber Edit 500 Error**:
  * *Root Cause*: SQLAdmin edit forms attempt to mutate read-only primary keys (`id`) or timezone-aware datetime defaults (`created_at`).
  * *Solution*: Define explicit `form_columns = ["whatsapp_number", "source"]` for `SubscriberAdmin`, eliminating form generation errors.

---

## 3. Implementation Plan & Phases

### Phase 1: Database Models & Migrations
1. Update SQLAlchemy ORM models in `backend/app/models/venues.py` and `backend/app/models/venue_staging.py`.
2. Generate and execute Alembic DB migration script to alter PostgreSQL table schemas.
3. Update `backend/app/seed.py` data fixtures.

### Phase 2: Pydantic Schemas & Ingestion CLI
1. Update `backend/app/schemas/venues.py` and `backend/app/schemas/venue_staging.py`.
2. Update `backend/app/api/v1/endpoints/venues.py` route handlers.
3. Update `backend/app/cli.py` enrichment and promotion commands.

### Phase 3: SQLAdmin Views
1. Refactor `backend/app/admin/views.py` with explicit `form_columns`, `form_extra_fields` (`latitude`, `longitude`), and `on_model_change` hooks.

### Phase 4: Admin TDD & Verification
1. Implement Pytest suite `backend/tests/test_admin.py` testing GET/POST list, view, create, and edit actions across all 7 views.
2. Update existing Pytest suites (`test_ingestion_pipeline.py`, `test_venue_ingest_schema.py`).
3. Run full test suite (`pytest backend/tests/`) to verify clean 100% pass rate.
