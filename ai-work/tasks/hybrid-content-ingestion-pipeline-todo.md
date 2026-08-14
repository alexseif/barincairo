# Task List: Hybrid Content Ingestion Pipeline

- [x] **Task 1: Database Staging Model & Alembic Migration (`SEC-1.2`)**
  - Create `VenueStaging` model in `backend/app/models/venue_staging.py`
  - Add `google_maps_url` column to `Venue` model in `backend/app/models/venues.py`
  - Expose `VenueStaging` in `backend/app/models/__init__.py`
  - Generate and apply Alembic migration `0003_create_venue_staging_and_google_maps_url.py`
  - Verification: `alembic check` and DB table reflection check

- [x] **Task 2: Ingestion Validation Schemas (`VenueIngestSchema`)**
  - Create `VenueIngestSchema` in `backend/app/schemas/venue_staging.py`
  - Enforce 2-citation verification gate (`citations: list[str] = Field(..., min_length=2)`)
  - Enforce Downtown Cairo WGS84 bounding box constraints (`30.0380-30.0520°N`, `31.2300-31.2480°E`)
  - Verification: Unit test `VenueIngestSchema` validation with sample payloads

- [x] **Task 3: Phase 1 Extraction Script (`extract_gmaps_venues.py`)**
  - Create `backend/scripts/extract_gmaps_venues.py` with `--bbox` argument parsing
  - Extract place metadata, direct `google_maps_url`, candidate photo pool, and top user reviews
  - Synthesize `what_people_say` review summary in `raw_payload`
  - Implement spatial deduplication by `place_id` and PostGIS `ST_DWithin`
  - Verification: Execute `extract_gmaps_venues.py` in test/dry-run mode and inspect `venue_staging`

- [x] **Task 4: CLI Operations (`enrich-staged` & `promote-staged`)**
  - Add `enrich-staged` subcommand in `backend/app/cli.py` (select main hero photo, Arabic copy, 2-citation gate check, status transition)
  - Add `promote-staged` subcommand in `backend/app/cli.py` (validate via `VenueIngestSchema`, populate `venues` and `venue_photos`, mark status `PROMOTED`)
  - Verification: Test CLI subcommands on sample staging records

- [x] **Task 5: SQLAdmin Integration (`VenueStagingAdmin`)**
  - Register `VenueStagingAdmin` view in `backend/app/admin/views.py`
  - Verification: Inspect SQLAdmin model view registration

- [x] **Task 6: Test Suite & End-to-End Verification**
  - Create `backend/tests/test_ingestion_pipeline.py` testing bounding box checks, 2-citation gate, photo selection, deduplication, and full promotion flow
  - Verification: Run `pytest backend/tests/test_ingestion_pipeline.py`, `ruff check backend`, `mypy backend/app`
