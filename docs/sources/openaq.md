# OpenAQ

> Documentation, terms and data policy checked on 2026-11-01. Station, unit and sample data in this entry come from live requests to the OpenAQ API v3, made on the query date stated under "Researched by".

## Summary

OpenAQ aggregates ground-level air-quality measurements from government reference monitors, research networks and low-cost sensor networks, harmonises them into one format and serves them through a REST API and an AWS S3 archive ([About](https://docs.openaq.org/about/about), [FAQ](https://docs.openaq.org/about/faq)). For Africa Pulse it is the most direct single route to air-quality observations across several African cities, with license metadata attached to each location.

## Owner

OpenAQ, a nonprofit organisation founded in the U.S. ([About](https://docs.openaq.org/about/about)). OpenAQ does not own the measurements: "OpenAQ asserts no intellectual property interest over the data it publishes" and "The data publisher will retain copyright to its data" ([Data Policy](https://docs.openaq.org/docs/data-policy)). Each location carries its own `owner` and `provider` objects ([Locations](https://docs.openaq.org/resources/locations)).

## Documentation

- Main documentation URL: https://docs.openaq.org/
- API reference URL: https://docs.openaq.org/api
- Terms of use URL: https://docs.openaq.org/about/terms
- Data policy URL: https://docs.openaq.org/docs/data-policy
- Licenses resource: https://docs.openaq.org/resources/licenses
- S3 archive guide: https://docs.openaq.org/docs/accessing-openaq-archive-data

## Domain

Air quality

## Access method

- REST API v3, all endpoints `GET`, base `https://api.openaq.org/v3` ([API reference](https://docs.openaq.org/api), [API key](https://docs.openaq.org/using-the-api/api-key)). Main resources: `/locations`, `/locations/{id}/sensors`, `/locations/{id}/latest`, `/sensors/{id}/measurements`, hourly/daily/yearly aggregates under `/sensors/{id}/hours`, `/days`, `/years`, plus `/parameters`, `/licenses`, `/providers`, `/owners`, `/instruments`, `/countries` ([API reference](https://docs.openaq.org/api)).
- API v1 and v2 "were retired in January 2025 and are no longer available"; requests to them return HTTP 410 ([Gone](https://docs.openaq.org/errors/gone)).
- Bulk history: public S3 bucket `openaq-data-archive` in `us-east-1`, gzipped CSV partitioned as `records/csv.gz/locationid=<id>/year=<yyyy>/month=<mm>/location-<id>-<yyyymmdd>.csv.gz`, readable anonymously with `--no-sign-request` ([Archive guide](https://docs.openaq.org/docs/accessing-openaq-archive-data), [AWS Open Data Registry](https://registry.opendata.aws/openaq/)).
- Official Python client: https://python.openaq.org/

## Authentication

- API key, sent in the `X-API-Key` header of every request ([API key](https://docs.openaq.org/using-the-api/api-key)).
- Registration is required: sign up at https://explore.openaq.org/register; the key is managed and rotated at https://explore.openaq.org/account ([API key](https://docs.openaq.org/using-the-api/api-key)).
- Free tier exists: 60 requests per minute and 2,000 per hour ([Rate limits](https://docs.openaq.org/using-the-api/rate-limits)).
- "An individual is permitted to register for only one API key" and "Unauthorized use of your API key, including transfer to another user, is prohibited" ([Terms of use](https://docs.openaq.org/about/terms)).
- S3 archive needs no credentials ([Archive guide](https://docs.openaq.org/docs/accessing-openaq-archive-data)).

## Geographic coverage

- Global, but OpenAQ "only ingests openly-licensed data" that has concentration values, coordinates and datetimes, and only "stationary, ground-level data", no satellite or airborne data ([FAQ](https://docs.openaq.org/about/faq)). African coverage depends on which local networks publish openly, so it is uneven.
- Location filters on `/v3/locations`: `coordinates` (WGS84 latitude,longitude) with `radius` in metres, 1 to 25,000; or `bbox` (minX,minY,maxX,maxY, max 4 decimal places); or `iso` (ISO 3166-1 alpha-2) or `countries_id`; plus `providers_id`, `monitor` (true = reference monitor, false = air sensor) and `mobile` ([Python client, locations](https://python.openaq.org/resources/locations/)). There is no city-name filter; `locality` is a descriptive field on the location, not a query key ([Locations](https://docs.openaq.org/resources/locations)).

### Coverage of the five target cities

Generated from `GET /v3/locations?coordinates=<lat>,<lon>&radius=25000&limit=1000` ([Locations](https://docs.openaq.org/resources/locations)) on 2026-11-02 19:49 UTC. Search centres: Lagos 6.5244,3.3792; Nairobi -1.2864,36.8172; Cairo 30.0444,31.2357; Johannesburg -26.2041,28.0473; Kinshasa -4.4419,15.2663. Radius 25 km, the API maximum. "Type" is from `isMonitor`: Reference monitor when true, Air sensor when false. "Status" is Active if `datetimeLast` is within 30 days of the query time. Station names, owners and providers are OpenAQ metadata, reproduced as identifiers only.

| City | Locations within 25 km | Active | Reference monitors | Air sensors | Locations in whole country (`iso`) | Most recent report (UTC) |
|---|---|---|---|---|---|---|
| Lagos | 67 | 41 | 1 | 66 | >1 (NG) | 2026-11-02 19:30 |
| Nairobi | 16 | 2 | 9 | 7 | >1 (KE) | 2026-11-02 19:00 |
| Cairo | 1 | 0 | 1 | 0 | >1 (EG) | 2025-03-04 12:00 |
| Johannesburg | 12 | 4 | 10 | 2 | >1 (ZA) | 2026-11-02 19:00 |
| Kinshasa | 14 | 9 | 1 | 13 | >1 (CD) | 2026-11-02 19:00 |

#### Lagos

| Location ID | Name | Type | Provider | Owner | Instrument | Parameters | First report (UTC) | Last report (UTC) | Observed lag | Status | Distance |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [6446050](https://explore.openaq.org/locations/6446050) | Alaba Blueline Train Station | Air sensor | HabitatMap | HabitatMap | HabitatMap Sensor | pm25 (µg/m³) | 2026-07-15 | 2026-11-02 19:30 | 18 min | Active | 9.1 km |
| [6446048](https://explore.openaq.org/locations/6446048) | Omole Estate | Air sensor | HabitatMap | HabitatMap | HabitatMap Sensor | pm25 (µg/m³) | 2026-07-15 | 2026-11-02 19:29 | 19 min | Active | 12.4 km |
| [6446047](https://explore.openaq.org/locations/6446047) | Oyingbo Redline Train Station | Air sensor | HabitatMap | HabitatMap | HabitatMap Sensor | pm25 (µg/m³) | 2026-07-15 | 2026-11-02 19:29 | 19 min | Active | 4.6 km |
| [6465603](https://explore.openaq.org/locations/6465603) | Mile - 12 Bus Terminal | Air sensor | HabitatMap | HabitatMap | HabitatMap Sensor | pm25 (µg/m³) | 2026-07-29 | 2026-11-02 19:29 | 19 min | Active | 9.3 km |
| [6446049](https://explore.openaq.org/locations/6446049) | Iganmu Blueline Train Station | Air sensor | HabitatMap | HabitatMap | HabitatMap Sensor | pm25 (µg/m³) | 2026-07-15 | 2026-11-02 19:29 | 19 min | Active | 6.6 km |
| [4986946](https://explore.openaq.org/locations/4986946) | Arepo - Ogun State | Air sensor | AirGradient | LAMATA | AirGradient Open Air Generation 1 (O-1PST) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-07-07 | 2026-11-02 19:00 | 49 min | Active | 19.7 km |
| [5038498](https://explore.openaq.org/locations/5038498) | Oshodi Bus Terminal 3 | Air sensor | AirGradient | LAMATA | AirGradient Open Air Max Generation 1 (O-M-1PPST-CE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-07-11 | 2026-11-02 19:00 | 49 min | Active | 4.6 km |
| [5045024](https://explore.openaq.org/locations/5045024) | Ifako-Ijaiye Bus Terminal | Air sensor | AirGradient | LAMATA | AirGradient Open Air Max Generation 1 (O-M-1PPST-CE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-07-12 | 2026-11-02 19:00 | 49 min | Active | 13.3 km |
| [5046018](https://explore.openaq.org/locations/5046018) | Agege Redline Train Station | Air sensor | AirGradient | LAMATA | AirGradient Open Air Max Generation 1 (O-M-1PPST-CE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-07-12 | 2026-11-02 19:00 | 49 min | Active | 12.2 km |
| [5350409](https://explore.openaq.org/locations/5350409) | LASWA - Five Cowries Terminal | Air sensor | AirGradient | LAMATA | AirGradient Open Air Max Generation 1 (O-M-1PPST-CE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-08-12 | 2026-11-02 19:00 | 49 min | Active | 10.5 km |
| [6098049](https://explore.openaq.org/locations/6098049) | Mile 12 Bus Terminal | Air sensor | AirGradient | LAMATA | AirGradient Open Air Max Generation 1 (O-M-1PPST-CE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-10-17 | 2026-11-02 19:00 | 49 min | Active | 9.3 km |
| [6385967](https://explore.openaq.org/locations/6385967) | Ojota Senior Secondary School, Lagos | Air sensor | AirGradient | Air Quality for Collective Public Health Action Project | AirGradient Open Air Max Generation 1 (O-M-1PPSTON-CE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2026-06-03 | 2026-11-02 19:00 | 49 min | Active | 6.6 km |
| [6412134](https://explore.openaq.org/locations/6412134) | Ikoyi-Obalende LCDA, Ikoyi Lagos | Air sensor | AirGradient | Air Quality for Collective Public Health Action Project | AirGradient Open Air Max Generation 1 (O-M-1PPSTON-CE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2026-06-21 | 2026-11-02 19:00 | 49 min | Active | 8.9 km |
| [6464052](https://explore.openaq.org/locations/6464052) | LAMATA Place | Air sensor | AirGradient | LAMATA | AirGradient Open Air Max Generation 1 (O-M-1PPST-CE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2026-07-28 | 2026-11-02 19:00 | 49 min | Active | 7.7 km |
| [6521348](https://explore.openaq.org/locations/6521348) | 588c8135a17c_Lagos Airport Road (MMIA) | Air sensor | AirGradient | Uniport-UCAM Urban AQ | AirGradient Open Air Max Generation 1 (O-M-1PPST-CE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2026-09-03 | 2026-11-02 19:00 | 49 min | Active | 6.0 km |
| [6522096](https://explore.openaq.org/locations/6522096) | 588c8135a1c8_Lagos- Lawanson Quality Bus Corridor | Air sensor | AirGradient | Uniport-UCAM Urban AQ | AirGradient Open Air Max Generation 1 (O-M-1PPST-CE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2026-09-03 | 2026-11-02 19:00 | 49 min | Active | 3.8 km |
| [6523113](https://explore.openaq.org/locations/6523113) | 588c8135a25c_Lagos - Ojuelegba Quality Bus Corridor | Air sensor | AirGradient | Uniport-UCAM Urban AQ | AirGradient Open Air Max Generation 1 (O-M-1PPST-CE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2026-09-04 | 2026-11-02 19:00 | 49 min | Active | 2.4 km |
| [5516338](https://explore.openaq.org/locations/5516338) | MARINA INTERCHANGE STATION | Air sensor | IQAir | LAMATA | AirVisual | pm25 (µg/m³) | 2025-08-21 | 2026-11-02 17:00 | 2 h | Active | 8.8 km |
| [5516341](https://explore.openaq.org/locations/5516341) | Mile 2 Interchange | Air sensor | IQAir | LAMATA | AirVisual | pm25 (µg/m³) | 2025-08-21 | 2026-11-02 17:00 | 2 h | Active | 16.0 km |
| [5516343](https://explore.openaq.org/locations/5516343) | Justrite - Ogolonto | Air sensor | IQAir | LAMATA | AirVisual | pm25 (µg/m³) | 2025-08-21 | 2026-11-02 17:00 | 2 h | Active | 14.9 km |
| [6336488](https://explore.openaq.org/locations/6336488) | airqo_g5469 | Air sensor | AirQo | OpenAQ admin | N/A | pm10 (µg/m³), pm25 (µg/m³) | 2026-05-05 | 2026-11-02 16:00 | 3 h | Active | 14.2 km |
| [6336490](https://explore.openaq.org/locations/6336490) | airqo_g5488 | Air sensor | AirQo | OpenAQ admin | N/A | pm10 (µg/m³), pm25 (µg/m³) | 2026-05-05 | 2026-11-02 16:00 | 3 h | Active | 4.5 km |
| [6336491](https://explore.openaq.org/locations/6336491) | airqo_g5503 | Air sensor | AirQo | OpenAQ admin | N/A | pm10 (µg/m³), pm25 (µg/m³) | 2026-05-05 | 2026-11-02 16:00 | 3 h | Active | 14.5 km |
| [6336493](https://explore.openaq.org/locations/6336493) | airqo_g5474 | Air sensor | AirQo | OpenAQ admin | N/A | pm10 (µg/m³), pm25 (µg/m³) | 2026-05-05 | 2026-11-02 16:00 | 3 h | Active | 2.3 km |
| [6336494](https://explore.openaq.org/locations/6336494) | airqo_g5379 | Air sensor | AirQo | OpenAQ admin | N/A | pm10 (µg/m³), pm25 (µg/m³) | 2026-05-05 | 2026-11-02 16:00 | 3 h | Active | 16.6 km |
| [6336496](https://explore.openaq.org/locations/6336496) | airqo_g5482 | Air sensor | AirQo | OpenAQ admin | N/A | pm10 (µg/m³), pm25 (µg/m³) | 2026-05-05 | 2026-11-02 16:00 | 3 h | Active | 16.1 km |
| [6337693](https://explore.openaq.org/locations/6337693) | airqo_g5505 | Air sensor | AirQo | OpenAQ admin | N/A | pm10 (µg/m³), pm25 (µg/m³) | 2026-05-06 | 2026-11-02 16:00 | 3 h | Active | 9.0 km |
| [6366721](https://explore.openaq.org/locations/6366721) | airqo_g5480 | Air sensor | AirQo | OpenAQ admin | N/A | pm10 (µg/m³), pm25 (µg/m³) | 2026-05-20 | 2026-11-02 16:00 | 3 h | Active | 2.0 km |
| [6397520](https://explore.openaq.org/locations/6397520) | University of Lagos | Air sensor | Aurassure | OpenAQ admin | N/A | pm10 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c) | 2026-04-30 | 2026-11-02 16:00 | 3 h | Active | 1.8 km |
| [5269430](https://explore.openaq.org/locations/5269430) | Fadeyi BRT Bus-Stop | Air sensor | AirGradient | LAMATA | AirGradient Open Air Max Generation 1 (O-M-1PPST-CE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-08-12 | 2026-11-02 14:00 | 5 h | Active | 1.3 km |
| [6336500](https://explore.openaq.org/locations/6336500) | airqo_g5483 | Air sensor | AirQo | OpenAQ admin | N/A | pm10 (µg/m³), pm25 (µg/m³) | 2026-05-05 | 2026-11-02 14:00 | 5 h | Active | 2.5 km |
| [6336497](https://explore.openaq.org/locations/6336497) | airqo_g5465 | Air sensor | AirQo | OpenAQ admin | N/A | pm10 (µg/m³), pm25 (µg/m³) | 2026-05-05 | 2026-11-02 13:00 | 6 h | Active | 8.2 km |
| [5011605](https://explore.openaq.org/locations/5011605) | Ikorodu Bus Terminal | Air sensor | AirGradient | LAMATA | AirGradient Open Air Max Generation 1 (O-M-1PPST-CE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-07-09 | 2026-11-02 10:00 | 9 h | Active | 17.3 km |
| [4903422](https://explore.openaq.org/locations/4903422) | Dolphin Estate - Lagos | Air sensor | AirGradient | LAMATA | AirGradient Open Air Generation 1 (O-1PST) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-06-29 | 2026-11-02 08:00 | 11 h | Active | 8.3 km |
| [5129500](https://explore.openaq.org/locations/5129500) | Abule Egaba Bus Terminal | Air sensor | AirGradient | LAMATA | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-08-14 | 2026-11-01 23:00 | 20 h | Active | 15.8 km |
| [6286018](https://explore.openaq.org/locations/6286018) | Miri Air - Diamond School, Ogijo | Air sensor | Miri Africa | Miri Africa | N/A | pm10 (µg/m³), pm25 (µg/m³), pressure (hpa), relativehumidity (%), temperature (c) | 2026-03-01 | 2026-11-01 18:00 | 1 d | Active | 23.6 km |
| [6286016](https://explore.openaq.org/locations/6286016) | Miri Air - Cathedral Church, Marina | Air sensor | Miri Africa | Miri Africa | Miri Air | pm10 (µg/m³), pm25 (µg/m³), pressure (hpa), relativehumidity (%), temperature (c) | 2026-03-01 | 2026-11-01 17:00 | 1 d | Active | 8.2 km |
| [6286025](https://explore.openaq.org/locations/6286025) | Miri Air - Igbogbo Ikorodu | Air sensor | Miri Africa | Miri Africa | Miri Air | pm10 (µg/m³), pm25 (µg/m³), pressure (hpa), relativehumidity (%), temperature (c) | 2026-03-19 | 2026-11-01 17:00 | 1 d | Active | 16.0 km |
| [6521401](https://explore.openaq.org/locations/6521401) | 588c8135a1bc_Lagos Ikeja Bus Terminal  | Air sensor | AirGradient | Uniport-UCAM Urban AQ | AirGradient Open Air Max Generation 1 (O-M-1PPST-CE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2026-09-03 | 2026-10-31 00:00 | 2 d | Active | 9.6 km |
| [6541902](https://explore.openaq.org/locations/6541902) | Oregun High School, Ikeja Lagos | Air sensor | AirGradient | AirGradient | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2026-09-15 | 2026-10-21 17:00 | 12 d | Active | 8.4 km |
| [6286020](https://explore.openaq.org/locations/6286020) | Miri Air - Ipaja | Air sensor | Miri Africa | Miri Africa | Miri Air | pm10 (µg/m³), pm25 (µg/m³), pressure (hpa), relativehumidity (%), temperature (c) | 2026-03-01 | 2026-10-20 17:00 | 13 d | Active | 14.1 km |
| [4579812](https://explore.openaq.org/locations/4579812) | Sagamu Road - Ikorodu | Air sensor | AirGradient | LAMATA | AirGradient ONE Generation 9 (I-9PSL-DE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-08-12 | 2026-09-27 23:00 | 35 d | Inactive | 19.4 km |
| [4959161](https://explore.openaq.org/locations/4959161) | Ketu - Lagos | Air sensor | AirGradient | LAMATA | AirGradient ONE Generation 9 (I-9PSL-DE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-07-04 | 2026-09-07 18:00 | 56 d | Inactive | 8.1 km |
| [3400895](https://explore.openaq.org/locations/3400895) | University of Lagos/Makoko | Air sensor | AirGradient | LAMATA | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-02-11 | 2026-09-05 23:00 | 57 d | Inactive | 1.0 km |
| [6286019](https://explore.openaq.org/locations/6286019) | Miri Air - Oregun | Air sensor | Miri Africa | Miri Africa | Miri Air | pm10 (µg/m³), pm25 (µg/m³), pressure (hpa), relativehumidity (%), temperature (c) | 2026-03-01 | 2026-08-23 03:00 | 71 d | Inactive | 8.5 km |
| [4605121](https://explore.openaq.org/locations/4605121) | M.K.O Abiola Gardens | Air sensor | AirGradient | LAMATA | AirGradient ONE Generation 9 (I-9PSL-DE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-08-13 | 2026-08-20 17:00 | 74 d | Inactive | 10.9 km |
| [6286021](https://explore.openaq.org/locations/6286021) | Miri Air - Amuwo Odofin | Air sensor | Miri Africa | Miri Africa | Miri Air | pm10 (µg/m³), pm25 (µg/m³), pressure (hpa), relativehumidity (%), temperature (c) | 2026-03-01 | 2026-08-08 10:00 | 86 d | Inactive | 8.3 km |
| [6286023](https://explore.openaq.org/locations/6286023) | Miri Air - Anwar-ul-Islam Model College | Air sensor | Miri Africa | Miri Africa | Miri Air | pm10 (µg/m³), pm25 (µg/m³), pressure (hpa), relativehumidity (%), temperature (c) | 2026-03-01 | 2026-07-31 17:00 | 94 d | Inactive | 12.0 km |
| [6286024](https://explore.openaq.org/locations/6286024) | Miri Air - Gbagada | Air sensor | Miri Africa | Miri Africa | Miri Air | pm10 (µg/m³), pm25 (µg/m³), pressure (hpa), relativehumidity (%), temperature (c) | 2026-03-01 | 2026-07-31 13:00 | 94 d | Inactive | 3.0 km |
| [6465775](https://explore.openaq.org/locations/6465775) | Majidun Bus Depot | Air sensor | HabitatMap | HabitatMap | HabitatMap Sensor | pm25 (µg/m³) | 2026-07-29 | 2026-07-29 18:37 | 96 d | Inactive | 14.0 km |
| [6095033](https://explore.openaq.org/locations/6095033) | Ojuelegba QBC | Air sensor | AirGradient | LAMATA | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-10-14 | 2026-06-03 13:00 | 152 d | Inactive | 2.4 km |
| [4850452](https://explore.openaq.org/locations/4850452) | Shagisha - Magodo | Air sensor | AirGradient | LAMATA | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-06-24 | 2026-05-09 13:00 | 177 d | Inactive | 9.9 km |
| [5188632](https://explore.openaq.org/locations/5188632) | Ojota Bus Terminal | Air sensor | AirGradient | LAMATA | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-08-12 | 2026-04-18 00:00 | 198 d | Inactive | 7.2 km |
| [5154310](https://explore.openaq.org/locations/5154310) | MMIA Ewu Bus Terminal | Air sensor | AirGradient | LAMATA | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-08-12 | 2026-04-15 10:00 | 201 d | Inactive | 7.0 km |
| [5108993](https://explore.openaq.org/locations/5108993) | Ikeja Bus Terminal  | Air sensor | AirGradient | LAMATA | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-08-22 | 2026-04-01 10:00 | 215 d | Inactive | 8.7 km |
| [4903342](https://explore.openaq.org/locations/4903342) | Osborne - Ikoyi | Air sensor | AirGradient | LAMATA | AirGradient Open Air Generation 1 (O-1PST) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-06-29 | 2026-03-15 22:00 | 231 d | Inactive | 8.8 km |
| [5269926](https://explore.openaq.org/locations/5269926) | Cele Bus Terminal | Air sensor | AirGradient | LAMATA | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-08-12 | 2026-01-12 10:00 | 294 d | Inactive | 5.2 km |
| [6135379](https://explore.openaq.org/locations/6135379) | Agidigbi - Acme Road | Air sensor | AirGradient | LAMATA | AirGradient Open Air Generation 1 (O-1PST) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-11-18 | 2025-12-30 16:00 | 307 d | Inactive | 11.3 km |
| [4839210](https://explore.openaq.org/locations/4839210) | Ikate - Lagos | Air sensor | AirGradient | LAMATA | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-06-23 | 2025-11-08 19:00 | 359 d | Inactive | 16.0 km |
| [5095987](https://explore.openaq.org/locations/5095987) | Iju Redline Train Station  | Air sensor | AirGradient | LAMATA | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-08-12 | 2025-10-06 18:00 | 1 y 27 d | Inactive | 16.7 km |
| [5016266](https://explore.openaq.org/locations/5016266) | LAMATA Place | Air sensor | AirGradient | LAMATA | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-07-09 | 2025-10-04 14:00 | 1 y 29 d | Inactive | 7.8 km |
| [5269431](https://explore.openaq.org/locations/5269431) | Ojuelegba QBC | Air sensor | AirGradient | LAMATA | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-09-01 | 2025-09-30 14:00 | 1 y 33 d | Inactive | 2.4 km |
| [4969237](https://explore.openaq.org/locations/4969237) | Oshodi | Air sensor | AirGradient | LAMATA | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-07-05 | 2025-07-21 10:00 | 1 y 104 d | Inactive | 4.6 km |
| [4944273](https://explore.openaq.org/locations/4944273) | LAMATA Place | Air sensor | AirGradient | LAMATA | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-07-03 | 2025-07-09 18:00 | 1 y 116 d | Inactive | 7.8 km |
| [5009574](https://explore.openaq.org/locations/5009574) | Ikorodu Bus Terminal | Air sensor | AirGradient | LAMATA | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-07-09 | 2025-07-09 09:00 | 1 y 116 d | Inactive | 17.3 km |
| [4944274](https://explore.openaq.org/locations/4944274) | Ikorodu Bus Terminal | Air sensor | AirGradient | LAMATA | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-07-03 | 2025-07-04 11:00 | 1 y 121 d | Inactive | 17.3 km |
| [404479](https://explore.openaq.org/locations/404479) | Lagos | Reference monitor | AirNow | Unknown Governmental Organization | Government Monitor | pm25 (µg/m³) | 2022-12-10 | 2025-02-12 16:00 | 1 y 263 d | Inactive | 9.8 km |

#### Nairobi

| Location ID | Name | Type | Provider | Owner | Instrument | Parameters | First report (UTC) | Last report (UTC) | Observed lag | Status | Distance |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [5119477](https://explore.openaq.org/locations/5119477) | Kitisuru | Air sensor | AirGradient | AirGradient | AirGradient Open Air Generation 1 (O-1PST) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-07-18 | 2026-11-02 19:00 | 49 min | Active | 9.4 km |
| [5199863](https://explore.openaq.org/locations/5199863) | Kihumo Village \|\| Antenna Array | Air sensor | AirGradient | The Demography Project | AirGradient Open Air Generation 1 (O-1PST) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-07-25 | 2026-11-02 19:00 | 49 min | Active | 14.8 km |
| [6237507](https://explore.openaq.org/locations/6237507) | Providence Academy  | Air sensor | AirGradient | AirGradient | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2026-02-12 | 2026-06-16 07:00 | 139 d | Inactive | 9.5 km |
| [6236592](https://explore.openaq.org/locations/6236592) | Marurui | Air sensor | AirGradient | AirGradient | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2026-02-11 | 2026-02-23 17:00 | 252 d | Inactive | 10.6 km |
| [6216058](https://explore.openaq.org/locations/6216058) | Mukuru- Pipeline | Air sensor | AirGradient | AirGradient | AirGradient Open Air Max Generation 1 (O-M-1PPST-CE) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2026-01-26 | 2026-02-06 06:00 | 269 d | Inactive | 8.9 km |
| [2156118](https://explore.openaq.org/locations/2156118) | Nairobi | Air sensor | Clarity | Clarity | Clarity Sensor | no2 (ppb), pm1 (µg/m³), pm10 (µg/m³), pm25 (µg/m³), temperature (f), temperature (c) | 2024-01-28 | 2025-10-16 05:47 | 1 y 17 d | Inactive | 11.7 km |
| [3394396](https://explore.openaq.org/locations/3394396) | Nairobi CMR | Reference monitor | AirNow | Unknown Governmental Organization | Government Monitor | pm25 (µg/m³) | 2025-02-06 | 2025-06-26 10:00 | 1 y 129 d | Inactive | 6.0 km |
| [5672958](https://explore.openaq.org/locations/5672958) | KENBIFS01 | Reference monitor | Clean Air Catalyst | OpenAQ admin | N/A, AIO 2, BAM 1022 | bc_375 (ng/m³), bc_880 (ng/m³), pm25 (µg/m³), pressure (hpa), relativehumidity (%), temperature (c), wind_direction (deg), wind_speed (m/s) | 2024-09-03 | 2025-05-31 15:00 | 1 y 155 d | Inactive | 0.8 km |
| [5672959](https://explore.openaq.org/locations/5672959) | KENBIMLK01 | Reference monitor | Clean Air Catalyst | OpenAQ admin | N/A, AIO 2, BAM 1022 | bc_375 (ng/m³), bc_470 (ng/m³), bc_528 (ng/m³), bc_625 (ng/m³), bc_880 (ng/m³), pm25 (µg/m³), pressure (hpa), relativehumidity (%), temperature (c), wind_direction (deg), wind_speed (m/s) | 2024-09-03 | 2025-05-31 15:00 | 1 y 155 d | Inactive | 9.2 km |
| [3399524](https://explore.openaq.org/locations/3399524) | Nairobi RR | Reference monitor | AirNow | Unknown Governmental Organization | Government Monitor | pm25 (µg/m³) | 2025-02-12 | 2025-02-17 16:00 | 1 y 258 d | Inactive | 7.1 km |
| [352507](https://explore.openaq.org/locations/352507) | Nairobi RR | Reference monitor | AirNow | Unknown Governmental Organization | Government Monitor | pm25 (µg/m³) | 2022-06-16 | 2025-02-12 15:00 | 1 y 263 d | Inactive | 5.8 km |
| [3394397](https://explore.openaq.org/locations/3394397) | Nairobi CMR | Reference monitor | AirNow | Unknown Governmental Organization | Government Monitor | pm25 (µg/m³) | 2025-02-10 | 2025-02-11 21:00 | 1 y 263 d | Inactive | 6.0 km |
| [2388059](https://explore.openaq.org/locations/2388059) | Nyayo Embakasi, Nairobi | Air sensor | AirGradient | Unknown Person | Unknown AirGradient Sensor, Unknown AirGradient Sensor | pm1 (µg/m³), pm1 (µg/m³), pm10 (µg/m³), pm10 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2024-02-06 | 2024-05-09 18:00 | 2 y 177 d | Inactive | 10.3 km |
| [6326576](https://explore.openaq.org/locations/6326576) | Nairobi, University of Nairobi, Parklands Campus, GEOHealth | Reference monitor | GeoHealth | GEOHealth Hub for Eastern Africa | BAM 1022 | pm25 (µg/m³) | 2019-08-20 | 2023-02-28 20:00 | 3 y 247 d | Inactive | 2.9 km |
| [6317](https://explore.openaq.org/locations/6317) | Alliance Girls High | Reference monitor | AirNow Kenya | Unknown Governmental Organization | Government Monitor | pm10 (µg/m³), pm25 (µg/m³) | 2018-04-21 | 2018-11-20 23:00 | 7 y 348 d | Inactive | 17.3 km |
| [5994](https://explore.openaq.org/locations/5994) | Nairobi CBD | Reference monitor | AirNow Kenya | Unknown Governmental Organization | Government Monitor | pm10 (µg/m³), pm25 (µg/m³) | 2018-04-23 | 2018-09-13 21:00 | 8 y 51 d | Inactive | 0.6 km |

#### Cairo

| Location ID | Name | Type | Provider | Owner | Instrument | Parameters | First report (UTC) | Last report (UTC) | Observed lag | Status | Distance |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [1621200](https://explore.openaq.org/locations/1621200) | Cairo | Reference monitor | AirNow | Unknown Governmental Organization | Government Monitor | pm25 (µg/m³) | 2023-09-25 | 2025-03-04 12:00 | 1 y 243 d | Inactive | 0.4 km |

#### Johannesburg

| Location ID | Name | Type | Provider | Owner | Instrument | Parameters | First report (UTC) | Last report (UTC) | Observed lag | Status | Distance |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [225424](https://explore.openaq.org/locations/225424) | Kliprivier | Reference monitor | South Africa | Unknown Governmental Organization | Government Monitor | co (ppm), no (ppm), no2 (ppm), nox (ppm), o3 (ppm), pm10 (µg/m³), pm25 (µg/m³), so2 (ppm) | 2021-04-29 | 2026-11-02 19:00 | 49 min | Active | 24.2 km |
| [6475117](https://explore.openaq.org/locations/6475117) | Little John Park  | Air sensor | AirGradient | Shift iT | AirGradient Open Air Generation 1 (O-1PST) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2026-08-05 | 2026-11-02 19:00 | 49 min | Active | 10.9 km |
| [6551402](https://explore.openaq.org/locations/6551402) | JWX 1 | Air sensor | AirGradient | Robin Kohl | AirGradient Open Air Generation 1 (O-1PST) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2026-10-05 | 2026-11-02 19:00 | 49 min | Active | 16.3 km |
| [225419](https://explore.openaq.org/locations/225419) | Buccleugh-NAQI | Reference monitor | South Africa | Unknown Governmental Organization | Government Monitor | co (ppm), no (ppm), no2 (ppm), nox (ppm), o3 (ppm), pm10 (µg/m³), pm25 (µg/m³), so2 (ppm) | 2021-04-29 | 2026-11-02 01:00 | 18 h | Active | 18.4 km |
| [225456](https://explore.openaq.org/locations/225456) | Alexandra-NAQI | Reference monitor | South Africa | Unknown Governmental Organization | Government Monitor | no (ppm), no2 (ppm), nox (ppm), pm10 (µg/m³), pm25 (µg/m³), so2 (ppm) | 2021-04-29 | 2026-09-21 00:00 | 42 d | Inactive | 12.5 km |
| [225445](https://explore.openaq.org/locations/225445) | Diepkloof-NAQI | Reference monitor | South Africa | Unknown Governmental Organization | Government Monitor | co (ppm), no (ppm), no2 (ppm), nox (ppm), o3 (ppm), pm10 (µg/m³), pm25 (µg/m³), so2 (ppm) | 2021-04-29 | 2026-08-31 07:00 | 63 d | Inactive | 10.4 km |
| [225446](https://explore.openaq.org/locations/225446) | Thokoza-NAQI | Reference monitor | South Africa | Unknown Governmental Organization | Government Monitor | pm10 (µg/m³), so2 (ppm) | 2021-04-29 | 2024-03-12 11:00 | 2 y 235 d | Inactive | 16.9 km |
| [225448](https://explore.openaq.org/locations/225448) | Jabavu-NAQI | Reference monitor | South Africa | Unknown Governmental Organization | Government Monitor | o3 (ppm), pm10 (µg/m³), pm25 (µg/m³), so2 (ppm) | 2021-04-28 | 2024-03-12 10:00 | 2 y 235 d | Inactive | 18.3 km |
| [230815](https://explore.openaq.org/locations/230815) | Mogale City | Reference monitor | South Africa | Unknown Governmental Organization | Government Monitor | co (ppm), no (ppm), no2 (ppm), nox (ppm), o3 (ppm), pm10 (µg/m³), so2 (ppm) | 2021-08-03 | 2023-12-11 16:00 | 2 y 327 d | Inactive | 24.4 km |
| [1321146](https://explore.openaq.org/locations/1321146) | Glen Austin | Reference monitor | South Africa | Unknown Governmental Organization | Government Monitor | so2 (ppm) | 2023-07-26 | 2023-07-26 23:00 | 3 y 99 d | Inactive | 12.0 km |
| [225401](https://explore.openaq.org/locations/225401) | Bedfordview-NAQI | Reference monitor | South Africa | Unknown Governmental Organization | Government Monitor | co (ppm), pm10 (µg/m³), pm25 (µg/m³), so2 (ppm) | 2021-04-29 | 2023-03-27 16:00 | 3 y 221 d | Inactive | 9.0 km |
| [364067](https://explore.openaq.org/locations/364067) | Germiston - Delville | Reference monitor | South Africa | Unknown Governmental Organization | Government Monitor | so2 (ppm) | 2021-05-28 | 2021-05-28 17:00 | 5 y 159 d | Inactive | 13.2 km |

#### Kinshasa

| Location ID | Name | Type | Provider | Owner | Instrument | Parameters | First report (UTC) | Last report (UTC) | Observed lag | Status | Distance |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [3700227](https://explore.openaq.org/locations/3700227) | KINAQ Masiala | Air sensor | AirGradient | KINAQ Huilleries | AirGradient Open Air Generation 1 (O-1PST) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-03-17 | 2026-11-02 19:00 | 49 min | Active | 8.2 km |
| [4615778](https://explore.openaq.org/locations/4615778) | Kintambo | Air sensor | AirGradient | KINAQ Huilleries | AirGradient Open Air Generation 1 (O-1PST) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-06-04 | 2026-11-02 19:00 | 49 min | Active | 12.2 km |
| [6301642](https://explore.openaq.org/locations/6301642) | WASARU ASBL / KINAQ Lemba | Air sensor | AirGradient | AirGradient | AirGradient Open Air Generation 1 (O-1PST) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2026-04-09 | 2026-11-02 19:00 | 49 min | Active | 7.2 km |
| [6341980](https://explore.openaq.org/locations/6341980) | WASARU / KINAQ Huilleries | Air sensor | AirGradient | KINAQ Huilleries | AirGradient Open Air Generation 1 (O-1PST) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2026-05-09 | 2026-11-02 19:00 | 49 min | Active | 15.0 km |
| [3653523](https://explore.openaq.org/locations/3653523) | KINAQ Kimwenza | Air sensor | AirGradient | KINAQ Huilleries | AirGradient Open Air Generation 1 (O-1PST) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-03-17 | 2026-11-02 15:00 | 4 h | Active | 3.2 km |
| [3844009](https://explore.openaq.org/locations/3844009) | KINAQ Gare Centrale | Air sensor | AirGradient | KINAQ Huilleries | AirGradient Open Air Generation 1 (O-1PST) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-03-26 | 2026-10-31 13:00 | 2 d | Active | 16.2 km |
| [3874915](https://explore.openaq.org/locations/3874915) | KINAQ BelAir | Air sensor | AirGradient | KINAQ Huilleries | AirGradient Open Air Generation 1 (O-1PST) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-03-29 | 2026-10-31 04:00 | 2 d | Active | 1.2 km |
| [3858835](https://explore.openaq.org/locations/3858835) | KINAQ Kalembelembe | Air sensor | AirGradient | KINAQ Huilleries | AirGradient Open Air Generation 1 (O-1PST) | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-03-27 | 2026-10-29 10:00 | 4 d | Active | 13.6 km |
| [3918624](https://explore.openaq.org/locations/3918624) | KINAQ Limete | Air sensor | AirGradient | KINAQ Huilleries | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-04-01 | 2026-10-28 16:00 | 5 d | Active | 12.0 km |
| [3750766](https://explore.openaq.org/locations/3750766) | KINAQ UPN | Air sensor | AirGradient | KINAQ Huilleries | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-03-18 | 2026-08-01 06:00 | 93 d | Inactive | 4.9 km |
| [6341934](https://explore.openaq.org/locations/6341934) | WASARU | Air sensor | AirGradient | AirGradient | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2026-05-09 | 2026-05-09 17:00 | 177 d | Inactive | 15.0 km |
| [3838823](https://explore.openaq.org/locations/3838823) | KINAQ Huilleries | Air sensor | AirGradient | KINAQ Huilleries | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-03-25 | 2026-04-29 12:00 | 187 d | Inactive | 15.0 km |
| [3862442](https://explore.openaq.org/locations/3862442) | KINAQ Cité Verte | Air sensor | AirGradient | KINAQ Huilleries | Unknown AirGradient Sensor | pm1 (µg/m³), pm25 (µg/m³), relativehumidity (%), temperature (c), um003 (particles/cm³) | 2025-03-27 | 2026-04-09 11:00 | 207 d | Inactive | 1.0 km |
| [352508](https://explore.openaq.org/locations/352508) | Kinshasa | Reference monitor | AirNow | Unknown Governmental Organization | Government Monitor | pm25 (µg/m³) | 2022-06-16 | 2025-02-17 05:00 | 1 y 258 d | Inactive | 16.5 km |

## Update frequency

- Accepted source reporting frequency is "between 10 minutes and 24 hours" ([FAQ](https://docs.openaq.org/about/faq)). This is an ingestion criterion, so each location updates at its provider's own cadence.
- Ingestion latency between the real-world measurement and its availability in the API: **Unknown**. Checked [About](https://docs.openaq.org/about/about), [FAQ](https://docs.openaq.org/about/faq), [Explorer guide](https://explore.openaq.org/getting-started) and [Rate limits](https://docs.openaq.org/using-the-api/rate-limits); none states a figure. The "Observed lag" column in the coverage tables above records how stale each location was at query time.
- S3 archive: files are written 72 hours after the end of each day and may be patched later ([Archive guide](https://docs.openaq.org/docs/accessing-openaq-archive-data)); the AWS registry lists the bucket as updated hourly ([AWS Open Data Registry](https://registry.opendata.aws/openaq/)).

## Historical availability

- Each location reports `datetimeFirst` and `datetimeLast` ([Locations](https://docs.openaq.org/resources/locations)); history depth therefore varies by location and is shown per station in the coverage tables.
- History is available through the same API via `datetime_from` / `datetime_to` on `/v3/sensors/{id}/measurements` and the aggregate endpoints ([Measurements operation](https://docs.openaq.org/api/operations/sensor_measurements_get_v3_sensors__sensors_id__measurements_get)). Long aggregations computed from raw measurements can time out with HTTP 408; narrowing the date range is recommended ([Measurements](https://docs.openaq.org/resources/measurements)).
- For large historical pulls OpenAQ points to the S3 archive ([FAQ](https://docs.openaq.org/about/faq)).

## Identifiers

- Integer IDs for `locations`, `sensors`, `parameters`, `providers`, `owners`, `instruments`, `licenses` and `countries` ([API reference](https://docs.openaq.org/api)). A location has one or more sensors; each sensor measures one parameter ([Locations](https://docs.openaq.org/resources/locations)).
- A measurement has no ID of its own. The natural key is `sensors_id` + `period.datetimeTo.utc` ([Measurements operation](https://docs.openaq.org/api/operations/sensor_measurements_get_v3_sensors__sensors_id__measurements_get)).
- The S3 archive is partitioned by `locationid` ([Archive guide](https://docs.openaq.org/docs/accessing-openaq-archive-data)).
- Stability of IDs over time: **Unknown**. Checked [Locations](https://docs.openaq.org/resources/locations), [API reference](https://docs.openaq.org/api), [FAQ](https://docs.openaq.org/about/faq) and [Gone](https://docs.openaq.org/errors/gone); no stability guarantee is published. Connectors should store OpenAQ IDs as source identifiers, not as Africa Pulse canonical keys.

## Timestamp semantics

- What time does each timestamp represent: datetimes mark the **end** of a period. "Data on OpenAQ are harmonized to follow an exclusive time-ending standard"; an hourly value stamped 03:00 covers 02:00 to 02:59. Dates (as opposed to datetimes) mark the **start** of a period ([Dates and datetimes](https://docs.openaq.org/using-the-api/dates-datetimes)). Each measurement carries `period.datetimeFrom` and `period.datetimeTo` ([Measurements](https://docs.openaq.org/resources/measurements)). Publication or ingestion time is not exposed: **Unknown**, checked the measurement response schema ([Measurements operation](https://docs.openaq.org/api/operations/sensor_measurements_get_v3_sensors__sensors_id__measurements_get)).
- Which time zone: every datetime is returned twice, as `utc` (`Z`) and `local` (with offset), e.g. `"utc": "2019-07-11T20:00:00Z"`, `"local": "2019-07-11T14:00:00-06:00"`. The location's `timezone` field is an IANA tz database ID ([Dates and datetimes](https://docs.openaq.org/using-the-api/dates-datetimes)). Query parameters given without a time zone are interpreted in the station's local time ([Dates and datetimes](https://docs.openaq.org/using-the-api/dates-datetimes)), so connectors must always send UTC with a `Z` suffix. S3 archive files use ISO 8601 with offset, e.g. `2023-02-22T01:00:00-07:00` ([Archive guide](https://docs.openaq.org/docs/accessing-openaq-archive-data)).
- Granularity: raw values at the provider's interval (10 minutes to 24 hours, [FAQ](https://docs.openaq.org/about/faq)); the raw example has `period.label` "raw" and `interval` "01:00:00" ([Measurements](https://docs.openaq.org/resources/measurements)). Aggregates: hourly means, daily means from 01:00 to 00:00 local time, yearly means from 1 January 01:00 to 31 December 00:00 local time ([Measurements](https://docs.openaq.org/resources/measurements)).

## Units

- Values are physical concentrations, not AQI ([About](https://docs.openaq.org/about/about), [Explorer guide](https://explore.openaq.org/getting-started)).
- The unit is defined per parameter in `parameter.units`, e.g. `pm25` in µg/m³ ([Parameters](https://docs.openaq.org/resources/parameters)), while the raw measurement example reports `o3` in ppm ([Measurements](https://docs.openaq.org/resources/measurements)). Gas pollutants can therefore arrive in mass (µg/m³) or volume (ppm) units, and connectors must read `parameter.units` on every record rather than assume a unit per pollutant name.
- Aggregates carry `summary` statistics (`min`, `q02`, `q25`, `median`, `q75`, `q98`, `max`, `avg`, `sd`) in the same unit as `value` ([Measurements operation](https://docs.openaq.org/api/operations/sensor_measurements_get_v3_sensors__sensors_id__measurements_get)).

### Parameters measured in the five target cities

Generated from `GET /v3/parameters` ([Parameters](https://docs.openaq.org/resources/parameters)) and the sensors of the locations above, on 2026-11-02 19:49 UTC.

| Parameter ID | Name | Display name | Units | Description | Seen in |
|---|---|---|---|---|---|
| 1 | pm10 | PM10 | µg/m³ | Particulate matter less than 10 micrometers in diameter mass concentration | Lagos, Nairobi, Johannesburg |
| 2 | pm25 | PM2.5 | µg/m³ | Particulate matter less than 2.5 micrometers in diameter mass concentration | Lagos, Nairobi, Cairo, Johannesburg, Kinshasa |
| 7 | no2 | NO₂ | ppm | Nitrogen Dioxide concentration | Johannesburg |
| 8 | co | CO | ppm | Carbon Monoxide concentration | Johannesburg |
| 9 | so2 | SO₂ | ppm | Sulfur Dioxide concentration | Johannesburg |
| 10 | o3 | O₃ | ppm | Ozone concentration | Johannesburg |
| 15 | no2 | NO₂ | ppb | Unknown | Nairobi |
| 19 | pm1 | PM1 | µg/m³ | Particulate matter less than 1 micrometer in diameter mass concentration | Lagos, Nairobi, Johannesburg, Kinshasa |
| 22 | wind_direction | Wind direction | deg | Direction that the wind originates from | Nairobi |
| 34 | wind_speed | Wind speed | m/s | Average wind speed in meters per second | Nairobi |
| 35 | no | NO | ppm | Nitrogen Monoxide concentration | Johannesburg |
| 95 | pressure | Atmospheric pressure | hpa | Atmospheric or barometric pressure | Lagos, Nairobi |
| 98 | relativehumidity | RH | % | Unknown | Lagos, Nairobi, Johannesburg, Kinshasa |
| 100 | temperature | Temperature (C) | c | Unknown | Lagos, Nairobi, Johannesburg, Kinshasa |
| 125 | um003 | PM0.3 count | particles/cm³ | Unknown | Lagos, Nairobi, Johannesburg, Kinshasa |
| 128 | temperature | Temperature (F) | f | Unknown | Nairobi |
| 19840 | nox | NOx | ppm | Nitrogen Oxides concentration | Johannesburg |
| 19861 | bc_375 | BC 375nm | ng/m³ | Black Carbon mass concentration 375nm  | Nairobi |
| 19862 | bc_470 | BC 470nm | ng/m³ | Black Carbon mass concentration 470nm  | Nairobi |
| 19863 | bc_528 | BC 528nm | ng/m³ | Black Carbon mass concentration 528nm  | Nairobi |
| 19864 | bc_625 | BC 625nm | ng/m³ | Black Carbon mass concentration 625nm  | Nairobi |
| 19865 | bc_880 | BC 880nm | ng/m³ | Black Carbon mass concentration 880nm  | Nairobi |

## Rate limits

- Free tier: 60 requests per minute and 2,000 requests per hour; higher limits on request ("Contact us for pricing") ([Rate limits](https://docs.openaq.org/using-the-api/rate-limits)).
- Response headers: `x-ratelimit-used`, `x-ratelimit-limit`, `x-ratelimit-remaining`, `x-ratelimit-reset` ([Rate limits](https://docs.openaq.org/using-the-api/rate-limits)).
- Exceeding the limit returns HTTP 429; "Exceeding API rate limits repeatedly can lead to either a temporary or permanent ban" ([Rate limits](https://docs.openaq.org/using-the-api/rate-limits)).
- Page size: `limit` default 100, maximum 1,000 on `/v3/locations` ([Python client, locations](https://python.openaq.org/resources/locations/)). Maximum `limit` on `/v3/sensors/{id}/measurements`: **Unknown**, the operation page gives only the default of 100 ([Measurements operation](https://docs.openaq.org/api/operations/sensor_measurements_get_v3_sensors__sensors_id__measurements_get)).
- Access "at rates higher than the documented rate limit" requires a separate paid agreement ([Terms of use](https://docs.openaq.org/about/terms)).

## Terms of use

- License: there is no single license for OpenAQ data. Each provider's data keeps its own license, and "the data publisher may elect to make the data available under the Creative Commons Attribution license (CC BY 4.0)" ([Data Policy](https://docs.openaq.org/docs/data-policy)). Licenses are exposed through `/v3/licenses` with the flags `commercialUseAllowed`, `attributionRequired`, `shareAlikeRequired`, `modificationAllowed` and `redistributionAllowed`; the documented example is license ID 41, "CC BY 4.0 DEED" ([Licenses](https://docs.openaq.org/resources/licenses)). The licenses that actually apply to the five target cities are listed in the table below. Use of the platform is governed by the OpenAQ [Terms of use](https://docs.openaq.org/about/terms); "As per OpenAQ's Terms of Use, compliance is required" with each license ([Licenses](https://docs.openaq.org/resources/licenses)).
- Commercial use permitted? Depends on the provider license (`commercialUseAllowed`); CC BY 4.0 permits it ([Licenses](https://docs.openaq.org/resources/licenses)). Platform restriction: using the hosted API "to develop products or services that substantially duplicate or directly compete with OpenAQ's core offerings is prohibited" ([Terms of use](https://docs.openaq.org/about/terms)).
- Storage permitted? The OpenAQ Terms of use do not address storage of retrieved data: **Unknown** at platform level, checked [Terms of use](https://docs.openaq.org/about/terms), [Data Policy](https://docs.openaq.org/docs/data-policy) and [FAQ](https://docs.openaq.org/about/faq). For data under CC BY 4.0, the license grants the right to reproduce the material ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)), which covers storing copies. Retrieval itself is restricted: "downloading data is strictly prohibited unless done through registered and authorized use" ([Terms of use](https://docs.openaq.org/about/terms)).
- Redistribution permitted? Depends on the provider license (`redistributionAllowed`) ([Licenses](https://docs.openaq.org/resources/licenses)). OpenAQ states it only uses "data that, to the best of our knowledge, has been made available for free redistribution" ([Data Policy](https://docs.openaq.org/docs/data-policy)).

### Licenses on locations in the five target cities

Generated from the `licenses` field of each location and `GET /v3/licenses/{id}` ([Licenses](https://docs.openaq.org/resources/licenses)) on 2026-11-02 19:49 UTC.

| License ID | Name | Commercial use | Attribution required | Share-alike | Modification | Redistribution | Source | Attribution (per location) | Cities |
|---|---|---|---|---|---|---|---|---|---|
| 33 | US Public Domain | Yes | No | No | Yes | Yes | [link](http://www.usa.gov/publicdomain/label/1.0/) | Unknown Governmental Organization | Lagos, Nairobi, Cairo, Kinshasa |
| 38 | CC0 1.0 | Yes | No | No | Yes | Yes | [link](https://creativecommons.org/publicdomain/zero/1.0/deed.ca) | Clarity | Nairobi |
| 41 | CC BY 4.0 | Yes | Yes | No | Yes | Yes | [link](https://creativecommons.org/licenses/by/4.0/) | Air Quality for Collective Public Health Action Project; AirGradient; GEOHealth Hub for Eastern Africa; KINAQ Huilleries; LAMATA; Miri Africa; OpenAQ admin; Robin Kohl; Shift iT; The Demography Project; Uniport-UCAM Urban AQ; Unknown Person | Lagos, Nairobi, Johannesburg, Kinshasa |

## Attribution requirements

- "When required, OpenAQ users must acknowledge the original source(s) of any data they use" ([Terms of use](https://docs.openaq.org/about/terms)); the Terms also require attribution to OpenAQ when data is accessed through its services ([Terms of use](https://docs.openaq.org/about/terms)). The Data Policy adds: "We strongly encourage OpenAQ users to acknowledge the original source(s) of any data they use" ([Data Policy](https://docs.openaq.org/docs/data-policy)).
- Whether attribution is required for a given location is set by `attributionRequired` on its license ([Licenses](https://docs.openaq.org/resources/licenses)); the attribution name and URL per location are shown in the licenses table above.
- Exact attribution wording prescribed by OpenAQ: **Unknown**, no fixed text found in [Terms of use](https://docs.openaq.org/about/terms), [Data Policy](https://docs.openaq.org/docs/data-policy) or [FAQ](https://docs.openaq.org/about/faq). Proposed form for Africa Pulse outputs: "Air-quality data: <provider / attribution name> via OpenAQ (openaq.org), <license name>."

## Redistribution restrictions

- Africa Pulse may redistribute raw or derived OpenAQ data only where the location's license has `redistributionAllowed: true`, and must then meet `attributionRequired` and `shareAlikeRequired` ([Licenses](https://docs.openaq.org/resources/licenses)). Because the license is per location and can change over time (license records carry their own validity dates, see the licenses table), the license ID must be stored with every observation.
- Africa Pulse must not operate as a substitute for the OpenAQ API: the competing-service clause applies ([Terms of use](https://docs.openaq.org/about/terms)).
- OpenAQ data is "offered as-is, without warranty of any kind" ([Terms of use](https://docs.openaq.org/about/terms)); redistributed outputs should carry the same caveat.
- No bulk OpenAQ data is committed to this repository, in line with [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Known limitations

- Coverage in Africa is uneven and limited to openly licensed, stationary, ground-level data ([FAQ](https://docs.openaq.org/about/faq)); see the per-city tables for which cities have current data.
- Mixed instrument quality. Reference monitors are "the 'gold standard'", typically government-run; air sensors are "less sophisticated" and easier to deploy ([Explorer guide](https://explore.openaq.org/getting-started)). The `monitor` filter separates the two ([Python client, locations](https://python.openaq.org/resources/locations/)). The documentation defines `isMonitor` inconsistently: "whether the station is actively monitoring air quality" on the location ([Locations](https://docs.openaq.org/resources/locations)) and "whether the device is used for official monitoring" on the instrument ([Instruments](https://docs.openaq.org/resources/instruments)). Africa Pulse should store both `isMonitor` and the instrument name.
- Data gaps can come from "technical issues from the upstream data provider" or OpenAQ ingestion problems ([FAQ](https://docs.openaq.org/about/faq)).
- Late-arriving corrections: S3 archive files may be patched after first publication ([Archive guide](https://docs.openaq.org/docs/accessing-openaq-archive-data)).
- Measurements carry `flagInfo.hasFlags` ([Measurements operation](https://docs.openaq.org/api/operations/sensor_measurements_get_v3_sensors__sensors_id__measurements_get)) and flags are listed at `/v3/locations/{id}/flags` and `/v3/sensors/{id}/flags` ([API reference](https://docs.openaq.org/api)); flag semantics are not documented on the pages checked. Values are not otherwise quality-assured: "we cannot guarantee its accuracy or suitability for any user's purpose" ([Data Policy](https://docs.openaq.org/docs/data-policy)).
- Units differ by parameter ID for the same pollutant (see Units).
- Queries without a time zone are read as station-local time ([Dates and datetimes](https://docs.openaq.org/using-the-api/dates-datetimes)).
- Radius search is capped at 25 km ([Python client, locations](https://python.openaq.org/resources/locations/)). This covers central Lagos, Cairo and Johannesburg but not their full metropolitan extent; a `bbox` per canonical city will be needed once the city entity model is defined.

## Sample request and response

Requests made on 2026-11-02 19:49 UTC. The API key is a placeholder; the real key was read from a local environment variable and is not committed.

```bash
# Locations within 25 km of central Lagos
curl --request GET \
  --url "https://api.openaq.org/v3/locations?coordinates=6.5244,3.3792&radius=25000&limit=1000" \
  --header "X-API-Key: YOUR-OPENAQ-API-KEY"

# Raw measurements for sensor 16934671 (pm25) at location 6446050
curl --request GET \
  --url "https://api.openaq.org/v3/sensors/16934671/measurements?datetime_from=2026-11-02T13%3A00%3A00Z&datetime_to=2026-11-02T19%3A30%3A02Z&limit=3" \
  --header "X-API-Key: YOUR-OPENAQ-API-KEY"
```

License check: location 6446050 has license ID(s) none recorded, which does not confirm `redistributionAllowed: true`, so no response values are reproduced. The request returned 3 record(s) with fields: `coordinates`, `coverage`, `flagInfo`, `parameter`, `period`, `summary`, `value`.

## Assessment

OpenAQ is a good fit as Africa Pulse's first air-quality source. It provides one schema across many networks, UTC and local timestamps on every record, explicit units per parameter, a reference-monitor versus air-sensor flag, and a machine-readable license on every location. These map directly onto the project's provenance and data-quality principles.

Risks:

1. **Coverage.** Usefulness per city depends on the coverage tables above. Cities served only by air sensors, or by locations that have stopped reporting, need that limitation represented explicitly rather than filled.
2. **Per-location licensing.** License terms vary by provider, so the connector must record the license ID on every observation and filter what is redistributed.
3. **API key terms.** One key per individual, non-transferable. A shared production pipeline needs a key held by the project, or a custom agreement with OpenAQ, not a contributor's personal key. This should be confirmed with OpenAQ before the connector runs on shared infrastructure.
4. **Competing-service clause.** Africa Pulse integrates and analyses data rather than re-serving the OpenAQ catalogue, but maintainers should confirm this reading with OpenAQ before any public API or bulk export of OpenAQ-derived data.
5. **Rate limits.** 2,000 requests per hour is enough for five cities on an hourly schedule, but backfills should use the S3 archive rather than the API.
6. **Quality.** Air-sensor data and flagged values need quality rules before they feed analytical marts.

## Researched by

@Oyetoluzeenat. Documentation, terms of use and data policy checked on 2026-11-01. API queried on 2026-11-02 19:49 UTC.
