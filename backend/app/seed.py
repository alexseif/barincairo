import asyncio

from geoalchemy2.elements import WKTElement
from sqlalchemy import select

from app.core.database import AsyncSessionLocal, engine
from app.models.venues import Base, Category, Venue, VibeTag

CATEGORIES_DATA = [
    {"slug": "historic-pub", "name": "Historic Pub"},
    {"slug": "rooftop-bar", "name": "Rooftop Bar"},
    {"slug": "bistro-lounge", "name": "Bistro Lounge"},
    {"slug": "cabaret-bar", "name": "Live Cabaret & Bar"},
    {"slug": "speakeasy", "name": "Speakeasy Backroom"},
    {"slug": "pub", "name": "Pub & Tavern"},
    {"slug": "lounge", "name": "Open Air Lounge"},
]

VIBES_DATA = [
    {"slug": "fancy", "name": "Fancy"},
    {"slug": "ambient-music", "name": "Ambient music"},
    {"slug": "live-performance", "name": "Live performance"},
    {"slug": "oud-player", "name": "Oud player"},
    {"slug": "old-times", "name": "Old times"},
    {"slug": "dancy", "name": "Dancy"},
    {"slug": "flirty", "name": "Flirty"},
]

VENUES_DATA = [
    {
        "slug": "cap-d-or-el-horeya",
        "category_slug": "historic-pub",
        "name": "Cap D'Or (El Horeya)",
        "description": "High-ceilinged 1930s Greek-Egyptian institution with original wooden bar, mirror panels, and cold Stella bottles.",
        "address": "12 El-Horeya Street (Falaki Square), Downtown Cairo",
        "lng": 31.2392,
        "lat": 30.0418,
        "price_range": "$",
        "working_hours": "5:00 PM - 3:00 AM",
        "vibe_description": "High ceilings, cold Stella, 1930s Greek-Egyptian atmosphere",
        "vibes": ["old-times", "ambient-music"],
    },
    {
        "slug": "estoril",
        "category_slug": "bistro-lounge",
        "name": "Estoril",
        "description": "Tucked away in a quiet alley passage off Talaat Harb; a historic haunt for Cairo artists, writers, and diplomats since 1957.",
        "address": "12 Talaat Harb Street (Passage), Downtown Cairo",
        "lng": 31.2385,
        "lat": 30.0435,
        "price_range": "$$",
        "working_hours": "12:00 PM - 12:00 AM",
        "vibe_description": "Artistic salon, quiet passage retreat, European-Egyptian bistro",
        "vibes": ["fancy", "old-times"],
    },
    {
        "slug": "odeon-palace-rooftop",
        "category_slug": "rooftop-bar",
        "name": "Odeon Palace Rooftop",
        "description": "24/7 rooftop lounge atop the historic Odeon Hotel, popular with filmmakers and night owls looking for open-air Cairo breeze.",
        "address": "6 Abdel Hamid Said Street (off Champollion), Downtown Cairo",
        "lng": 31.2405,
        "lat": 30.0468,
        "price_range": "$$",
        "working_hours": "24/7",
        "vibe_description": "24/7 open air rooftop, film scene hangout, night breeze",
        "vibes": ["flirty", "ambient-music"],
    },
    {
        "slug": "cafe-riche",
        "category_slug": "historic-pub",
        "name": "Café Riche",
        "description": "Founded in 1908, a landmark of Egyptian political and literary history where Naguib Mahfouz held weekly salon meetings.",
        "address": "29 Talaat Harb Street, Downtown Cairo",
        "lng": 31.2381,
        "lat": 30.0448,
        "price_range": "$$",
        "working_hours": "9:30 AM - 11:30 PM",
        "vibe_description": "Literary history, vintage photography, intellectual salon",
        "vibes": ["old-times", "ambient-music"],
    },
    {
        "slug": "shahrazad-nightclub",
        "category_slug": "cabaret-bar",
        "name": "Shahrazad Nightclub & Bar",
        "description": "Vintage 1950s cabaret hall with velvet drapes, brass lanterns, live oriental bands, and traditional Egyptian dance performances.",
        "address": "182 26th of July Street, Downtown Cairo",
        "lng": 31.2398,
        "lat": 30.0475,
        "price_range": "$$",
        "working_hours": "10:00 PM - 4:00 AM",
        "vibe_description": "Live oriental orchestra, velvet drapes, 1950s Cairo cabaret",
        "vibes": ["live-performance", "dancy", "oud-player"],
    },
    {
        "slug": "windsor-barrel-bar",
        "category_slug": "historic-pub",
        "name": "Windsor Hotel Barrel Bar",
        "description": "Former British Officers' Club with original wooden barrel seats, vintage telephone booths, and early 20th-century colonial decor.",
        "address": "19 Al-Alfi Street, Downtown Cairo",
        "lng": 31.2442,
        "lat": 30.0512,
        "price_range": "$$",
        "working_hours": "4:00 PM - 1:00 AM",
        "vibe_description": "Wooden barrel stools, antique telephone booth, nostalgia",
        "vibes": ["old-times", "ambient-music"],
    },
    {
        "slug": "greek-club",
        "category_slug": "bistro-lounge",
        "name": "Greek Club",
        "description": "High-ceilinged second-floor balcony overlooking Talaat Harb Square, serving classic Mediterranean dishes and cold spirits.",
        "address": "2 Champollion Street (Talaat Harb Square), Downtown Cairo",
        "lng": 31.2389,
        "lat": 30.0440,
        "price_range": "$$",
        "working_hours": "1:00 PM - 1:00 AM",
        "vibe_description": "High balcony view, Greek mezze, iconic square outlook",
        "vibes": ["fancy", "old-times"],
    },
    {
        "slug": "horus-rooftop",
        "category_slug": "rooftop-bar",
        "name": "Horus Rooftop",
        "description": "Open-air rooftop bar overlooking Adly Street and historic synagogue, featuring ambient beats and panoramic views of Downtown.",
        "address": "21 Adly Street, Downtown Cairo",
        "lng": 31.2388,
        "lat": 30.0461,
        "price_range": "$$",
        "working_hours": "5:00 PM - 2:00 AM",
        "vibe_description": "Synagogue outlook, breezy open terrace, relaxed vibe",
        "vibes": ["ambient-music", "flirty"],
    },
    {
        "slug": "lotus-rooftop",
        "category_slug": "rooftop-bar",
        "name": "Lotus Hotel Rooftop Bar",
        "description": "Laid-back bohemian rooftop bar atop the historic Lotus Hotel, popular among backpackers, expats, and local artists.",
        "address": "12 Talaat Harb Street, Downtown Cairo",
        "lng": 31.2396,
        "lat": 30.0452,
        "price_range": "$",
        "working_hours": "4:00 PM - 2:00 AM",
        "vibe_description": "Bohemian rooftop, relaxed crowd, casual Cairo night",
        "vibes": ["ambient-music", "old-times"],
    },
    {
        "slug": "carol-bar",
        "category_slug": "historic-pub",
        "name": "Carol Bar",
        "description": "Intimate, dimly lit mid-century cocktail lounge with leather booths, vintage mirrors, and classic jazz background tunes.",
        "address": "12 Kasr El Nil Street, Downtown Cairo",
        "lng": 31.2411,
        "lat": 30.0482,
        "price_range": "$$",
        "working_hours": "6:00 PM - 2:00 AM",
        "vibe_description": "Dim leather booths, classic jazz background, intimate lounge",
        "vibes": ["old-times", "fancy"],
    },
    {
        "slug": "bierkeller",
        "category_slug": "pub",
        "name": "Bierkeller",
        "description": "European-style basement tavern known for draft taps, hearty pub snacks, and lively evening gatherings.",
        "address": "6 Shawarby Street, Downtown Cairo",
        "lng": 31.2401,
        "lat": 30.0439,
        "price_range": "$$",
        "working_hours": "5:00 PM - 1:00 AM",
        "vibe_description": "Basement tavern, draft beer, social gatherings",
        "vibes": ["ambient-music", "dancy"],
    },
    {
        "slug": "al-alfi-lounge",
        "category_slug": "lounge",
        "name": "Al-Alfi Lounge",
        "description": "Pedestrian promenade lounge with outdoor seating, live Oud performances, and traditional mezze.",
        "address": "24 Al-Alfi Pedestrian Promenade, Downtown Cairo",
        "lng": 31.2438,
        "lat": 30.0508,
        "price_range": "$$",
        "working_hours": "4:00 PM - 1:00 AM",
        "vibe_description": "Outdoor promenade, live Oud music, oriental snacks",
        "vibes": ["live-performance", "oud-player"],
    },
    {
        "slug": "champollion-backroom",
        "category_slug": "speakeasy",
        "name": "Champollion Backroom",
        "description": "Discreet backroom speakeasy behind a historic Downtown storefront serving craft signature cocktails.",
        "address": "15 Champollion Street, Downtown Cairo",
        "lng": 31.2395,
        "lat": 30.0442,
        "price_range": "$$$",
        "working_hours": "7:00 PM - 3:00 AM",
        "vibe_description": "Speakeasy entrance, craft cocktails, exclusive mood",
        "vibes": ["fancy", "flirty"],
    },
    {
        "slug": "sherazade-rooftop",
        "category_slug": "rooftop-bar",
        "name": "Sherazade Rooftop",
        "description": "High-rise rooftop extension of the Shahrazad complex with nighttime views of the Cairo Tower and Nile skyline.",
        "address": "182 26th of July Street (Top Floor), Downtown Cairo",
        "lng": 31.2402,
        "lat": 30.0478,
        "price_range": "$$",
        "working_hours": "6:00 PM - 3:00 AM",
        "vibe_description": "Nile skyline view, Cairo tower lookout, open roof",
        "vibes": ["dancy", "ambient-music"],
    },
    {
        "slug": "grand-hotel-bar",
        "category_slug": "historic-pub",
        "name": "Grand Hotel Bar",
        "description": "Authentic 1940s Downtown pub with stained glass windows, brass fixtures, and traditional hospitality.",
        "address": "17 26th of July Street, Downtown Cairo",
        "lng": 31.2420,
        "lat": 30.0491,
        "price_range": "$",
        "working_hours": "5:00 PM - 1:00 AM",
        "vibe_description": "1940s stained glass, brass counter, traditional Downtown host",
        "vibes": ["old-times", "ambient-music"],
    },
]


async def seed_data() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Seed Categories
        category_map = {}
        for cat in CATEGORIES_DATA:
            res = await session.execute(select(Category).where(Category.slug == cat["slug"]))
            existing_cat = res.scalar_one_or_none()
            if not existing_cat:
                new_cat = Category(slug=cat["slug"], name=cat["name"])
                session.add(new_cat)
                await session.flush()
                category_map[cat["slug"]] = new_cat.id
            else:
                existing_cat.name = cat["name"]
                category_map[cat["slug"]] = existing_cat.id

        # Seed Vibes
        vibe_map = {}
        for vibe in VIBES_DATA:
            res = await session.execute(select(VibeTag).where(VibeTag.slug == vibe["slug"]))
            existing_vibe = res.scalar_one_or_none()
            if not existing_vibe:
                new_vibe = VibeTag(slug=vibe["slug"], name=vibe["name"])
                session.add(new_vibe)
                await session.flush()
                vibe_map[vibe["slug"]] = new_vibe
            else:
                existing_vibe.name = vibe["name"]
                vibe_map[vibe["slug"]] = existing_vibe

        # Seed Venues
        for v in VENUES_DATA:
            res = await session.execute(select(Venue).where(Venue.slug == v["slug"]))
            existing_venue = res.scalar_one_or_none()
            wkt_location = WKTElement(f"POINT({v['lng']} {v['lat']})", srid=4326)

            if not existing_venue:
                venue_obj = Venue(
                    category_id=category_map[v["category_slug"]],
                    slug=v["slug"],
                    name=v["name"],
                    description=v["description"],
                    address=v["address"],
                    location=wkt_location,
                    price_range=v["price_range"],
                    working_hours=v["working_hours"],
                    vibe_description=v["vibe_description"],
                    is_active=True,
                )
                for vibe_slug in v["vibes"]:
                    if vibe_slug in vibe_map:
                        venue_obj.vibes.append(vibe_map[vibe_slug])
                session.add(venue_obj)
            else:
                existing_venue.name = v["name"]
                existing_venue.description = v["description"]
                existing_venue.address = v["address"]
                existing_venue.working_hours = v["working_hours"]

        await session.commit()
        print("✅ Seed completed successfully: 7 Categories, 7 Vibes, 15 Venues populated.")


if __name__ == "__main__":
    asyncio.run(seed_data())
