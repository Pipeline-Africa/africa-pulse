# Source Register Entry: World bank Indicators 

## Summary

The World Bank Open Data / World Development Indicators (WDI) API provides open access to over 1,400 global development indicators spanning macroeconomic, demographic, energy, labor, and infrastructure metrics. It serves as a foundational source for contextualizing national-level economic growth, urban population trends, and infrastructural developments across African countries for Africa Pulse.

## Owner

The World Bank Group (International Bank for Reconstruction and Development / International Development Association).

## Documentation

- Main documentation URL: https://data.worldbank.org
- API reference URL: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation
- Terms of use URL: https://data.worldbank.org/summary-terms-of-use

## Domain
Economic indicators / Other (Socioeconomic, Demographics, Infrastructure)

## Access method
REST API, bulk CSV/JSON/XML dataset downloads, and Python/R client packages (`wbdata`, `wbstats`).

## Authentication

None. No API key or registration is required to query the API. The API is completely free and openly accessible.

## Geographic coverage

Coverage: All 54 sovereign African countries and regional aggregates (e.g., Sub-Saharan Africa `SSF`, Middle East & North Africa `MEA`).
Location Specification:** ISO-2 or ISO-3 country codes (e.g., `NG` / `NGA` for Nigeria, `KE` / `KEN` for Kenya, `EG` / `EGY` for Egypt, `ZA` / `ZAF` for South Africa, `CD` / `COD` for DR Congo) or World Bank regional codes (`SSF`, `AFE`, `AFW`).
City Coverage: City-level geospatial data is **not** available; indicators are reported strictly at the national or regional level.


## Update frequency
Updated quarterly (typically April, July, September, and December). Data lags real-world events by 1 to 2 years due to compilation procedures from national statistical offices.

## Historical availability
Data spans back to 1960 for standard macroeconomic indicators. Historical records are fully retrievable through the same REST API endpoint using the `date` parameter (e.g., `?date=1960:2024`).

## Identifiers
Entity Identifiers:** Standardized ISO-3166 alpha-2 and alpha-3 codes for countries.
Indicator Identifiers:** Structured series codes (e.g., `NY.GDP.MKTP.CD` for GDP in current USD, `SP.URB.TOTL.IN.ZS` for urban population percentage). Identifiers are stable over time.

## Timestamp semantics
Time Represented: Period end / annual summary (or quarterly/monthly aggregate where applicable).
Time Zone: Not applicable (annual or monthly period values).
Granularity: Mostly annual (`YYYY`), with select indicators available at quarterly or monthly frequencies.

## Units

Units vary depending on the indicator:
* `NY.GDP.MKTP.CD`: Current US Dollars ($)
* `SP.URB.TOTL.IN.ZS`: Percentage (`%`) of total population
* `EG.ELC.ACCS.ZS`: Percentage (`%`) of population with access
* `FP.CPI.TOTL.ZG`: Inflation rate (`%` annual)
* `SP.POP.TOTL`: Headcount (Count)

## Rate limits
* No strict rate limits or hard daily quotas are published.
* Fair-use policy: Concurrency should be kept reasonable (recommended <= 10 requests per second).
* Payload limits: Pagination defaults to 50 items per page; can be expanded to 1,000 to 10,000 items per request via `?per_page=10000`.

## Terms of use
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0) by default for World Bank-produced datasets.
* **Commercial use permitted:** Yes.
* **Storage permitted:** Yes.
* **Attribution requirements:** Must cite "The World Bank" as the source and indicate if changes were made.
* **Exact attribution text:** "Data from World Bank Development Indicators, licensed under CC BY 4.0."

## Redistribution restrictions
Raw and derived datasets may be redistributed provided CC BY 4.0 attribution conditions are preserved. No claims of official endorsement by the World Bank Group may be made.

## Known limitations
* Lack of sub-national or city-level granularity (reports national totals/percentages only).
* Heavy reporting lag (1–2 years behind the current date for many African nations).
* Incomplete or estimated records for regions facing conflict or reporting disruptions (e.g., DR Congo historical gaps).

## Sample request and response

### Request
`GET https://api.worldbank.org/v2/country/NGA/indicator/NY.GDP.MKTP.CD?date=2020:2022&format=json`

### Response
```json
[
  {
    "page": 1,
    "pages": 1,
    "per_page": 50,
    "total": 3,
    "sourceid": "2",
    "sourcename": "World Development Indicators",
    "lastupdated": "2024-03-28"
  },
  [
    {
      "indicator": {
        "id": "NY.GDP.MKTP.CD",
        "value": "GDP (current US$)"
      },
      "country": {
        "id": "NGA",
        "value": "Nigeria"
      },
      "countryiso3code": "NGA",
      "date": "2022",
      "value": 477386116801.129,
      "unit": "",
      "obs_status": "",
      "decimal": 0
    },
    {
      "indicator": {
        "id": "NY.GDP.MKTP.CD",
        "value": "GDP (current US$)"
      },
      "country": {
        "id": "NGA",
        "value": "Nigeria"
      },
      "countryiso3code": "NGA",
      "date": "2021",
      "value": 440833583923.018,
      "unit": "",
      "obs_status": "",
      "decimal": 0
    }
  ]
]

## Assessment
Fit: Excellent macro-level baseline source for context and cross-country comparisons across Africa.

Risks: Cannot be used for real-time monitoring or city-scale operational analytics due to annual aggregation and reporting delays.


## Researched by
1. Checker Info
GitHub Handle: @mrabarah1

Date Checked: October 20, 2026

GitHub handle and date checked (terms change, so the date matters).


### 2. Real Request Execution
Verified via standard `curl` request:
`curl -s "https://api.worldbank.org/v2/country/KEN/indicator/SP.POP.TOTL?date=2022:2023&format=json"`

### 3. Key Findings
* Timestamps represent annual periods (`YYYY`).
* Coverage is comprehensive at the national level for all 54 African nations, but non-existent at the city/sub-national level.
* License ([CC BY 4.0](https://datacatalog.worldbank.org/public-licenses)) fully permits commercial ingestion, storage, transformation, and redistribution.

### 4. Urban Indicator Completeness Check (Focus Countries)

| Indicator Code | Indicator Name | Nigeria (NGA) | Kenya (KEN) | Egypt (EGY) | South Africa (ZAF) | DR Congo (COD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `SP.URB.TOTL.IN.ZS` | Urban population (% of total) | Complete | Complete | Complete | Complete | Complete |
| `SP.URB.GROW` | Urban population growth (annual %) | Complete | Complete | Complete | Complete | Complete |
| `EG.ELC.ACCS.UR.ZS` | Access to electricity, urban (% of urban pop) | Complete | Complete | Complete | Complete | Incomplete / Sparse |
| `EN.ATM.PM25.MC.M3` | PM2.5 air pollution, mean annual (mcg/cu.m) | Moderate | Moderate | Moderate | Moderate | Moderate |
| `IT.NET.USER.ZS` | Individuals using the Internet (% of pop) | Complete | Complete | Complete | Complete | Sparse |
| `NY.GDP.MKTP.CD` | GDP (current US$) | Complete | Complete | Complete | Complete | Complete |

### 5. Revisions Policy
Historical data for past years can and does change retroactively. When national statistical offices (NSOs) release updated census data, rebase national accounts, or adjust inflation calculations, the World Bank updates those historic values during its quarterly releases.
