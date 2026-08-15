import logging
from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from scripts.extract_gmaps_venues import extract_and_stage_venues

logger = logging.getLogger(__name__)

router = APIRouter()


class ScrapeRequest(BaseModel):
    location: str = Field("downtown", description="Target location or district name (e.g. heliopolis, downtown, maadi)")
    qty: int = Field(10, ge=1, le=50, description="Maximum number of new un-staged venues to extract")


class ScrapeResponse(BaseModel):
    status: str
    location: str
    requested_qty: int
    staged_count: int
    message: str


@router.post("/admin/scrape", response_model=ScrapeResponse, status_code=status.HTTP_200_OK)
async def trigger_admin_scrape(request_body: ScrapeRequest) -> ScrapeResponse:
    """Phase 1 Admin Trigger: Scrape and stage lightweight venues for a specified location/district."""
    try:
        records = await extract_and_stage_venues(location=request_body.location, qty=request_body.qty)
        staged_count = len(records)
        return ScrapeResponse(
            status="ok",
            location=request_body.location,
            requested_qty=request_body.qty,
            staged_count=staged_count,
            message=f"Successfully extracted and staged {staged_count} venue(s) into venue_staging for location '{request_body.location}'.",
        )
    except Exception as e:
        logger.error(f"Phase 1 Admin Scrape failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute Phase 1 extraction: {str(e)}",
        )
