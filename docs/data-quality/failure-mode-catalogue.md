# Data Quality Failure Mode Catalogue



This document identifies potential data-quality failure modes for Africa Pulse data sources and describes how they can be detected and handled by the ingestion pipeline.



## Open-Meteo observations



### Investigation performed



A sample two-day hourly Open-Meteo response was inspected for structural consistency, missing values, plausible measurement ranges, duplicate timestamps, and chronological ordering.



Observed sample:



- 48 timestamps

- 48 temperature observations

- 48 relative humidity observations

- 48 precipitation observations

- No null values observed

- No duplicate timestamps observed

- Timestamps were in chronological order

- Temperature range observed: 24.7–28.2 °C

- Relative humidity range observed: 74–95%

- Precipitation range observed: 0.0–3.1 mm



An invalid-coordinate request using latitude `999` was also tested. Open-Meteo rejected the request because latitude must be within the valid geographic range.



## Failure Modes



_To be completed as the investigation continues.




## Failure Modes

_To be completed as the investigation continues.





## Failure Modes

### 1. Invalid geographic coordinates

**Source:** Open-Meteo

**Failure:** A request may contain latitude or longitude values outside valid geographic bounds.

**Real-data observation:** An Open-Meteo request using latitude `999` returned an error stating that latitude must be between -90 and 90 degrees.

**Detection:**
- Validate latitude is between -90 and 90.
- Validate longitude is between -180 and 180.
- Check the API response status and expected response schema before processing.

**Handling:**
- Reject invalid coordinates before ingestion.
- Do not treat API error responses as weather observations.
- Log the rejected request and reason for investigation.

### 2. API authentication failure

**Source:** OpenAQ

**Failure:** Requests can fail when the API key is missing, invalid, expired, or incorrectly configured.

**Real-data observation:** A request without an OpenAQ API key returned `401 Unauthorized`. A request using an invalid credential returned an `Invalid credentials` response.

**Detection:**
- Check HTTP status codes before parsing measurements.
- Validate that the response contains the expected measurement schema rather than an authentication error.

**Handling:**
- Do not ingest the response as air-quality data.
- Log the authentication failure without exposing credentials.
- Alert operators when authentication failures persist.
- Do not automatically retry indefinitely when credentials are invalid.

### 3. Stale observations

**Source:** OpenAQ

**Failure:** The latest available measurement for a sensor may be old and therefore unsuitable for current-state analysis.

**Real-data observation:** A five-record response from the OpenAQ `latest` endpoint contained observation timestamps from 2021, 2022, 2024, 2025, and 2026.

**Detection:**
- Compare each observation timestamp with ingestion time.
- Calculate the age of each measurement.
- Define a freshness threshold appropriate to the dataset.

**Handling:**
- Flag observations older than the configured freshness threshold.
- Preserve stale observations when useful for historical analysis.
- Exclude or clearly label stale records in current-state analytics.

### 4. Missing or null measurements

**Source:** Open-Meteo and OpenAQ

**Failure:** Required measurements or metadata may be missing or null.

**Real-data observation:** No null values were found in the Open-Meteo sample or the five-record OpenAQ sample inspected during this investigation. The check demonstrates how missing values can be detected, but no missing-value failure was observed in these samples.

**Detection:**
- Check required fields for null or missing values.
- Validate required measurements before transformation.

**Handling:**
- Quarantine records missing critical fields.
- Preserve explicitly nullable fields when allowed by the schema.
- Record the reason a record failed validation.

### 5. Duplicate observations

**Source:** Open-Meteo and OpenAQ

**Failure:** Repeated API retrieval or upstream delivery can result in the same observation being processed more than once.

**Real-data observation:** No duplicate timestamps were found in the inspected Open-Meteo sample. No duplicate `(sensor ID, timestamp)` pairs were found among the five inspected OpenAQ records.

**Detection:**
- Define a deterministic observation key.
- For OpenAQ, compare combinations such as sensor ID and observation timestamp.
- Detect repeated keys before loading curated data.

**Handling:**
- Deduplicate records using the defined observation key.
- Keep raw records when required for auditability.
- Ensure retries do not create duplicate curated records.

### 6. Out-of-range or implausible values

**Source:** Open-Meteo and OpenAQ

**Failure:** Measurements can be structurally valid while containing impossible or suspicious values.

**Real-data observation:** The inspected Open-Meteo sample contained temperatures from 24.7 to 28.2 °C, relative humidity from 74% to 95%, and precipitation from 0.0 to 3.1 mm. These values passed the basic plausibility checks used during the investigation.

**Detection:**
- Apply domain-specific range rules.
- Require relative humidity to remain between 0% and 100%.
- Reject negative precipitation values.
- Apply appropriate plausibility thresholds to other measurements.

**Handling:**
- Flag or quarantine physically impossible values.
- Preserve suspicious values separately when they require investigation.
- Avoid silently changing measurements without an explicit correction policy.

### 7. Observation-array misalignment

**Source:** Open-Meteo

**Failure:** Parallel arrays such as timestamps, temperature, humidity, and precipitation can become misaligned if their lengths differ.

**Real-data observation:** The inspected Open-Meteo response contained 48 timestamps, 48 temperature values, 48 humidity values, and 48 precipitation values, so the sample passed the alignment check.

**Detection:**
- Compare the lengths of all hourly observation arrays before combining them into records.

**Handling:**
- Reject or quarantine responses containing inconsistent array lengths.
- Do not silently truncate arrays because this could associate measurements with the wrong timestamps.



### 8. Incorrect assumptions about API result ordering

**Source:** OpenAQ

**Failure:** A pipeline may incorrectly assume that the first page returned by a measurements endpoint contains the newest observations.

**Real-data observation:** A request for 100 measurements from OpenAQ sensor `23735` returned records in ascending chronological order from `2017-09-22T11:00:00Z` to `2017-09-28T09:00:00Z`. The same sensor had a latest observation dated `2026-10-04`. This demonstrates that retrieving the first page of measurements without an appropriate time filter does not necessarily retrieve the newest observations.

**Detection:**
- Inspect the minimum and maximum timestamps returned by each query.
- Compare measurement timestamps with the requested time window.
- Do not infer freshness from API pagination position.

**Handling:**
- Specify appropriate date/time filters when retrieving recent observations.
- Follow the API's documented pagination and ordering behavior.
- Validate the returned timestamp range before treating data as current.



### 9. Late or out-of-order observations

**Source:** OpenAQ

**Failure:** Observation arrival order may differ from measurement event-time order when upstream providers report data late.

**Real-data observation:** The 100-record sensor sample inspected during this investigation was chronologically ordered and contained no duplicate timestamps. Therefore, an out-of-order occurrence was not observed in that sample. However, the ingestion design must not assume that arrival order always equals measurement-time order.

**Detection:**
- Track both observation/event time and ingestion time.
- Compare new observations with the latest event time already processed for each sensor.
- Flag observations arriving outside the expected ordering or lateness window.

**Handling:**
- Accept valid late-arriving observations within an explicit lateness policy.
- Insert or update them according to event time rather than arrival position.
- Do not discard a valid measurement solely because it arrived late.




### 10. Successful HTTP response with an empty dataset

**Source:** OpenAQ

**Failure:** An API request can succeed at the HTTP level while returning no observations. Checking only for HTTP `200 OK` can therefore cause a pipeline to incorrectly treat an empty response as a successful data ingestion.

**Real-data observation:** A request for measurements from non-existent sensor ID `999999999` returned HTTP `200 OK`, but the response metadata reported `found: 0` and the `results` array was empty.

**Detection:**
- Check the HTTP status code.
- Validate the expected response schema.
- Check the number of returned observations.
- Treat an empty `results` array separately from a populated successful response.

**Handling:**
- Do not create measurement records from an empty response.
- Log the sensor or query that produced no observations.
- Distinguish a legitimate no-data condition from API, authentication, or parsing failures.
- Alert or investigate if an expected active source repeatedly returns no data.


### 11. API rate limiting

**Source:** OpenAQ

**Failure:** A pipeline that sends requests faster than the provider permits can exhaust its API request allowance and may be throttled or rejected.

**Real-data observation:** OpenAQ responses inspected during this investigation included rate-limit metadata such as `X-Ratelimit-Limit`, `X-Ratelimit-Used`, `X-Ratelimit-Remaining`, and `X-Ratelimit-Reset`. One observed response reported a limit of 60, with 59 requests remaining after the request.

**Detection:**
- Monitor HTTP status codes and rate-limit response headers.
- Track the remaining request allowance when the provider exposes it.
- Detect repeated throttling responses.

**Handling:**
- Reduce unnecessary API calls.
- Respect provider rate limits and reset periods.
- Apply bounded retry with backoff for retryable throttling responses.
- Avoid aggressive immediate retries that further exhaust the request allowance.



### 12. Schema drift or missing required fields

**Source:** Open-Meteo and OpenAQ

**Failure:** An upstream provider may change, remove, rename, or restructure fields expected by the ingestion pipeline.

**Detection:**
- Validate every response against the expected schema.
- Check required fields before transformation.
- Monitor validation failures after upstream API changes.

**Handling:**
- Quarantine responses that do not satisfy the required schema.
- Log which fields are missing or incompatible.
- Version schemas when intentional upstream changes are adopted.
- Do not silently map unknown structures into curated data.



### 13. Unit inconsistency or unexpected unit changes

**Source:** Open-Meteo and OpenAQ

**Failure:** A measurement may be interpreted incorrectly if the pipeline assumes a unit instead of validating the unit supplied by the source. Upstream unit changes or inconsistent units can also make otherwise valid numeric values misleading.

**Detection:**
- Validate measurement units against the expected unit for each parameter.
- Store the unit together with the measurement where appropriate.
- Detect unexpected changes in units before transformation.

**Handling:**
- Convert supported units explicitly into the canonical unit used by the pipeline.
- Quarantine measurements with unsupported or unknown units.
- Never perform silent unit conversion without a defined conversion rule.



### 14. Timestamp and time-zone ambiguity

**Source:** Open-Meteo and OpenAQ

**Failure:** Incorrect interpretation of timestamps or time zones can associate measurements with the wrong hour, day, or reporting period.

**Real-data observation:** The Open-Meteo sample returned hourly timestamps such as `2026-10-07T00:00`, while OpenAQ records inspected during the investigation included explicit UTC timestamps such as `2026-10-04T00:00:00Z`. The different timestamp representations demonstrate why the pipeline should not assume that all sources express time identically.

**Detection:**
- Validate timestamp format before ingestion.
- Check whether timezone information or a UTC offset is present.
- Normalize event timestamps before comparing records from different sources.

**Handling:**
- Convert timestamps to a canonical timezone such as UTC for storage and comparison.
- Preserve original source timestamps when useful for traceability.
- Quarantine timestamps that cannot be parsed or safely interpreted.