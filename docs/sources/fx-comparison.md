# Foreign-Exchange Source Comparison

## Purpose

Compare candidate sources for ingesting foreign-exchange reference rates across African currencies. The comparison focuses on rate meaning, geographic and historical coverage, programmatic access, data quality, and terms of use.

A source should be selected based on the rate definition required by the product. An official central-bank rate, an indicative bank-market rate, and an aggregated mid-market rate are different measures and must not be silently substituted for one another.

## Sources assessed

| Source | Register entry | Source type | Primary use |
|---|---|---|---|
| Central Bank of Nigeria (CBN) | [cbn-fx.md](cbn-fx.md) | Central bank | Nigeria's official NFEM reference rate |
| Central Bank of Kenya (CBK) | [cbk-fx.md](cbk-fx.md) | Central bank | Kenya's indicative daily FX rates |
| Frankfurter | [frankfurter.md](frankfurter.md) | Aggregated rates API | Broad daily and historical currency coverage |

## Comparison matrix

| Criterion | CBN | CBK | Frankfurter |
|---|---|---|---|
| Rate definition | Official NFEM rate and related market statistics | Indicative daily mean, buying, and selling rates | Blended mid-market rate by default; provider-specific rates may be available |
| African currency coverage | Nigeria-focused | Kenya-focused, with multiple currencies | Multiple African currencies, including NGN, KES, EGP, ZAR, and CDF |
| City-level rates | Not established | Not established | Not a city-level feed |
| Access method | Official website | Website and historical-data/export functionality | Documented REST API |
| API authentication | Unknown; supported public API not confirmed | Unknown; supported public API not confirmed | No API key required |
| Update frequency | Daily rate information | Daily indicative rates | Generally daily; varies by provider and currency |
| Historical availability | Published history exists; completeness and retrieval method need verification | Historical datasets linked back to 2001 | Historical coverage from 1948, depending on currency/provider |
| Sample live response verified | No | No | No |
| Commercial use | Unknown; clarify with CBN | Unknown; clarify with CBK | Blended rates documented as free for commercial use; upstream terms may differ |
| Bulk storage | Requires clarification | Requires clarification | Daily caching/storage is encouraged |
| Redistribution | Permissions need clarification | Permissions need clarification | Depends on blended versus provider-specific data and applicable terms |
| Overall assessment | Candidate for official Nigerian rate | Candidate for official Kenyan reference data | Candidate for broad multi-currency ingestion |

## Official rates versus parallel-market rates

These sources must not be labelled generically as "the African exchange rate" without recording what each value represents.

- **CBN:** The NFEM rate is described by the CBN as the official rate for the day. It is not a parallel-market quote.
- **CBK:** The published values are indicative rates reflecting market participants' average buying and selling rates. They are not guaranteed transaction prices and should not be labelled parallel-market rates.
- **Frankfurter:** The default blended series is a mid-market reference rate assembled from contributing sources. It is not necessarily the official rate of a particular country and is not a parallel-market feed.

**Parallel-market coverage:** None of the three candidates has been verified as a dedicated source of parallel-market rates. If the product requires those rates, research and assess a separate source. Record its provenance, methodology, geographic scope, reliability, and redistribution permissions independently.

## Timestamp and rate normalisation

Use a common internal schema while retaining the original source fields.

Suggested logical fields:

| Field | Purpose |
|---|---|
| `source` | Stable source identifier, such as `cbn`, `cbk`, or `frankfurter` |
| `provider` | Upstream provider when applicable |
| `observation_date` | Date the rate represents |
| `retrieved_at` | Time the ingestion process fetched the observation |
| `base_currency` | Currency from which the rate is quoted |
| `quote_currency` | Currency in which the rate is expressed |
| `rate` | Normalised numeric rate |
| `rate_type` | Explicit definition, such as `official_nfem`, `indicative_mean`, `buy`, `sell`, or `mid_market` |
| `original_fields` | Source-specific fields retained for audit and reconciliation |

The schema is a proposal, not a claim that every source already supplies all these fields.

### Normalisation rules

1. Confirm the quote direction before storing a rate. For example, NGN per USD is not interchangeable with USD per NGN.
2. Preserve the original rate type. Do not collapse buy, sell, mean, closing, and mid-market observations into an indistinguishable value.
3. Preserve the source observation date separately from retrieval time.
4. Do not manufacture intraday timestamps from date-only observations.
5. Keep provider identity for aggregated feeds so that observations can be traced to their source.
6. Treat a missing observation as missing data. Do not silently forward-fill or substitute another provider's rate.
7. If rates are converted or inverted, document the calculation and retain the original observation.

## Geographic coverage

These candidates provide country/currency-level reference data, not city-specific rates.

For a country-level FX dataset, associate each currency and observation with its relevant source and rate definition. Do not create separate rates for Lagos, Nairobi, or other cities unless a separately researched source actually provides city-level observations.

Currency availability also does not imply complete continental coverage. Validate the required currencies and dates before accepting a provider as a source for a production dataset.

## Terms of use and redistribution

Licensing is a source-selection criterion, not a task to defer until after the pipeline has been built.

- **CBN:** Its website disclaimer permits certain copying with source attribution and prohibits amending or distorting the material. General commercial reuse and bulk redistribution rights remain Unknown.
- **CBK:** An explicit open-data licence and permissions for commercial storage and redistribution were not identified in the checked page.
- **Frankfurter:** Its documentation states that blended rates are free for commercial use and encourages storing daily observations. Provider-specific data remains subject to applicable upstream terms.

Before publishing a redistributed dataset, retain the relevant terms, record the decision, and obtain clarification where permissions remain Unknown.

## Recommendation

**Use Frankfurter as the initial candidate for broad, daily, multi-currency ingestion**, subject to successful live-response verification and a review of the applicable terms.

Keep CBN and CBK as country-specific reference sources when their published rate definitions are explicitly required. Do not replace their official or indicative rates with Frankfurter's blended series without recording the change in source and meaning.

This recommendation is provisional because no successful live response has yet been captured for the proposed Frankfurter request, and licensing questions remain unresolved for the central-bank sources.

## Outstanding research checklist

- [ ] Execute a real request to Frankfurter for representative African currencies and capture the HTTP status and actual response.
- [ ] Confirm quote direction, response schema, observation date, and missing-currency behaviour.
- [ ] Verify whether Frankfurter can return the required provider-specific rates for each target currency.
- [ ] Capture real observations from the CBN and CBK pages or their published downloads.
- [ ] Verify source dates, publication timing, historical completeness, and correction behaviour.
- [ ] Confirm commercial storage and redistribution permissions for each selected source.
- [ ] Research a separate parallel-market source if parallel-market coverage is a product requirement.
- [ ] Document the final source selection and the rationale for each required rate type.

## Research references

- CBN rates: https://www.cbn.gov.ng/rates/ExchRateByCurrency.html
- CBN legal disclaimer: https://www.cbn.gov.ng/Legal.html
- CBK rates: https://www.centralbank.go.ke/rates/forex-exchange-rates/
- CBK methodology: https://www.centralbank.go.ke/forex/
- Frankfurter documentation: https://frankfurter.dev/
- Frankfurter currency catalogue: https://frankfurter.dev/currencies/

## Research status

- **Research date:** 2026-10-29
- **Status:** Draft comparison; live sample verification and some licensing questions remain outstanding.