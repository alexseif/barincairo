# Task Checklist: Backend Entity & Admin Updates

**Plan File**: `ai-work/tasks/backend-entity-admin-updates-plan.md`  
**Target Branch**: `backend`  

- [x] **Git Setup**: Create and checkout new branch `backend` from `main`
- [x] **Task 1: Database Models, Lat/Lng Helpers, & Alembic Migration**
  - [x] Update ORM models in `backend/app/models/venues.py` (Category, VibeTag, Venue) and `venue_staging.py`
  - [x] Add `working_hours` attribute to `Venue` and `VenueStaging`
  - [x] Add `@property` lat/lng getters/setters on `Venue` and `VenueStaging`
  - [x] Generate and run Alembic migration (`alembic revision --autogenerate`, `alembic upgrade head`)
  - [x] Git Commit Task 1 changes
- [x] **Task 2: Pydantic Schemas, API Serialization, & Ingestion CLI**
  - [x] Update Pydantic schemas in `backend/app/schemas/venues.py`, `venue_staging.py`, `categories.py`, `vibe_tags.py`
  - [x] Update API routes & GeoJSON serializers in `backend/app/api/v1/endpoints/venues.py`
  - [x] Update `backend/app/cli.py` enrichment and promotion commands
  - [x] Update existing tests (`test_venue_ingest_schema.py`, `test_ingestion_pipeline.py`, `test_api.py`)
  - [x] Run existing Pytest suite to verify alignment
  - [x] Git Commit Task 2 changes
- [x] **Task 3: SQLAdmin Views & 500 Error Fixes**
  - [x] Refactor `backend/app/admin/views.py` to expose full CRUD for all 7 entities
  - [x] Fix PostGIS Geometry 500 error on `VenueAdmin` & `VenueStagingAdmin` using `scaffold_form` and `on_model_change`
  - [x] Fix `SubscriberAdmin` 500 error by setting explicit `form_columns = ["whatsapp_number", "source"]`
  - [x] Git Commit Task 3 changes
- [x] **Task 4: Admin TDD Pytest Suite & System Verification**
  - [x] Write `backend/tests/test_admin.py` testing GET/POST across all 7 views
  - [x] Run full Pytest suite (`pytest backend/tests/`)
  - [x] Verify clean test run with 100% pass rate
  - [x] Git Commit Task 4 changes
