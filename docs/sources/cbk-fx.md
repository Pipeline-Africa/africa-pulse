# Central Bank of Kenya (CBK) — Foreign Exchange Rates

## Summary

The Central Bank of Kenya publishes daily indicative foreign-exchange rates for public use. Its published rates are compiled by the Financial Markets department and reflect average buying and selling rates of major market participants at the start of each trading day.

This source is a candidate for Kenya's official central-bank reference data. Its indicative rates should not be treated as guaranteed transaction prices offered by a particular bank, bureau, or parallel-market dealer.

## Owner

- **Organisation:** Central Bank of Kenya (CBK)
- **Country:** Kenya
- **Official rates page:** https://www.centralbank.go.ke/rates/forex-exchange-rates/
- **Methodology information:** https://www.centralbank.go.ke/forex/

## Documentation

- **Main rates page:** https://www.centralbank.go.ke/rates/forex-exchange-rates/
- **Methodology:** https://www.centralbank.go.ke/forex/
- **Public API documentation:** Unknown. A supported public API contract was not identified during this research.

## Domain

Foreign exchange reference rates, including daily currency mean, buying, and selling rates.

## Access method

- **Observed access method:** Official website with a published rate table and historical-data/export functionality.
- **Programmatic API:** Unknown. No documented, supported public API was confirmed.
- **Historical access:** The CBK site links to historical data and supports a large table of observations.
- **Recommended initial integration approach:** Validate the site's export format and stability before choosing between downloading published files and extracting the web table.

## Authentication

Unknown for programmatic access. The public rates page is accessible without an account, but this does not establish API authentication requirements.

## Geographic coverage

Kenyan foreign-exchange reference data covering multiple currencies. The rates are not city-specific and should be associated with the Kenyan reference market, not individual cities.

## Update frequency

Daily. The CBK describes the rates as reflecting average buying and selling rates of major market participants at the start of trading each day.

Exact publication time, revisions, and service-level guarantees are Unknown.

## Historical availability

The CBK website provides historical datasets dating back to 2001. Confirm the availability and completeness of the particular currency/date range required before ingestion.

## Identifiers

- **Currency:** Currency name/code shown in the published table.
- **Date:** The published date; examples are displayed in day/month/year format.
- **Rate fields:** Mean, buy, and sell.
- **Stable observation identifier:** Unknown. Use the source date and currency as a provisional natural key, after verifying whether duplicate or revised observations can occur.

## Timestamp semantics

The published observation is date-based. The exact time of publication and timezone are Unknown.

The CBK methodology describes the rates as reflecting average buying and selling rates at the start of trading. Preserve the source date separately from ingestion time. Do not assign an invented UTC timestamp to a date-only observation.

## Units

The published table includes mean, buying, and selling rates. Confirm the direction of each quote before normalising it—for example, whether a value represents Kenyan shillings per unit of foreign currency.

Retain the original rate fields and their source labels. Do not assume that `mean` is the same as the closing rate or a live executable price.

## Rate limits

Unknown. No documented public API rate-limit policy was confirmed.

## Terms of use

- **License name:** Unknown. No explicit open-data licence was identified on the rates page checked.
- **Commercial use:** Unknown.
- **Storage:** Unknown for systematic long-term storage in a commercial product.
- **Redistribution:** Unknown, including redistribution of downloaded historical observations.
- **Required follow-up:** Review the terms applicable to the chosen downloadable dataset and obtain confirmation from CBK if commercial storage or redistribution is planned.

## Attribution

Identify the Central Bank of Kenya as the source and link to the official rates page. Confirm any additional attribution requirements before public or commercial redistribution.

## Redistribution restrictions

Do not assume that public accessibility or the ability to export historical data grants permission for commercial republication. Commercial redistribution rights remain Unknown.

## Known limitations

- Rates are indicative reference rates, not guaranteed transaction prices.
- Buying, selling, and mean rates are distinct measures and must remain distinct in the data model.
- A documented public API was not confirmed.
- Exact publication timestamps, revision semantics, and licensing permissions require further verification.
- The page's published values may not represent rates available to every customer or at every location.

## Sample request and response

**Request:** The official rates page is available at:

https://www.centralbank.go.ke/rates/forex-exchange-rates/

The page provides access to published rates and historical data, but a stable, documented API request and a successful machine-readable response were not verified during this research. No sample response is included because an actual response has not yet been captured and validated.

## Assessment

**Provisional status: Candidate — useful official Kenyan reference data; automated access and licensing need verification.**

Use this source when the requirement is for CBK's published indicative daily rates. Preserve the date and the mean/buy/sell distinctions.

Before implementation, capture a real observation, validate quote direction and export structure, and establish whether commercial storage and redistribution are permitted.

## Researched by/date

- **Research date:** 2026-10-29
- **Status:** Preliminary desk research. The live request and response acceptance criterion remains incomplete.