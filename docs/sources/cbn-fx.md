# Central Bank of Nigeria (CBN) — Foreign Exchange Rates

## Summary

The Central Bank of Nigeria (CBN) publishes foreign-exchange rate information for Nigeria, including rates associated with the Nigerian Foreign Exchange Market (NFEM). The CBN describes the NFEM rate as the official exchange rate for the day, derived using a volume-weighted average.

This source is a candidate for Nigeria's official FX reference rate. It must not be presented as a parallel-market or street-market rate.

## Owner

- **Organisation:** Central Bank of Nigeria (CBN)
- **Country:** Nigeria
- **Official rate page:** https://www.cbn.gov.ng/rates/ExchRateByCurrency.html
- **Website terms/disclaimer:** https://www.cbn.gov.ng/Legal.html

## Documentation

- **Main data page:** https://www.cbn.gov.ng/rates/ExchRateByCurrency.html
- **Terms and copyright information:** https://www.cbn.gov.ng/Legal.html
- **Public API documentation:** Unknown. The pages checked do not establish a supported public API contract.

## Domain

Foreign exchange rates and related Nigerian foreign-exchange-market statistics.

## Access method

- **Observed access method:** Official CBN website.
- **Programmatic API:** Unknown. A documented, supported public API endpoint was not established during this research.
- **Recommended initial integration approach:** Treat the published website as the source of record. Do not assume that scraping or an undocumented endpoint is a stable interface.

## Authentication

Unknown. No authentication requirements for a supported public API were established because a documented public API was not confirmed.

## Geographic coverage

Nigeria's official foreign-exchange-market reference rate.

The published data is currency/rate-oriented rather than city-specific. It should not be interpreted as a set of exchange rates for individual Nigerian cities.

## Update frequency

The CBN page publishes daily-rate information. Exact publication time, availability guarantees, and correction policy are Unknown.

## Historical availability

The CBN publishes rate information on its website. The extent, completeness, and supported programmatic retrieval of historical observations require further verification.

## Identifiers

- **Base/quote convention:** The published rate table identifies currencies and NGN-denominated rates. Confirm the exact quote convention from the selected observation before normalising it.
- **Currency identifiers:** Currency names/codes as published by the CBN.
- **Stable record identifier:** Unknown. No documented observation ID was established.

## Timestamp semantics

The CBN describes the NFEM rate as the official exchange rate for the day. The exact timestamp, timezone, market cut-off, and treatment of subsequently corrected observations are Unknown.

For ingestion, preserve the published date separately from the time at which the data was retrieved. Do not invent a time-of-day timestamp if the source only supplies a date.

## Units

The page includes NGN/USD-related rate information and market statistics, including high, low, closing and mean values and turnover. Confirm the meaning and units of each field against the actual table before ingestion.

Store the rate definition and quote convention alongside each value. Do not combine a closing rate, mean rate, or turnover measure into a single generic `rate` field without preserving its original meaning.

## Rate limits

Unknown. No documented public API rate-limit policy was confirmed.

## Terms of use

- **License name:** Unknown. The CBN legal disclaimer describes website copyright and permitted copying; it does not identify a general open-data licence for this dataset.
- **Commercial use:** Unknown. The disclaimer should not be interpreted as an unrestricted commercial-use licence.
- **Storage:** Unknown for systematic or long-term storage in a commercial data product.
- **Redistribution:** The CBN states that website content may be copied electronically or on paper if the CBN is expressly identified as the source, and that material must not be amended or distorted. Whether this permission covers commercial redistribution of a normalised historical dataset is Unknown.
- **Required follow-up:** Obtain clarification from the CBN before relying on this source for commercial redistribution or a product that republishes the data.

## Attribution

At minimum, identify the Central Bank of Nigeria as the source when displaying copied material, consistent with the CBN's published disclaimer. Confirm any additional attribution wording required for the intended use.

## Redistribution restrictions

Do not assume that permission to copy website content automatically grants permission to sell, sublicense, or redistribute a bulk historical dataset. Commercial bulk redistribution rights are Unknown and require clarification.

## Known limitations

- Represents an official NFEM reference rate, not a parallel-market rate.
- A supported public API was not confirmed.
- Publication timing, historical completeness, correction semantics, and automated-access stability remain Unknown.
- The CBN's general website disclaimer does not settle every licensing question for commercial data products.

## Sample request and response

**Request:** The official rate page is available at:

https://www.cbn.gov.ng/rates/ExchRateByCurrency.html

A stable, documented API request and a successful machine-readable response were not verified during this research. No sample response is included because an actual response has not yet been captured and validated.

## Assessment

**Provisional status: Candidate — official Nigerian reference rate; integration and licensing need further verification.**

Use this source when the product requirement explicitly calls for Nigeria's official NFEM rate. Do not label it as the parallel-market rate.

Before implementation, verify the exact fields and quote convention, capture a real observation, establish a reliable retrieval method, and clarify commercial storage and redistribution permissions.

## Researched by/date

- **Research date:** 2026-10-29
- **Status:** Preliminary desk research. The live request and response acceptance criterion remains incomplete.