import asyncio
from geoalchemy2.elements import WKTElement
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal, engine
from app.models.venues import Base, Category, Venue, VibeTag

CATEGORIES_DATA = [
    {"slug": "historic-pub", "name_en": "Historic Pub", "name_ar": "بار كلاسيكي تاريخي"},
    {"slug": "rooftop-bar", "name_en": "Rooftop Bar", "name_ar": "سطح / روف بار"},
    {"slug": "bistro-lounge", "name_en": "Bistro Lounge", "name_ar": "بيسترو ولاونج"},
    {"slug": "cabaret-bar", "name_en": "Live Cabaret & Bar", "name_ar": "كاباريه ومسرح حقيقي"},
    {"slug": "speakeasy", "name_en": "Speakeasy Backroom", "name_ar": "بار سري (سبيك إيزي)"},
    {"slug": "pub", "name_en": "Pub & Tavern", "name_ar": "حانة وبار شبيهاً بالنادي"},
    {"slug": "lounge", "name_en": "Open Air Lounge", "name_ar": "لاونج مفتوح"},
]

VIBES_DATA = [
    {"slug": "fancy", "name_en": "Fancy", "name_ar": "فاخر"},
    {"slug": "ambient-music", "name_en": "Ambient music", "name_ar": "موسيقى هادئة"},
    {"slug": "live-performance", "name_en": "Live performance", "name_ar": "عروض حية"},
    {"slug": "oud-player", "name_en": "Oud player", "name_ar": "عازف عود"},
    {"slug": "old-times", "name_en": "Old times", "name_ar": "زمن جميل"},
    {"slug": "dancy", "name_en": "Dancy", "name_ar": "صاخب ورقص"},
    {"slug": "flirty", "name_en": "Flirty", "name_ar": "رومانسي ودافئ"},
]

VENUES_DATA = [
    {
        "slug": "cap-d-or-el-horeya",
        "category_slug": "historic-pub",
        "name_en": "Cap D'Or (El Horeya / الحرية)",
        "name_ar": "بار الحرية (كاب دور)",
        "description_en": "High-ceilinged 1930s Greek-Egyptian institution with original wooden bar, mirror panels, and cold Stella bottles.",
        "description_ar": "بار ومقهى كلاسيكي تاريخي يعود إلى الثلاثينيات، يتميز بأسقفه العالية وأجوائه الشعبية الفريدة.",
        "address_en": "12 El-Horeya Street (Falaki Square), Downtown Cairo",
        "address_ar": "١٢ شارع الحرية (ميدان الفلكي)، وسط البلد",
        "lng": 31.2392,
        "lat": 30.0418,
        "price_range": "$",
        "vibe_description": "High ceilings, cold Stella, 1930s Greek-Egyptian atmosphere",
        "vibes": ["old-times", "ambient-music"],
    },
    {
        "slug": "estoril",
        "category_slug": "bistro-lounge",
        "name_en": "Estoril (إستوريل)",
        "name_ar": "مطعم وبار إستوريل",
        "description_en": "Tucked away in a quiet alley passage off Talaat Harb; a historic haunt for Cairo artists, writers, and diplomats since 1957.",
        "description_ar": "ملتقى الفنانين والمثقفين منذ عام ١٩٥٧، يختبئ في ممر هادئ متفرع من شارع طلعت حرب.",
        "address_en": "12 Talaat Harb Street (Passage), Downtown Cairo",
        "address_ar": "١٢ شارع طلعت حرب (ممر إستوريل)، وسط البلد",
        "lng": 31.2385,
        "lat": 30.0435,
        "price_range": "$$",
        "vibe_description": "Artistic salon, quiet passage retreat, European-Egyptian bistro",
        "vibes": ["fancy", "old-times"],
    },
    {
        "slug": "odeon-palace-rooftop",
        "category_slug": "rooftop-bar",
        "name_en": "Odeon Palace Rooftop (سطح أوديون)",
        "name_ar": "روف بار فندق أوديون",
        "description_en": "24/7 rooftop lounge atop the historic Odeon Hotel, popular with filmmakers and night owls looking for open-air Cairo breeze.",
        "description_ar": "روف كلاسيكي يطل على سماء وسط البلد، مفتوح على مدار الساعة ويعتبر وجهة مفضلة للمخرجين وعشاق السهر.",
        "address_en": "6 Abdel Hamid Said Street (off Champollion), Downtown Cairo",
        "address_ar": "٦ شارع عبد الحميد سعيد (متفرع من شامبليون)، وسط البلد",
        "lng": 31.2405,
        "lat": 30.0468,
        "price_range": "$$",
        "vibe_description": "24/7 open air rooftop, film scene hangout, night breeze",
        "vibes": ["flirty", "ambient-music"],
    },
    {
        "slug": "cafe-riche",
        "category_slug": "historic-pub",
        "name_en": "Café Riche (كافيه ريش)",
        "name_ar": "كافيه ومقهى ريش",
        "description_en": "Founded in 1908, a landmark of Egyptian political and literary history where Naguib Mahfouz held weekly salon meetings.",
        "description_ar": "صرح ثقافي وتاريخي أسس عام ١٩٠٨، شهد اجتماعات نجيب محفوظ وثوار ١٩١٩.",
        "address_en": "29 Talaat Harb Street, Downtown Cairo",
        "address_ar": "٢٩ شارع طلعت حرب، وسط البلد",
        "lng": 31.2381,
        "lat": 30.0448,
        "price_range": "$$",
        "vibe_description": "Literary history, vintage photography, intellectual salon",
        "vibes": ["old-times", "ambient-music"],
    },
    {
        "slug": "shahrazad-nightclub",
        "category_slug": "cabaret-bar",
        "name_en": "Shahrazad Nightclub & Bar (شهرزاد)",
        "name_ar": "ملهى وبار شهرزاد",
        "description_en": "Vintage 1950s cabaret hall with velvet drapes, brass lanterns, live oriental bands, and traditional Egyptian dance performances.",
        "description_ar": "ملهى وبار شرقي كلاسيكي بتصميم الخمسينيات، يقدم عروضاً موسيقية حية وأجواء طربية.",
        "address_en": "182 26th of July Street, Downtown Cairo",
        "address_ar": "١٨٢ شارع ٢٦ يوليو، وسط البلد",
        "lng": 31.2398,
        "lat": 30.0475,
        "price_range": "$$",
        "vibe_description": "Live oriental orchestra, velvet drapes, 1950s Cairo cabaret",
        "vibes": ["live-performance", "dancy", "oud-player"],
    },
    {
        "slug": "windsor-barrel-bar",
        "category_slug": "historic-pub",
        "name_en": "Windsor Hotel Barrel Bar (بار ويندسور)",
        "name_ar": "بار فندق ويندسور التاريخي",
        "description_en": "Former British Officers' Club with original wooden barrel seats, vintage telephone booths, and early 20th-century colonial decor.",
        "description_ar": "نادٍ كلاسيكي عريق يتألق بمقاعده الخشبية الأنتيك وأجوائه التاريخية من أوائل القرن العشرين.",
        "address_en": "19 Al-Alfi Street, Downtown Cairo",
        "address_ar": "١٩ شارع الألفي، وسط البلد",
        "lng": 31.2442,
        "lat": 30.0512,
        "price_range": "$$",
        "vibe_description": "Wooden barrel stools, antique telephone booth, nostalgia",
        "vibes": ["old-times", "ambient-music"],
    },
    {
        "slug": "greek-club",
        "category_slug": "bistro-lounge",
        "name_en": "Greek Club (النادي اليوناني)",
        "name_ar": "النادي اليوناني",
        "description_en": "High-ceilinged second-floor balcony overlooking Talaat Harb Square, serving classic Mediterranean dishes and cold spirits.",
        "description_ar": "إطلالة ساحرة من الطابق الثاني على ميدان طلعت حرب، يجمع بين المطبخ اليوناني والمشروبات الكلاسيكية.",
        "address_en": "2 Champollion Street (Talaat Harb Square), Downtown Cairo",
        "address_ar": "٢ شارع شامبليون (ميدان طلعت حرب)، وسط البلد",
        "lng": 31.2389,
        "lat": 30.0440,
        "price_range": "$$",
        "vibe_description": "High balcony view, Greek mezze, iconic square outlook",
        "vibes": ["fancy", "old-times"],
    },
    {
        "slug": "horus-rooftop",
        "category_slug": "rooftop-bar",
        "name_en": "Horus Rooftop (سطح حورس)",
        "name_ar": "روف بار حورس",
        "description_en": "Open-air rooftop bar overlooking Adly Street and historic synagogue, featuring ambient beats and panoramic views of Downtown.",
        "description_ar": "روف مفتوح في الهواء الطلق يقدم إطلالة بنورامية على معالم شارع عدلي ومباني وسط البلد المعمارية.",
        "address_en": "21 Adly Street, Downtown Cairo",
        "address_ar": "٢١ شارع عدلي، وسط البلد",
        "lng": 31.2388,
        "lat": 30.0461,
        "price_range": "$$",
        "vibe_description": "Synagogue outlook, breezy open terrace, relaxed vibe",
        "vibes": ["ambient-music", "flirty"],
    },
    {
        "slug": "lotus-rooftop",
        "category_slug": "rooftop-bar",
        "name_en": "Lotus Hotel Rooftop Bar (لوتس روف)",
        "name_ar": "سطح فندق لوتس",
        "description_en": "Laid-back bohemian rooftop bar atop the historic Lotus Hotel, popular among backpackers, expats, and local artists.",
        "description_ar": "روف هادئ ذو طابع بوهيمي كلاسيكي يرحب بزوار وسط البلد والفنانين المستقلين.",
        "address_en": "12 Talaat Harb Street, Downtown Cairo",
        "address_ar": "١٢ شارع طلعت حرب، وسط البلد",
        "lng": 31.2396,
        "lat": 30.0452,
        "price_range": "$",
        "vibe_description": "Bohemian rooftop, relaxed crowd, casual Cairo night",
        "vibes": ["ambient-music", "old-times"],
    },
    {
        "slug": "carol-bar",
        "category_slug": "historic-pub",
        "name_en": "Carol Bar (بار كارول)",
        "name_ar": "بار كارول",
        "description_en": "Intimate, dimly lit mid-century cocktail lounge with leather booths, vintage mirrors, and classic jazz background tunes.",
        "description_ar": "بار كلاسيكي دافئ بتصميم منتصف القرن العشرين، يتميز بمقاعده الجلدية وموسيقاه الهادئة.",
        "address_en": "12 Kasr El Nil Street, Downtown Cairo",
        "address_ar": "١٢ شارع قصر النيل، وسط البلد",
        "lng": 31.2411,
        "lat": 30.0482,
        "price_range": "$$",
        "vibe_description": "Dim leather booths, classic jazz background, intimate lounge",
        "vibes": ["old-times", "fancy"],
    },
    {
        "slug": "bierkeller",
        "category_slug": "pub",
        "name_en": "Bierkeller (بيركيلر)",
        "name_ar": "بار وبيركيلر",
        "description_en": "European-style basement tavern known for draft taps, hearty pub snacks, and lively evening gatherings.",
        "description_ar": "حانة بدروم بالطراز الأوروبي توفر أجواء دافئة لللقاءات الشبابية ومشروبات الشعير الطازجة.",
        "address_en": "6 Shawarby Street, Downtown Cairo",
        "address_ar": "٦ شارع الشواربي، وسط البلد",
        "lng": 31.2401,
        "lat": 30.0439,
        "price_range": "$$",
        "vibe_description": "Basement tavern, draft beer, social gatherings",
        "vibes": ["ambient-music", "dancy"],
    },
    {
        "slug": "al-alfi-lounge",
        "category_slug": "lounge",
        "name_en": "Al-Alfi Lounge (لاونج الألفي)",
        "name_ar": "لاونج ممشى الألفي",
        "description_en": "Pedestrian promenade lounge with outdoor seating, live Oud performances, and traditional mezze.",
        "description_ar": "لاونج بإطلالة على ممشى الألفي المخصص للمشاة، يقدم عروض عود حية والمقبلات الشرقي.",
        "address_en": "24 Al-Alfi Pedestrian Promenade, Downtown Cairo",
        "address_ar": "٢٤ ممشى الألفي للمشاة، وسط البلد",
        "lng": 31.2438,
        "lat": 30.0508,
        "price_range": "$$",
        "vibe_description": "Outdoor promenade, live Oud music, oriental snacks",
        "vibes": ["live-performance", "oud-player"],
    },
    {
        "slug": "champollion-backroom",
        "category_slug": "speakeasy",
        "name_en": "Champollion Backroom (غرفة شامبليون)",
        "name_ar": "غرفة شامبليون السرية",
        "description_en": "Discreet backroom speakeasy behind a historic Downtown storefront serving craft signature cocktails.",
        "description_ar": "بار سري خلف واجهة تاريخية في شارع شامبليون يقدم كوكتيلات مبتكرة وأجواء خاصة.",
        "address_en": "15 Champollion Street, Downtown Cairo",
        "address_ar": "١٥ شارع شامبليون، وسط البلد",
        "lng": 31.2395,
        "lat": 30.0442,
        "price_range": "$$$",
        "vibe_description": "Speakeasy entrance, craft cocktails, exclusive mood",
        "vibes": ["fancy", "flirty"],
    },
    {
        "slug": "sherazade-rooftop",
        "category_slug": "rooftop-bar",
        "name_en": "Sherazade Rooftop (سطح شهرزاد)",
        "name_ar": "روف بار شهرزاد",
        "description_en": "High-rise rooftop extension of the Shahrazad complex with nighttime views of the Cairo Tower and Nile skyline.",
        "description_ar": "امتداد علوي يجمع بين الإطلالة الساحرة برج القاهرة وشوارع وسط البلد التاريخية.",
        "address_en": "182 26th of July Street (Top Floor), Downtown Cairo",
        "address_ar": "١٨٢ شارع ٢٦ يوليو (الطابق العلوي)، وسط البلد",
        "lng": 31.2402,
        "lat": 30.0478,
        "price_range": "$$",
        "vibe_description": "Nile skyline view, Cairo tower lookout, open roof",
        "vibes": ["dancy", "ambient-music"],
    },
    {
        "slug": "grand-hotel-bar",
        "category_slug": "historic-pub",
        "name_en": "Grand Hotel Bar (بار الفندق الكبير)",
        "name_ar": "بار الجراند أوتيل",
        "description_en": "Authentic 1940s Downtown pub with stained glass windows, brass fixtures, and traditional hospitality.",
        "description_ar": "بار كلاسيكي قديم يعود إلى الأربعينيات بزجاج ملون وديكورات نحاسية أصيلة.",
        "address_en": "17 26th of July Street, Downtown Cairo",
        "address_ar": "١٧ شارع ٢٦ يوليو، وسط البلد",
        "lng": 31.2420,
        "lat": 30.0491,
        "price_range": "$",
        "vibe_description": "1940s stained glass, brass counter, traditional Downtown host",
        "vibes": ["old-times", "ambient-music"],
    },
]


async function seed_data() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Seed Categories
        category_map = {}
        for cat in CATEGORIES_DATA:
            res = await session.execute(select(Category).where(Category.slug == cat["slug"]))
            existing_cat = res.scalar_one_or_none()
            if not existing_cat:
                new_cat = Category(slug=cat["slug"], name_en=cat["name_en"], name_ar=cat["name_ar"])
                session.add(new_cat)
                await session.flush()
                category_map[cat["slug"]] = new_cat.id
            else:
                category_map[cat["slug"]] = existing_cat.id

        # Seed Vibes
        vibe_map = {}
        for vibe in VIBES_DATA:
            res = await session.execute(select(VibeTag).where(VibeTag.slug == vibe["slug"]))
            existing_vibe = res.scalar_one_or_none()
            if not existing_vibe:
                new_vibe = VibeTag(slug=vibe["slug"], name_en=vibe["name_en"], name_ar=vibe["name_ar"])
                session.add(new_vibe)
                await session.flush()
                vibe_map[vibe["slug"]] = new_vibe
            else:
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
                    name_en=v["name_en"],
                    name_ar=v["name_ar"],
                    description_en=v["description_en"],
                    description_ar=v["description_ar"],
                    address_en=v["address_en"],
                    address_ar=v["address_ar"],
                    location=wkt_location,
                    price_range=v["price_range"],
                    vibe_description=v["vibe_description"],
                    is_active=True,
                )
                for vibe_slug in v["vibes"]:
                    if vibe_slug in vibe_map:
                        venue_obj.vibes.append(vibe_map[vibe_slug])
                session.add(venue_obj)

        await session.commit()
        print("✅ Seed completed successfully: 7 Categories, 7 Vibes, 15 Venues populated.")


if __name__ == "__main__":
    asyncio.run(seed_data())
