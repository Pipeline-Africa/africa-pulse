

import httpx
import pandas as pd
import pytest

from connectors.weather.open_meteo import (
    OpenMeteoCollector,
    WeatherAPIError,
    WeatherResponseError,
)
from connectors.weather.schemas import WeatherLocation


@pytest.fixture
def location():
    return WeatherLocation(
        name="Lagos",
        latitude=6.5244,
        longitude=3.3792,
    )


@pytest.fixture
def api_response():
    return {
        "latitude": 6.5,
        "longitude": 3.4,
        "timezone": "Africa/Lagos",
        "timezone_abbreviation": "WAT",
        "hourly_units": {
            "time": "iso8601",
            "temperature_2m": "°C",
            "relative_humidity_2m": "%",
            "precipitation": "mm",
            "wind_speed_10m": "km/h",
        },
        "hourly": {
            "time": [
                "2026-11-18T00:00",
                "2026-11-18T01:00",
            ],
            "temperature_2m": [27.1, 26.8],
            "relative_humidity_2m": [85, 87],
            "precipitation": [0.0, 0.2],
            "wind_speed_10m": [12.4, 10.8],
        },
    }


@pytest.mark.asyncio
async def test_collect_returns_dataframe(
    location,
    api_response,
):
    async def handler(request):
        return httpx.Response(
            200,
            json=api_response,
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(
        transport=transport
    ) as client:
        collector = OpenMeteoCollector(client=client)

        result = await collector.collect(location)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2

    assert result.iloc[0]["location"] == "Lagos"
    assert result.iloc[0]["temperature_celsius"] == 27.1

    assert result.iloc[0]["source"] == "open-meteo"
    assert result["fetched_at"].notna().all()


@pytest.mark.asyncio
async def test_collect_preserves_missing_values(
    location,
    api_response,
):
    api_response["hourly"]["precipitation"] = [
        None,
        0.2,
    ]

    async def handler(request):
        return httpx.Response(200, json=api_response)

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler)
    ) as client:
        collector = OpenMeteoCollector(client=client)
        result = await collector.collect(location)

    assert pd.isna(result.iloc[0]["precipitation_mm"])


@pytest.mark.asyncio
async def test_collect_rejects_invalid_response(
    location,
):
    async def handler(request):
        return httpx.Response(
            200,
            json={"unexpected": "response"},
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler)
    ) as client:
        collector = OpenMeteoCollector(client=client)

        with pytest.raises(WeatherResponseError):
            await collector.collect(location)


@pytest.mark.asyncio
async def test_collect_handles_http_error(location):
    async def handler(request):
        return httpx.Response(
            503,
            json={"error": True},
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler)
    ) as client:
        collector = OpenMeteoCollector(client=client)

        with pytest.raises(WeatherAPIError):
            await collector.collect(location)


@pytest.mark.asyncio
async def test_collect_rejects_invalid_forecast_days(location):
    collector = OpenMeteoCollector()

    with pytest.raises(ValueError):
        await collector.collect(
            location,
            forecast_days=30,
        )


def test_dataframe_has_expected_columns(
    location,
    api_response,
):
    payload = OpenMeteoCollector._validate_response(
        api_response
    )

    result = OpenMeteoCollector._to_dataframe(
        payload,
        location,
    )

    expected = {
        "location",
        "latitude",
        "longitude",
        "observed_at",
        "temperature_celsius",
        "relative_humidity_pct",
        "precipitation_mm",
        "wind_speed_kmh",
        "source",
        "fetched_at",
    }

    assert expected.issubset(result.columns)
    assert result.attrs["timezone"] == "Africa/Lagos"
