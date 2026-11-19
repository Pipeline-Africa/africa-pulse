
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, model_validator


class WeatherLocation(BaseModel):
    name: str = Field(min_length=1)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class HourlyWeather(BaseModel):
    time: list[datetime]
    temperature_2m: list[float | None]
    relative_humidity_2m: list[float | None]
    precipitation: list[float | None]
    wind_speed_10m: list[float | None]

    @model_validator(mode="after")
    def validate_array_lengths(self):
        lengths = {
            len(getattr(self, field))
            for field in (
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "wind_speed_10m",
            )
        }

        if len(lengths) != 1:
            raise ValueError(
                "Hourly weather measurements must have equal lengths"
            )

        if len(self.time) != next(iter(lengths)):
            raise ValueError(
                "Hourly timestamps and measurements must have equal lengths"
            )

        if len(set(self.time)) != len(self.time):
            raise ValueError("Duplicate hourly timestamps received")

        return self


class OpenMeteoResponse(BaseModel):
    latitude: float
    longitude: float
    timezone: str
    timezone_abbreviation: str | None = None
    hourly_units: dict[str, str]
    hourly: HourlyWeather


class WeatherCollection(BaseModel):
    location: WeatherLocation
    source: str = "open-meteo"
    fetched_at: datetime
    measurements: list[dict[str, Any]]
    units: dict[str, str]
