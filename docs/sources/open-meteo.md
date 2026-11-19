# Open-Meteo

## Summary

Open-Meteo is an open-source weather API that provides weather forecasts and historical weather data for any location, free for non-commercial use and with no API key required. It is the likely first source for Africa Pulse because it covers African cities and can be used without registration.

Source: [Open-Meteo documentation](https://open-meteo.com/en/docs); "Non-Commercial Use" section of the [Terms & Privacy page](https://open-meteo.com/en/terms); "Open-Meteo is open-source" section of the [Licence page](https://open-meteo.com/en/licence); all checked 2026-10-23.

## Owner

Open-Meteo is run by OpenMeteo GmbH, a company based in Bürglen, Switzerland. The CEO is Patrick Zippenfenig. The terms are governed by Swiss law.

Source: "Open-Meteo is operated by" section of the [Terms & Privacy page](https://open-meteo.com/en/terms), checked 2026-10-23.

## Documentation

- Main documentation URL: https://open-meteo.com/en/docs
- API reference URL: each API has its own page, e.g. [Forecast](https://open-meteo.com/en/docs), [Historical Weather](https://open-meteo.com/en/docs/historical-weather-api), [Historical Forecast](https://open-meteo.com/en/docs/historical-forecast-api)
- Terms of use URL: https://open-meteo.com/en/terms

## Domain

Weather.

## Access method

REST API over HTTPS, returning JSON. No scraping needed. Each API (forecast, historical weather, historical forecast) has its own base URL, and you pick the location with `latitude` and `longitude` parameters.

Source: [Open-Meteo documentation](https://open-meteo.com/en/docs); my own requests on 2026-10-23.

## Authentication

None for the free API: no key, no sign-up. I made all my test requests without any credentials. Commercial use requires a paid subscription (API Standard, Professional or Enterprise), billed through Stripe and tied to an account.

Source: [Terms & Privacy page](https://open-meteo.com/en/terms), checked 2026-10-23; my own requests on 2026-10-23.

## Geographic coverage

All of Africa is covered. The forecast comes from global models run by national weather services (ECMWF, NOAA, DWD and others), and every historical dataset is listed as "Global". I tested Lagos (forecast) and Nairobi (historical), and both returned full hourly data.

Locations are given as `latitude` and `longitude`. There are no city names or station IDs. The API snaps to the nearest grid cell, so the coordinates you get back differ slightly from the ones you sent: Lagos `6.52, 3.38` came back as `6.5026364, 3.397651`. Each response also gives the grid cell's elevation (10 m for Lagos, 1668 m for Nairobi).

There is a separate Geocoding API, based on GeoNames, that turns place names into coordinates. I didn't test it, since the connector will use fixed coordinates.

The docs list models from many national weather services, including Norway, Canada, Australia, China and several European countries, but none from an African weather service. So African cities are covered by global models rather than models built for the region.

Source: "Data Sources" table of the [Historical Weather API documentation](https://open-meteo.com/en/docs/historical-weather-api); model list on the [Forecast API documentation](https://open-meteo.com/en/docs); "Data Sources" section of the [Licence page](https://open-meteo.com/en/licence); my own requests on 2026-10-23.

## Update frequency

It depends on which dataset you use. For historical data, ECMWF IFS updates every 6 hours with no delay, while ERA5 and ERA5-Land update daily with a 5-day delay. Forecast models each run on their own schedule. The docs point to a separate model updates page for exact timings, which I haven't recorded here.

In practice, recent days should come from the Forecast API (using `past_days`), and anything older than about a week can come from the Historical Weather API.

Source: "Data Sources" table of the [Historical Weather API documentation](https://open-meteo.com/en/docs/historical-weather-api), checked 2026-10-23.

## Historical availability

Open-Meteo has three separate APIs, and it's easy to mix them up:

| API | Base URL | What it gives you | Modelled or observed? |
|---|---|---|---|
| Forecast | `api.open-meteo.com/v1/forecast` | Forecast for 7 days by default (up to 16), plus up to 92 past days with `past_days` | Modelled |
| Historical Weather | `archive-api.open-meteo.com/v1/archive` | Reanalysis from ERA5 (0.25°, from 1940), ERA5-Land (0.1°, from 1950) and ECMWF IFS (9 km, from 2017) | Modelled (reanalysis) |
| Historical Forecast | `historical-forecast-api.open-meteo.com/v1/forecast` | Archived forecasts from around 2022 onwards, using the same models, parameters and response format as the Forecast API. The first few hours of each model run are stitched into one continuous hourly series | Modelled |

The docs also list a Single Runs API and a Previous Model Runs API, both for studying forecast model output rather than actual weather. They're out of scope for now.

None of them are station observations. Reanalysis is the closest thing to "what really happened": the docs say it combines weather station, aircraft, buoy, radar and satellite observations with models to fill the gaps. But the output is still a model grid, not a thermometer reading. Historical Forecast answers a different question: what did we expect to happen? That's useful for checking forecast accuracy, but it shouldn't be treated as actual weather.

History comes through the same kind of REST request as the forecast, just with a different base URL plus `start_date` and `end_date`. I tested it for Nairobi on 2024-01-01 and got 24 hourly values, in UTC by default, for a grid point at 1668 m elevation.

ERA5 and ERA5-Land update daily with a 5-day delay, while the ECMWF IFS dataset (from 2017) updates every 6 hours with no delay. By default, data from 2017 onwards comes from the newer 9 km models. The docs advise selecting only ERA5 or ERA5-Land for studies over several decades, because mixing models can introduce changes that aren't real weather changes.

Source: info box and "Data sources" table of the [Historical Weather API documentation](https://open-meteo.com/en/docs/historical-weather-api); [Forecast API documentation](https://open-meteo.com/en/docs) (`past_days`, `forecast_days`); [Historical Forecast API documentation](https://open-meteo.com/en/docs/historical-forecast-api); my own request on 2026-10-23.

## Identifiers

There are no record IDs or station IDs. A single value is identified by the grid cell's latitude and longitude, the timestamp, and the variable name.

These aren't fully stable. The grid cell returned depends on which model is used, and by default the Historical Weather API switches to newer 9 km models from 2017 onwards. So the same request coordinates could map to slightly different grid points for different periods. The connector should store both the coordinates we requested and the ones returned.

Source: my own requests on 2026-10-23 (Lagos and Nairobi grid snapping); "Data Sources" section of the [Historical Weather API documentation](https://open-meteo.com/en/docs/historical-weather-api).

## Timestamp semantics

Timestamps come back in UTC by default. Adding `timezone=auto` (or a name like `Africa/Lagos`) switches them to local time.

The tricky part is that the timestamps don't include an offset. They look like `2026-10-23T01:00` either way. When I ran the same Lagos request both ways, the time strings were identical, but the values had shifted by an hour: 27.8 °C sat at `00:00` in UTC and at `01:00` in Lagos time. The only way to tell which time zone a response uses is the `utc_offset_seconds` field (0 for UTC, 3600 for Lagos). The connector should always request UTC to avoid mistakes.

Most values, like temperature, are a snapshot at the given hour. Some, like precipitation, cover the hour before it, as a sum or an average, so precipitation at `01:00` is the total from 00:00 to 01:00. Daily values follow the requested time zone's day. Real 15-minute data is only available in Central Europe and North America. For African cities the API fills 15-minute requests by interpolating hourly data, so Africa Pulse should treat hourly as the true resolution.

Source: "Hourly Parameter Definition" table and "15-Minutely Weather Variables" note in the [Open-Meteo Forecast API documentation](https://open-meteo.com/en/docs); my own requests on 2026-10-23.

## Units

All units below are the defaults. Every response also includes an `hourly_units` (or `daily_units`) block that states the unit for each field, so the connector can check it rather than assume.

| Field | Unit | Valid time |
|---|---|---|
| `temperature_2m`, `dew_point_2m`, `apparent_temperature` | °C (°F optional) | Instant |
| `relative_humidity_2m` | % | Instant |
| `pressure_msl`, `surface_pressure` | hPa | Instant |
| `cloud_cover` (and `_low`, `_mid`, `_high`) | % | Instant |
| `wind_speed_10m` | km/h (mph, m/s or knots optional) | Instant |
| `wind_direction_10m` | ° | Instant |
| `precipitation` | mm (inch optional) | Preceding hour sum |
| `vapour_pressure_deficit` | kPa | Instant |

Units can be switched per request, but for consistency we should stick to the defaults. My Lagos request returned exactly these defaults: `"temperature_2m":"°C"`, `"precipitation":"mm"`, `"wind_speed_10m":"km/h"`.

Source: "Hourly Parameter Definition" table in the [Open-Meteo Forecast API documentation](https://open-meteo.com/en/docs); my own request on 2026-10-23.

## Rate limits

| | Free | API Standard | API Professional | API Enterprise |
|---|---|---|---|---|
| Commercial use | No | Yes | Yes | Yes |
| Per minute | 600 | Unlimited | Unlimited | Unlimited |
| Per hour | 5,000 | Unlimited | Unlimited | Unlimited |
| Per day | 10,000 | Unlimited | Unlimited | Unlimited |
| Per month | 300,000 | 1M | 5M | >50M |

Limits are applied per IP address and application. The terms warn that apps hosted on shared platforms like Vercel, Netlify or Render may hit the limit sooner than expected. Open-Meteo also reserves the right to block apps or IPs that misuse the service, without notice.

Source: "Non-Commercial Use" section and plan comparison table of the [Terms & Privacy page](https://open-meteo.com/en/terms), checked 2026-10-23.

## Terms of use

- License: "Attribution 4.0 International (CC BY 4.0)" for the API data. The Open-Meteo source code is separately licensed under GNU AGPLv3, which doesn't affect our use of the data.

- Commercial use permitted? Not on the free API. The terms define commercial use as apps or sites with subscriptions or ads, commercial products, or undisclosed research at commercial companies. Non-commercial examples include non-profit sites without ads, public research and educational content. Commercial use needs a paid plan.

- Storage permitted? Yes. The licence says we are free to "copy and redistribute the material in any medium or format", provided we give attribution.

Open question for maintainers: whether Africa Pulse counts as non-commercial. If it has no ads, subscriptions or paid features, it appears to fit the non-commercial examples, but this should be confirmed before we rely on the free tier.

The terms can change at any time, and changes are tracked on GitHub, so this entry should be rechecked before the connector goes live.

Source: "Non-Commercial Use" and "API Subscription" sections of the [Terms & Privacy page](https://open-meteo.com/en/terms); "Licence" section of the [Licence page](https://open-meteo.com/en/licence); both checked 2026-10-23.

## Attribution requirements

Wherever Open-Meteo data is displayed, we must include a link next to it. The licence page gives this example:

```html
<a href="https://open-meteo.com/">Weather data by Open-Meteo.com</a>
```

CC BY 4.0 also requires a link to the licence and a note if we changed the data, for example by converting units or aggregating to daily values.

Open-Meteo builds on open data from national weather services (DWD, ECMWF, NOAA, Météo-France and others). The licence page lists each one with its own licence, so we should credit them too where practical.

Source: "Licence" and "Data Sources" sections of the [Licence page](https://open-meteo.com/en/licence), checked 2026-10-23.

## Redistribution restrictions

Yes, Africa Pulse may redistribute both raw and derived data. CC BY 4.0 allows sharing and adapting the data in any format, as long as we give attribution, link to the licence and say if we changed anything.

Two caveats:
- The licence covers the data, not the free API service. Redistributing data we fetched is fine, but if Africa Pulse itself becomes commercial, the free API can no longer be used to fetch it.
- UK Met Office data is under CC-BY-SA (share-alike), so anything built from it must be shared under the same licence. If the connector ever pulls UK Met Office models, this needs to be checked first.

Source: "Licence" and "Data Sources" sections of the [Licence page](https://open-meteo.com/en/licence); [Terms & Privacy page](https://open-meteo.com/en/terms); both checked 2026-10-23.

## Known limitations

- **Modelled, not measured.** Every API returns model output. None of it is a direct station reading.
- **Coarse resolution in Africa.** Only global models (roughly 9–25 km) cover Africa, so values can differ from conditions in a specific neighbourhood, especially near coasts and mountains.
- **Grid snapping.** Returned coordinates and elevation are for the grid cell, not the exact point requested.
- **Time zones.** Timestamps carry no offset, and daylight saving changes are ignored within a request (relevant to Egypt and Morocco).
- **15-minute data is interpolated** for Africa, not real.
- **Mixed models over time.** Historical data switches models in 2017, which can create artificial jumps in long-term trends unless ERA5 or ERA5-Land is selected explicitly.
- **No guarantees.** The terms say the data is provided without warranty and that uninterrupted access isn't guaranteed. On the free tier, apps or IPs can be blocked without notice.

Source: [Terms & Privacy page](https://open-meteo.com/en/terms); [Forecast API documentation](https://open-meteo.com/en/docs); [Historical Weather API documentation](https://open-meteo.com/en/docs/historical-weather-api); all checked 2026-10-23.

## Sample request and response

Request made on 2026-10-23 for Lagos (forecast API, default settings):

```text
https://api.open-meteo.com/v1/forecast?latitude=6.52&longitude=3.38&hourly=temperature_2m,precipitation,wind_speed_10m&forecast_days=1
```

Response, trimmed to the first three hours (the full response has 24 hourly values):

```json
{
  "latitude": 6.5026364,
  "longitude": 3.397651,
  "utc_offset_seconds": 0,
  "timezone": "GMT",
  "timezone_abbreviation": "GMT",
  "elevation": 10.0,
  "hourly_units": {
    "time": "iso8601",
    "temperature_2m": "°C",
    "precipitation": "mm",
    "wind_speed_10m": "km/h"
  },
  "hourly": {
    "time": ["2026-10-23T00:00", "2026-10-23T01:00", "2026-10-23T02:00"],
    "temperature_2m": [27.8, 27.6, 27.4],
    "precipitation": [0.00, 0.00, 0.00],
    "wind_speed_10m": [7.3, 6.2, 6.8]
  }
}
```

[Weather data by Open-Meteo.com](https://open-meteo.com/), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Trimmed from the original response. Included here because the licence permits redistribution with attribution.

Source: request made by the researcher on 2026-10-23.

## Assessment

A good fit for a first connector. It covers every African city we'd want, needs no key, returns clean and consistent JSON across its forecast and historical APIs, and its data licence (CC BY 4.0) lets us store and redistribute what we fetch.

The main risks:
- **Commercial status.** The free API is non-commercial only. If Africa Pulse ever adds ads, subscriptions or paid features, we'd need a paid plan. Maintainers should confirm our status now.
- **Rate limits.** 10,000 calls a day is plenty for a few cities, but limits apply per IP, so shared hosting could hit them early.
- **Data quality.** Everything is modelled at global resolution, so it's best for city-level trends, not precise local readings. If we need observed data later, we'll need a second source.
- **Changing terms.** The terms can change at any time, so this entry should be rechecked before the connector goes live.

## Researched by

@Rilexx90, checked 2026-10-23.
