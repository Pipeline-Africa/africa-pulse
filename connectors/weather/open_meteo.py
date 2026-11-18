
from datetime import UTC, datetime
from typing import Any

import httpx
import pandas as pd
from pydantic import ValidationError

from connectors.weather.schemas import (
    OpenMeteoResponse,
    WeatherLocation,
)

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

HOURLY_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
]


class WeatherCollectorError(Exception):
    """Base exception for weather collection failures."""


class WeatherAPIError(WeatherCollectorError):
    """Raised when Open-Meteo returns an unsuccessful response."""


class WeatherResponseError(WeatherCollectorError):
    """Raised when the API response is invalid."""


class OpenMeteoCollector:
    def __init__(
        self,
        timeout: float = 30.0,
        client: httpx.AsyncClient | None = None,
    ):
        self.timeout = timeout
        self.client = client

    async def collect(
        self,
        location: WeatherLocation,
        forecast_days: int = 7,
    ) -> pd.DataFrame:
        if not 1 <= forecast_days <= 16:
            raise ValueError("forecast_days must be between 1 and 16")

        params = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "hourly": ",".join(HOURLY_VARIABLES),
            "forecast_days": forecast_days,
            "timezone": "auto",
        }

        response = await self._request(params)
        payload = self._validate_response(response)

        return self._to_dataframe(
            payload=payload,
            location=location,
        )

    async def _request(
        self,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        try:
            if self.client is not None:
                response = await self.client.get(
                    OPEN_METEO_URL,
                    params=params,
                )
            else:
                async with httpx.AsyncClient(
                    timeout=self.timeout
                ) as client:
                    response = await client.get(
                        OPEN_METEO_URL,
                        params=params,
                    )

            response.raise_for_status()

            return response.json()

        except httpx.TimeoutException as exc:
            raise WeatherAPIError(
                "Open-Meteo request timed out"
            ) from exc

        except httpx.HTTPStatusError as exc:
            raise WeatherAPIError(
                f"Open-Meteo returned HTTP {exc.response.status_code}"
            ) from exc

        except httpx.RequestError as exc:
            raise WeatherAPIError(
                f"Could not connect to Open-Meteo: {exc}"
            ) from exc

        except ValueError as exc:
            raise WeatherResponseError(
                "Open-Meteo returned invalid JSON"
            ) from exc

    @staticmethod
    def _validate_response(
        response: dict[str, Any],
    ) -> OpenMeteoResponse:
        if response.get("error"):
            raise WeatherResponseError(
                response.get("reason", "Open-Meteo API error")
            )

        try:
            return OpenMeteoResponse.model_validate(response)

        except ValidationError as exc:
            raise WeatherResponseError(
                f"Invalid Open-Meteo response: {exc}"
            ) from exc

    @staticmethod
    def _to_dataframe(
        payload: OpenMeteoResponse,
        location: WeatherLocation,
    ) -> pd.DataFrame:
        hourly = payload.hourly

        df = pd.DataFrame({
            "observed_at": hourly.time,
            "temperature_celsius": hourly.temperature_2m,
            "relative_humidity_pct": hourly.relative_humidity_2m,
            "precipitation_mm": hourly.precipitation,
            "wind_speed_kmh": hourly.wind_speed_10m,
        })

        fetched_at = datetime.now(UTC)

        df.insert(0, "location", location.name)
        df.insert(1, "latitude", location.latitude)
        df.insert(2, "longitude", location.longitude)
        df["source"] = "open-meteo"
        df["fetched_at"] = fetched_at

        df["observed_at"] = pd.to_datetime(
            df["observed_at"]
        )

        # Preserve source timezone and units for downstream consumers.
        df.attrs["source"] = "open-meteo"
        df.attrs["timezone"] = payload.timezone
        df.attrs["units"] = payload.hourly_units

        return df
