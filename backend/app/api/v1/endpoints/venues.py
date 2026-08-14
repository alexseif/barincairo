
from fastapi import APIRouter, Depends, HTTPException, Query, status
from geoalchemy2.functions import ST_X, ST_Y
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_async_session
from app.models.venues import Category, Venue, VibeTag
from app.schemas.venues import (
    CategoryResponse,
    GeoJSONFeature,
    GeoJSONFeatureCollection,
    GeoJSONGeometry,
    VenueProperties,
    VibeTagResponse,
)

router = APIRouter()


@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(
    session: AsyncSession = Depends(get_async_session),
) -> list[CategoryResponse]:
    result = await session.execute(select(Category).order_by(Category.name_en))
    categories = result.scalars().all()
    return [CategoryResponse.model_validate(c) for c in categories]


@router.get("/vibes", response_model=list[VibeTagResponse])
async def list_vibes(
    session: AsyncSession = Depends(get_async_session),
) -> list[VibeTagResponse]:
    result = await session.execute(select(VibeTag).order_by(VibeTag.name_en))
    vibes = result.scalars().all()
    return [VibeTagResponse.model_validate(v) for v in vibes]


@router.get("/venues", response_model=GeoJSONFeatureCollection)
async def list_venues_geojson(
    bbox: str | None = Query(None, description="min_lng,min_lat,max_lng,max_lat"),
    category: str | None = Query(None, description="Category slug filter"),
    price_range: str | None = Query(None, description="Price range filter e.g. $, $$, $$$"),
    vibe: str | None = Query(None, description="Vibe tag slug filter"),
    session: AsyncSession = Depends(get_async_session),
) -> GeoJSONFeatureCollection:
    stmt = (
        select(Venue, ST_X(Venue.location).label("lng"), ST_Y(Venue.location).label("lat"))
        .options(selectinload(Venue.category), selectinload(Venue.vibes))
        .where(Venue.is_active.is_(True))
    )

    if category:
        stmt = stmt.join(Venue.category).where(Category.slug == category)

    if price_range:
        stmt = stmt.where(Venue.price_range == price_range)

    if vibe:
        stmt = stmt.join(Venue.vibes).where(VibeTag.slug == vibe)

    result = await session.execute(stmt)
    rows = result.all()

    features: list[GeoJSONFeature] = []
    for venue, lng, lat in rows:
        vibe_slugs = [v.slug for v in venue.vibes]
        feature = GeoJSONFeature(
            type="Feature",
            geometry=GeoJSONGeometry(
                type="Point",
                coordinates=[float(lng), float(lat)],
            ),
            properties=VenueProperties(
                id=venue.id,
                slug=venue.slug,
                name_en=venue.name_en,
                name_ar=venue.name_ar,
                description_en=venue.description_en,
                description_ar=venue.description_ar,
                address_en=venue.address_en,
                address_ar=venue.address_ar,
                price_range=venue.price_range,
                vibe_description=venue.vibe_description,
                photo_url=venue.photo_url,
                category_slug=venue.category.slug,
                category_name=venue.category.name_en,
                vibes=vibe_slugs,
            ),
        )
        features.append(feature)

    return GeoJSONFeatureCollection(type="FeatureCollection", features=features)


@router.get("/venues/{slug}", response_model=GeoJSONFeature)
async def get_venue_detail(
    slug: str,
    session: AsyncSession = Depends(get_async_session),
) -> GeoJSONFeature:
    stmt = (
        select(Venue, ST_X(Venue.location).label("lng"), ST_Y(Venue.location).label("lat"))
        .options(selectinload(Venue.category), selectinload(Venue.vibes))
        .where(Venue.slug == slug, Venue.is_active.is_(True))
    )
    result = await session.execute(stmt)
    row = result.first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found")

    venue, lng, lat = row
    vibe_slugs = [v.slug for v in venue.vibes]

    return GeoJSONFeature(
        type="Feature",
        geometry=GeoJSONGeometry(
            type="Point",
            coordinates=[float(lng), float(lat)],
        ),
        properties=VenueProperties(
            id=venue.id,
            slug=venue.slug,
            name_en=venue.name_en,
            name_ar=venue.name_ar,
            description_en=venue.description_en,
            description_ar=venue.description_ar,
            address_en=venue.address_en,
            address_ar=venue.address_ar,
            price_range=venue.price_range,
            vibe_description=venue.vibe_description,
            photo_url=venue.photo_url,
            category_slug=venue.category.slug,
            category_name=venue.category.name_en,
            vibes=vibe_slugs,
        ),
    )
