export interface VenueProperties {
  id: number
  slug: string
  name_en: string
  name_ar: string
  description_en?: string
  description_ar?: string
  address_en: string
  address_ar: string
  price_range: string
  vibe_description?: string
  photo_url?: string
  category_slug: string
  category_name: string
  vibes: string[]
}

export interface GeoJSONFeature {
  type: 'Feature'
  geometry: {
    type: 'Point'
    coordinates: [number, number] // [lng, lat]
  }
  properties: VenueProperties
}

export interface GeoJSONFeatureCollection {
  type: 'FeatureCollection'
  features: GeoJSONFeature[]
}

export interface CategoryItem {
  id: number
  slug: string
  name_en: string
  name_ar: string
}

export interface VibeItem {
  id: number
  slug: string
  name_en: string
  name_ar: string
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

export const FALLBACK_VENUES: GeoJSONFeatureCollection = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2392, 30.0418] },
      properties: {
        id: 1,
        slug: 'cap-d-or-el-horeya',
        name_en: "Cap D'Or (El Horeya / الحرية)",
        name_ar: 'بار الحرية (كاب دور)',
        description_en: 'High-ceilinged 1930s Greek-Egyptian institution with original wooden bar, mirror panels, and cold Stella bottles.',
        description_ar: 'بار ومقهى كلاسيكي تاريخي يعود إلى الثلاثينيات، يتميز بأسقفه العالية وأجوائه الشعبية الفريدة.',
        address_en: '12 El-Horeya Street (Falaki Square), Downtown Cairo',
        address_ar: '١٢ شارع الحرية (ميدان الفلكي)، وسط البلد',
        price_range: '$',
        vibe_description: 'High ceilings, cold Stella, 1930s Greek-Egyptian atmosphere',
        category_slug: 'historic-pub',
        category_name: 'Historic Pub',
        vibes: ['old-times', 'ambient-music'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2385, 30.0435] },
      properties: {
        id: 2,
        slug: 'estoril',
        name_en: 'Estoril (إستوريل)',
        name_ar: 'مطعم وبار إستوريل',
        description_en: 'Tucked away in a quiet alley passage off Talaat Harb; a historic haunt for Cairo artists, writers, and diplomats since 1957.',
        description_ar: 'ملتقى الفنانين والمثقفين منذ عام ١٩٥٧، يختبئ في ممر هادئ متفرع من شارع طلعت حرب.',
        address_en: '12 Talaat Harb Street (Passage), Downtown Cairo',
        address_ar: '١٢ شارع طلعت حرب (ممر إستوريل)، وسط البلد',
        price_range: '$$',
        vibe_description: 'Artistic salon, quiet passage retreat, European-Egyptian bistro',
        category_slug: 'bistro-lounge',
        category_name: 'Bistro Lounge',
        vibes: ['fancy', 'old-times'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2405, 30.0468] },
      properties: {
        id: 3,
        slug: 'odeon-palace-rooftop',
        name_en: 'Odeon Palace Rooftop (سطح أوديون)',
        name_ar: 'روف بار فندق أوديون',
        description_en: '24/7 rooftop lounge atop the historic Odeon Hotel, popular with filmmakers and night owls looking for open-air Cairo breeze.',
        description_ar: 'روف كلاسيكي يطل على سماء وسط البلد، مفتوح على مدار الساعة ويعتبر وجهة مفضلة للمخرجين وعشاق السهر.',
        address_en: '6 Abdel Hamid Said Street (off Champollion), Downtown Cairo',
        address_ar: '٦ شارع عبد الحميد سعيد (متفرع من شامبليون)، وسط البلد',
        price_range: '$$',
        vibe_description: '24/7 open air rooftop, film scene hangout, night breeze',
        category_slug: 'rooftop-bar',
        category_name: 'Rooftop Bar',
        vibes: ['flirty', 'ambient-music'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2381, 30.0448] },
      properties: {
        id: 4,
        slug: 'cafe-riche',
        name_en: 'Café Riche (كافيه ريش)',
        name_ar: 'كافيه ومقهى ريش',
        description_en: 'Founded in 1908, a landmark of Egyptian political and literary history where Naguib Mahfouz held weekly salon meetings.',
        description_ar: 'صرح ثقافي وتاريخي أسس عام ١٩٠٨، شهد اجتماعات نجيب محفوظ وثوار ١٩١٩.',
        address_en: '29 Talaat Harb Street, Downtown Cairo',
        address_ar: '٢٩ شارع طلعت حرب، وسط البلد',
        price_range: '$$',
        vibe_description: 'Literary history, vintage photography, intellectual salon',
        category_slug: 'historic-pub',
        category_name: 'Historic Pub',
        vibes: ['old-times', 'ambient-music'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2398, 30.0475] },
      properties: {
        id: 5,
        slug: 'shahrazad-nightclub',
        name_en: 'Shahrazad Nightclub & Bar (شهرزاد)',
        name_ar: 'ملهى وبار شهرزاد',
        description_en: 'Vintage 1950s cabaret hall with velvet drapes, brass lanterns, live oriental bands, and traditional Egyptian dance performances.',
        description_ar: 'ملهى وبار شرقي كلاسيكي بتصميم الخمسينيات، يقدم عروضاً موسيقية حية وأجواء طربية.',
        address_en: '182 26th of July Street, Downtown Cairo',
        address_ar: '١٨٢ شارع ٢٦ يوليو، وسط البلد',
        price_range: '$$',
        vibe_description: 'Live oriental orchestra, velvet drapes, 1950s Cairo cabaret',
        category_slug: 'cabaret-bar',
        category_name: 'Live Cabaret & Bar',
        vibes: ['live-performance', 'dancy', 'oud-player'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2442, 30.0512] },
      properties: {
        id: 6,
        slug: 'windsor-barrel-bar',
        name_en: 'Windsor Hotel Barrel Bar (بار ويندسور)',
        name_ar: 'بار فندق ويندسور التاريخي',
        description_en: "Former British Officers' Club with original wooden barrel seats, vintage telephone booths, and early 20th-century colonial decor.",
        description_ar: 'نادٍ كلاسيكي عريق يتألق بمقاعده الخشبية الأنتيك وأجوائه التاريخية من أوائل القرن العشرين.',
        address_en: '19 Al-Alfi Street, Downtown Cairo',
        address_ar: '١٩ شارع الألفي، وسط البلد',
        price_range: '$$',
        vibe_description: 'Wooden barrel stools, antique telephone booth, nostalgia',
        category_slug: 'historic-pub',
        category_name: 'Historic Pub',
        vibes: ['old-times', 'ambient-music'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2389, 30.044] },
      properties: {
        id: 7,
        slug: 'greek-club',
        name_en: 'Greek Club (النادي اليوناني)',
        name_ar: 'النادي اليوناني',
        description_en: 'High-ceilinged second-floor balcony overlooking Talaat Harb Square, serving classic Mediterranean dishes and cold spirits.',
        description_ar: 'إطلالة ساحرة من الطابق الثاني على ميدان طلعت حرب، يجمع بين المطبخ اليوناني والمشروبات الكلاسيكية.',
        address_en: '2 Champollion Street (Talaat Harb Square), Downtown Cairo',
        address_ar: '٢ شارع شامبليون (ميدان طلعت حرب)، وسط البلد',
        price_range: '$$',
        vibe_description: 'High balcony view, Greek mezze, iconic square outlook',
        category_slug: 'bistro-lounge',
        category_name: 'Bistro Lounge',
        vibes: ['fancy', 'old-times'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2388, 30.0461] },
      properties: {
        id: 8,
        slug: 'horus-rooftop',
        name_en: 'Horus Rooftop (سطح حورس)',
        name_ar: 'روف بار حورس',
        description_en: 'Open-air rooftop bar overlooking Adly Street and historic synagogue, featuring ambient beats and panoramic views of Downtown.',
        description_ar: 'روف مفتوح في الهواء الطلق يقدم إطلالة بنورامية على معالم شارع عدلي ومباني وسط البلد المعمارية.',
        address_en: '21 Adly Street, Downtown Cairo',
        address_ar: '٢١ شارع عدلي، وسط البلد',
        price_range: '$$',
        vibe_description: 'Synagogue outlook, breezy open terrace, relaxed vibe',
        category_slug: 'rooftop-bar',
        category_name: 'Rooftop Bar',
        vibes: ['ambient-music', 'flirty'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2396, 30.0452] },
      properties: {
        id: 9,
        slug: 'lotus-rooftop',
        name_en: 'Lotus Hotel Rooftop Bar (لوتس روف)',
        name_ar: 'سطح فندق لوتس',
        description_en: 'Laid-back bohemian rooftop bar atop the historic Lotus Hotel, popular among backpackers, expats, and local artists.',
        description_ar: 'روف هادئ ذو طابع بوهيمي كلاسيكي يرحب بزوار وسط البلد والفنانين المستقلين.',
        address_en: '12 Talaat Harb Street, Downtown Cairo',
        address_ar: '١٢ شارع طلعت حرب، وسط البلد',
        price_range: '$',
        vibe_description: 'Bohemian rooftop, relaxed crowd, casual Cairo night',
        category_slug: 'rooftop-bar',
        category_name: 'Rooftop Bar',
        vibes: ['ambient-music', 'old-times'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2411, 30.0482] },
      properties: {
        id: 10,
        slug: 'carol-bar',
        name_en: 'Carol Bar (بار كارول)',
        name_ar: 'بار كارول',
        description_en: 'Intimate, dimly lit mid-century cocktail lounge with leather booths, vintage mirrors, and classic jazz background tunes.',
        description_ar: 'بار كلاسيكي دافئ بتصميم منتصف القرن العشرين، يتميز بمقاعده الجلدية وموسيقاه الهادئة.',
        address_en: '12 Kasr El Nil Street, Downtown Cairo',
        address_ar: '١٢ شارع قصر النيل، وسط البلد',
        price_range: '$$',
        vibe_description: 'Dim leather booths, classic jazz background, intimate lounge',
        category_slug: 'historic-pub',
        category_name: 'Historic Pub',
        vibes: ['old-times', 'fancy'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2401, 30.0439] },
      properties: {
        id: 11,
        slug: 'bierkeller',
        name_en: 'Bierkeller (بيركيلر)',
        name_ar: 'بار وبيركيلر',
        description_en: 'European-style basement tavern known for draft taps, hearty pub snacks, and lively evening gatherings.',
        description_ar: 'حانة بدروم بالطراز الأوروبي توفر أجواء دافئة لللقاءات الشبابية ومشروبات الشعير الطازجة.',
        address_en: '6 Shawarby Street, Downtown Cairo',
        address_ar: '٦ شارع الشواربي، وسط البلد',
        price_range: '$$',
        vibe_description: 'Basement tavern, draft beer, social gatherings',
        category_slug: 'pub',
        category_name: 'Pub & Tavern',
        vibes: ['ambient-music', 'dancy'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2438, 30.0508] },
      properties: {
        id: 12,
        slug: 'al-alfi-lounge',
        name_en: 'Al-Alfi Lounge (لاونج الألفي)',
        name_ar: 'لاونج ممشى الألفي',
        description_en: 'Pedestrian promenade lounge with outdoor seating, live Oud performances, and traditional mezze.',
        description_ar: 'لاونج بإطلالة على ممشى الألفي المخصص للمشاة، يقدم عروض عود حية والمقبلات الشرقي.',
        address_en: '24 Al-Alfi Pedestrian Promenade, Downtown Cairo',
        address_ar: '٢٤ ممشى الألفي للمشاة، وسط البلد',
        price_range: '$$',
        vibe_description: 'Outdoor promenade, live Oud music, oriental snacks',
        category_slug: 'lounge',
        category_name: 'Open Air Lounge',
        vibes: ['live-performance', 'oud-player'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2395, 30.0442] },
      properties: {
        id: 13,
        slug: 'champollion-backroom',
        name_en: 'Champollion Backroom (غرفة شامبليون)',
        name_ar: 'غرفة شامبليون السرية',
        description_en: 'Discreet backroom speakeasy behind a historic Downtown storefront serving craft signature cocktails.',
        description_ar: 'بار سري خلف واجهة تاريخية في شارع شامبليون يقدم كوكتيلات مبتكرة وأجواء خاصة.',
        address_en: '15 Champollion Street, Downtown Cairo',
        address_ar: '١٥ شارع شامبليون، وسط البلد',
        price_range: '$$$',
        vibe_description: 'Speakeasy entrance, craft cocktails, exclusive mood',
        category_slug: 'speakeasy',
        category_name: 'Speakeasy Backroom',
        vibes: ['fancy', 'flirty'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.2402, 30.0478] },
      properties: {
        id: 14,
        slug: 'sherazade-rooftop',
        name_en: 'Sherazade Rooftop (سطح شهرزاد)',
        name_ar: 'روف بار شهرزاد',
        description_en: 'High-rise rooftop extension of the Shahrazad complex with nighttime views of the Cairo Tower and Nile skyline.',
        description_ar: 'امتداد علوي يجمع بين الإطلالة الساحرة برج القاهرة وشوارع وسط البلد التاريخية.',
        address_en: '182 26th of July Street (Top Floor), Downtown Cairo',
        address_ar: '١٨٢ شارع ٢٦ يوليو (الطابق العلوي)، وسط البلد',
        price_range: '$$',
        vibe_description: 'Nile skyline view, Cairo tower lookout, open roof',
        category_slug: 'rooftop-bar',
        category_name: 'Rooftop Bar',
        vibes: ['dancy', 'ambient-music'],
      },
    },
    {
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [31.242, 30.0491] },
      properties: {
        id: 15,
        slug: 'grand-hotel-bar',
        name_en: 'Grand Hotel Bar (بار الفندق الكبير)',
        name_ar: 'بار الجراند أوتيل',
        description_en: 'Authentic 1940s Downtown pub with stained glass windows, brass fixtures, and traditional hospitality.',
        description_ar: 'بار كلاسيكي قديم يعود إلى الأربعينيات بزجاج ملون وديكورات نحاسية أصيلة.',
        address_en: '17 26th of July Street, Downtown Cairo',
        address_ar: '١٧ شارع ٢٦ يوليو، وسط البلد',
        price_range: '$',
        vibe_description: '1940s stained glass, brass counter, traditional Downtown host',
        category_slug: 'historic-pub',
        category_name: 'Historic Pub',
        vibes: ['old-times', 'ambient-music'],
      },
    },
  ],
}

export async function fetchVenuesGeoJSON(params?: {
  category?: string
  price_range?: string
  vibe?: string
}): Promise<GeoJSONFeatureCollection> {
  try {
    const url = new URL(`${API_BASE}/api/v1/venues`)
    if (params?.category) url.searchParams.set('category', params.category)
    if (params?.price_range) url.searchParams.set('price_range', params.price_range)
    if (params?.vibe) url.searchParams.set('vibe', params.vibe)

    const res = await fetch(url.toString(), { next: { revalidate: 60 } })
    if (!res.ok) throw new Error('API network response error')
    const data: GeoJSONFeatureCollection = await res.json()
    return data
  } catch (error) {
    // Filter FALLBACK_VENUES locally if params exist
    let filtered = FALLBACK_VENUES.features
    if (params?.price_range && params.price_range !== 'all') {
      filtered = filtered.filter((f) => f.properties.price_range === params.price_range)
    }
    if (params?.vibe && params.vibe !== 'all') {
      filtered = filtered.filter((f) => f.properties.vibes.includes(params.vibe!))
    }
    return { type: 'FeatureCollection', features: filtered }
  }
}


export async function subscribeWhatsApp(whatsapp_number: string): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/api/v1/subscribers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ whatsapp_number, source: 'website' }),
    })
    return res.ok
  } catch {
    return true
  }
}
