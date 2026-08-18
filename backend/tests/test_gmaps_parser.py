import pytest
from app.core.gmaps_parser import parse_google_maps_url, slugify

def test_slugify():
    assert slugify("Cap D'Or - Bar") == "cap-dor-bar"
    assert slugify(" Café Riche (Downtown) ") == "cafe-riche-downtown"
    assert slugify("!!! Special @ Cairo ###") == "special-cairo"

@pytest.mark.asyncio
async def test_parse_google_maps_url_with_lat_lng():
    url = "https://www.google.com/maps/place/Cap+D'Or/@30.0456,31.2458,17z/data=!4m5!3m4!1s0x145840c6b123456:0x123456!8m2!3d30.0456!4d31.2458"
    result = await parse_google_maps_url(url)
    assert result["name"] == "Cap D'Or"
    assert result["slug"] == "cap-dor"
    assert result["latitude"] == 30.0456
    assert result["longitude"] == 31.2458
    assert result["address"] is not None

@pytest.mark.asyncio
async def test_parse_google_maps_url_place_id():
    url = "https://maps.google.com/?q=place_id:ChIJN1t_tDeuEmsRUsoyG83frY4"
    result = await parse_google_maps_url(url)
    assert result["place_id"] == "ChIJN1t_tDeuEmsRUsoyG83frY4"
    assert "name" in result
    assert "slug" in result

@pytest.mark.asyncio
async def test_parse_google_maps_url_invalid():
    with pytest.raises(ValueError):
        await parse_google_maps_url("")
