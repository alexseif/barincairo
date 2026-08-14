# Task Checklist: Backend Entity & Admin Updates

**Plan File**: `ai-work/tasks/backend-entity-admin-updates-plan.md`  
**Target Branch**: `backend`  

- [ ] **Git Setup**: Create and checkout new branch `backend` from `main`
- [ ] **Task 1: Database Models, Lat/Lng Helpers, & Alembic Migration**
  - [ ] Update ORM models in `backend/app/models/venues.py` (Category, VibeTag, Venue) and `venue_staging.py`
  - [ ] Add `working_hours` attribute to `Venue` and `VenueStaging`
  - [ ] Add `@property` lat/lng getters/setters on `Venue` and `VenueStaging`
  - [ ] Generate and run Alembic migration (`alembic revision --autogenerate`, `alembic upgrade head`)
  - [ ] Git Commit Task 1 changes
- [ ] **Task 2: Pydantic Schemas, API Serialization, & Ingestion CLI**
  - [ ] Update Pydantic schemas in `backend/app/schemas/venues.py`, `venue_staging.py`, `categories.py`, `vibe_tags.py`
  - [ ] Update API routes & GeoJSON serializers in `backend/app/api/v1/endpoints/venues.py`
  - [ ] Update `backend/app/cli.py` enrichment and promotion commands
  - [ ] Update existing tests (`test_venue_ingest_schema.py`, `test_ingestion_pipeline.py`, `test_api.py`)
  - [ ] Run existing Pytest suite to verify alignment
  - [ ] Git Commit Task 2 changes
- [ ] **Task 3: SQLAdmin Views & 500 Error Fixes**
  - [ ] Refactor `backend/app/admin/views.py` to expose full CRUD for all 7 entities
  - [ ] Fix PostGIS Geometry 500 error on `VenueAdmin` & `VenueStagingAdmin` using `form_extra_fields` and `on_model_change`
  - [ ] Fix `SubscriberAdmin` 500 error by setting explicit `form_columns = ["whatsapp_number", "source"]`
  - [ ] Git Commit Task 3 changes
- [ ] **Task 4: Admin TDD Pytest Suite & System Verification**
  - [ ] Write `backend/tests/test_admin.py` testing GET/POST across all 7 views
  - [ ] Run full Pytest suite (`pytest backend/tests/`)
  - [ ] Verify clean test run with 100% pass rate
  - [ ] Git Commit Task 4 changes
