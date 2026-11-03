# GDELT

> Documentation and terms checked on 2026-11-02. Volume figures, geocoding observations and the sample response come from the GDELT 2.0 Event export files for 26 October to 1 November 2026 (672 files, every 15-minute file in that UTC week, none missing) and from requests to the DOC 2.0 API, made on 2026-11-02. Method notes are given with each figure.

## Summary

GDELT (Global Database of Events, Language, and Tone) monitors print, broadcast and web news worldwide, machine-codes the events, actors, locations and tone described in each article, and publishes the result every 15 minutes ([About](https://www.gdeltproject.org/about.html), [GDELT 2.0](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/)). For Africa Pulse it is a candidate signal for news and public events in cities. It measures media coverage of events, not the events themselves, and its city geocoding has known errors, so it needs strong quality rules before use.

## Owner

The GDELT Project, created by Kalev H. Leetaru ([About](https://www.gdeltproject.org/about.html)). GDELT codes articles published by third-party news outlets; it distributes coded records and article URLs, not article text ([Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf), field `SOURCEURL`).

## Documentation

- Main documentation URL: https://www.gdeltproject.org/data.html
- API reference URL: DOC 2.0 API, https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/ ; GEO 2.0 API, https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/
- Event file format: https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf
- Global Knowledge Graph format: https://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.pdf
- Terms of use URL: https://www.gdeltproject.org/about.html#termsofuse

## Domain

News & public events

## Access method

GDELT has no single API. The routes relevant to Africa Pulse are:

- **Raw 15-minute files (recommended for a connector).** Event 2.0, Mentions and GKG 2.0 tables are each written every 15 minutes ([Data](https://gdeltproject.org/data.html), [Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf)). `http://data.gdeltproject.org/gdeltv2/lastupdate.txt` lists the newest files, and a master file list covers all files ([GDELT 2.0](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/)). Each file is a ZIP holding one tab-delimited CSV; the Event export has 61 columns (observed in all 672 files fetched for this entry). Each line of `lastupdate.txt` gives file size in bytes, MD5 checksum and URL (observed, see Sample request and response).
- **DOC 2.0 API.** `https://api.gdeltproject.org/api/v2/doc/doc` returns article lists and volume or tone timelines for a keyword query, in HTML, CSV, JSON, RSS and other formats ([DOC 2.0](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)).
- **GEO 2.0 API.** `https://api.gdeltproject.org/api/v2/geo/geo` maps locations mentioned near a keyword over the last 15 minutes to 7 days, with GeoJSON output ([GEO 2.0](https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/)).
- **Google BigQuery.** All GDELT datasets are in BigQuery and the live ones update every 15 minutes ([Data](https://gdeltproject.org/data.html)). BigQuery usage is billed by Google under the user's own account.
- **AWS S3.** Bucket `gdelt-open-data` (us-east-1) is listed as "Not currently being updated" ([AWS Open Data Registry](https://registry.opendata.aws/gdelt/)) and is not suitable for current data.

## Authentication

None for raw files, the DOC API or the GEO API. No key or registration was needed for any request made for this entry. BigQuery access needs a Google Cloud account ([Data](https://gdeltproject.org/data.html)).

## Geographic coverage

- Global. GDELT monitors news "from nearly every corner of every country" in more than 100 languages ([About](https://www.gdeltproject.org/about.html)); 65 languages are machine-translated to English in real time ([GDELT 2.0](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/)).
- Coverage of a place depends on how much the monitored media write about it, not on any sensor network. See "Media-coverage bias" under Known limitations for measured figures for the five target cities.
- Location is specified per event by three geography blocks (Actor1, Actor2, Action), each with `Geo_Type`, `Geo_FullName`, `Geo_CountryCode` (FIPS 10-4), `Geo_ADM1Code`, `Geo_ADM2Code`, `Geo_Lat`, `Geo_Long` and `Geo_FeatureID` ([Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf)). Africa Pulse should use the Action block, which records where the event took place.

### How GDELT geocodes events to cities

- GDELT uses fulltext geocoding: it scans the article text for place names and matches them against a gazetteer, the U.S. GEOnet Names Server (GNS) for places outside the U.S. Ambiguous names are resolved by checking whether the containing country or division is also mentioned, and larger places score higher: "Capitals and large cities usually receive a very high score" ([Leetaru 2012, D-Lib Magazine](https://dlib.org/dlib/september12/leetaru/09leetaru.html)). The GEO API describes a gazetteer of more than 9 million places down to remote landmarks ([GEO 2.0](https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/)).
- For each event, the place reference closest to the action in the text is encoded, and a match is not always found ([Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf)).
- `ActionGeo_Type` gives the match level: 1 country, 2 U.S. state, 3 U.S. city or landmark, 4 city or landmark outside the U.S., 5 first-order administrative division outside the U.S. City-level matches (types 3 and 4) carry the signed numeric GNS `FeatureID`; latitude and longitude are "the centroid" of the matched place ([Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf)).
- City events therefore resolve to a single point per gazetteer feature. Observed: all 1,882 type-4 "Lagos, Lagos, Nigeria" events in the sample week have FeatureID `-2017355` and the same coordinates, 6.45306, 3.39583 (Lagos Island). GDELT cannot place an event within a city beyond the named sub-places in the gazetteer.
- Observed target-city feature IDs (type 4, week of 26 Oct to 1 Nov 2026): Lagos `-2017355`, Nairobi `-2258072` ("Nairobi, Nairobi Area, Kenya"), Cairo `-290692` ("Cairo, Al Qahirah, Egypt"), Johannesburg `-1240261` ("Johannesburg, Gauteng, South Africa"), Kinshasa `-2049111` ("Kinshasa, Kinshasa, Democratic Republic Of The Congo").

### Reliability of city geocoding for African cities

- GDELT itself states that geocoding errors are common: a city confused with a namesake, a mistranslated place name, or unrelated text assigned to the wrong place ([GEO 2.0](https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/)).
- A peer-reviewed comparison of GDELT with hand-coded conflict data found only moderate agreement and serious geographic bias at the local level, and advised caution for sub-national research ([Hammond and Weidmann 2014, Research & Politics, doi:10.1177/2053168014539924](https://kops.uni-konstanz.de/entities/publication/cd1512fc-1853-4302-9829-cb83f47cbbcb)). The geocoding paper reports no Africa-specific accuracy figures and notes transliteration problems in African place names ([Leetaru 2012](https://dlib.org/dlib/september12/leetaru/09leetaru.html)).
- Observed false matches in Lagos State (ADM1 `NI05`), week of 26 Oct to 1 Nov 2026:
  - 447 events geocoded to "Tinubu, Lagos, Nigeria" (FeatureID `-2027738`, 6.51667, 3.36667). Inspected records were national stories (fuel prices, a court ruling on an Imo State Senate ticket) in which "Tinubu" is the President's surname, matched to a Lagos place of the same name. That is 24% of the 1,882 events placed on Lagos itself.
  - 22 events geocoded to "Hausa, Lagos, Nigeria", an ethnic-group name matched to a place.
- Observed correct sub-city matches in the same week: Ikeja 93, Ikorodu 49, Victoria Island 36, Apapa 27, Lagos Island 20, Shomolu 11, Igando 11, Ikotun 10, Ebute Metta 9, Agege 7 events; "Lagos State, Lagos, Nigeria" (type 5) 383 events.
- No event named "Lagos" was geocoded outside Nigeria in the sample week, so city-name collision was not observed for Lagos.
- Conclusion: country and city-name matching is usable for large African cities, but event counts at city level include systematic false positives from person and group names, and every event in a city shares one centroid. City-level counts should be treated as an indicator of media attention, filtered for known false features, and never presented as precise event locations.

## Update frequency

- Event 2.0, Mentions and GKG 2.0 files are published every 15 minutes ([Data](https://gdeltproject.org/data.html)); news is processed within 15 minutes of being monitored ([GDELT 2.0](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/)). All 672 15-minute export files for 26 Oct to 1 Nov 2026 were present when fetched on 2026-11-02.
- Delay between the real-world event and its first appearance in GDELT depends on when it is reported; GDELT records when it added the record (`DATEADDED`), not when the event happened to the minute (see Timestamp semantics). Typical reporting lag for African events: **Unknown**, no figure in [Data](https://gdeltproject.org/data.html), [GDELT 2.0](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/) or the [Event Codebook](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf).
- DOC and GEO API maps and timelines update every 15 minutes ([GEO 2.0](https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/)).

### Daily volume estimate: Lagos

Method: every Event 2.0 export file from 2026-10-26 00:00 to 2026-11-01 23:45 UTC (Monday to Sunday, 672 files) was read, and rows were counted where `ActionGeo_Type` = 4, `ActionGeo_CountryCode` = `NI` and `ActionGeo_FullName` begins with "Lagos". Days are UTC days of `DATEADDED`.

| UTC day | Lagos events | Distinct source URLs | All GDELT events |
|---|---|---|---|
| Mon 2026-10-26 | 252 | 88 | 108,055 |
| Tue 2026-10-27 | 331 | 105 | 119,106 |
| Wed 2026-10-28 | 364 | 128 | 123,196 |
| Thu 2026-10-29 | 294 | 99 | 118,962 |
| Fri 2026-10-30 | 232 | 77 | 114,106 |
| Sat 2026-10-31 | 217 | 61 | 73,394 |
| Sun 2026-11-01 | 192 | 65 | 63,401 |
| **Total** | **1,882** | **623** | **720,220** |

- Estimate: about 270 city-level events per day for Lagos (range 192 to 364), coded from about 90 distinct articles per day, so roughly 3 event records per article. Weekdays averaged 295 events and the weekend 205, following the global weekly cycle.
- Volume shifts with the news cycle, not with what happens in the city: on 1 Nov 2026 the event-type mix for Lagos was mostly statements and consultations (CAMEO root codes 04 Consult 31, 01 Make public statement 28, 11 Disapprove 23, 02 Appeal 23).
- Comparison, same week, city-level events per day: Nairobi 104 to 312, Cairo 66 to 411, Johannesburg 66 to 196, Kinshasa 3 to 23.

## Historical availability

- GDELT 2.0 data begins on 19 February 2015 ([GDELT 2.0](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/)); all 15-minute files are listed in the master file list and remain downloadable through the same route.
- GDELT 1.0 reduced event data covers 1 January 1979 to 17 February 2014 and is no longer updated ([Data](https://gdeltproject.org/data.html)). It uses a different format and was not assessed here.
- DOC 2.0 API searches a rolling window, three months by default, with `startdatetime` / `enddatetime` limited to that window ([DOC 2.0](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)); a later update extended searching to 1.5 years ([DOC 2.0 updates](https://blog.gdeltproject.org/doc-2-0-updates-1-5-year-searching-and-updated-mobile-interface/)). GEO 2.0 covers at most the last 7 days ([GEO 2.0](https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/)). For history, raw files or BigQuery must be used.

## Identifiers

- `GlobalEventID`: unique identifier for each event record. GDELT warns that IDs are often sequential with date but "this is NOT always the case", so they must not be used for ordering ([Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf)). Whether IDs survive reprocessing: **Unknown**, not stated in the [Event Codebook](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf), [Data](https://gdeltproject.org/data.html) or [GDELT 2.0](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/).
- Locations: `Geo_FeatureID` is the GNS feature ID for city-level matches (signed integer as text, e.g. `-2017355` for Lagos) and a textual country or ADM1 code otherwise; `Geo_ADM1Code` is the FIPS 10-4 country code plus FIPS 10-4 ADM1 code (e.g. `NI05` Lagos State); `Geo_ADM2Code` is a GAUL code for places outside the U.S. ([Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf)).
- Country codes in geography fields are FIPS 10-4, not ISO 3166: Nigeria `NI`, Kenya `KE`, Egypt `EG`, South Africa `SF`, DR Congo `CG` (observed in the sample files). Actor country codes are 3-character CAMEO codes ([Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf)). A crosswalk to Africa Pulse canonical city and country keys is required.
- Articles: `SOURCEURL` holds the first report's URL ([Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf)). Files: the 15-minute timestamp in each file name (e.g. `20261101140000.export.CSV.zip`).

## Timestamp semantics

- What time does each timestamp represent:
  - `Day` (YYYYMMDD), with `MonthYear`, `Year` and `FractionDate` derived from it: the date the event took place, as coded from the article ([Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf)). It can differ from the publication date. Observed on 1 Nov 2026: 975 of 63,401 records (1.5%) had a `Day` different from the date in `DATEADDED`, including a Lagos record added on 2026-11-01 with `Day` 2025-11-01.
  - `DATEADDED` (YYYYMMDDHHMMSS): when the event was added to the GDELT database, at 15-minute resolution; GDELT advises this field for 15-minute queries ([Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf)). Observed: `DATEADDED` always equals the timestamp in the file name.
  - Mentions table: records each later mention of an event with the article's publication timestamp ([GDELT 2.0](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/)).
- Which time zone: `DATEADDED` is UTC ([Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf)). Time zone of `Day`: **Unknown**, the codebook gives no zone. DOC API timeline dates are returned with a `Z` suffix, e.g. `20261027T050000Z` (observed); the time zone of `startdatetime` / `enddatetime` inputs is not stated ([DOC 2.0](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)): **Unknown**.
- Granularity: `Day` is daily; `DATEADDED` is 15-minute. DOC API timelines use 15-minute steps for spans under 72 hours, hourly steps up to one week and daily steps beyond ([DOC 2.0](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)).

## Units

| Field | Unit / scale | Source |
|---|---|---|
| `NumMentions`, `NumSources`, `NumArticles` | Counts, measured only in the 15-minute update where the event was first seen | [Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf) |
| `AvgTone` | Dimensionless score, -100 (extremely negative) to +100 (extremely positive); usually -10 to +10, 0 neutral | [Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf) |
| `GoldsteinScale` | -10 to +10, a fixed score per CAMEO event code, not per event | [Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf) |
| `QuadClass` | Category 1 to 4: verbal cooperation, material cooperation, verbal conflict, material conflict | [Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf) |
| `EventCode`, `EventBaseCode`, `EventRootCode` | CAMEO codes, kept as strings (leading zeros matter, e.g. `04`) | [Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf) |
| `Geo_Lat`, `Geo_Long` | Decimal degrees, centroid of the matched place; datum **Unknown**, not stated in the codebook | [Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf) |
| DOC API `timelinevol` | Percent of all monitored coverage | [DOC 2.0](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/) |
| DOC API `timelinevolraw` | Article count, with `norm` = total monitored articles in the step | [DOC 2.0](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/) |

No currency or physical units are involved.

## Rate limits

- Raw files: no rate limit is documented: **Unknown**, checked [Data](https://gdeltproject.org/data.html), [GDELT 2.0](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/) and [About](https://www.gdeltproject.org/about.html). Fetching 672 files with 8 parallel requests on 2026-11-02 met no throttling (observed). Each Event export file is small (80,200 bytes zipped for the 20:30 UTC file on 2026-11-02, from `lastupdate.txt`); a GKG file was 7,007,475 bytes.
- DOC 2.0 API: no numeric limit is given in the API documentation ([DOC 2.0](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)). Observed on 2026-11-02: article-list requests returned a plain-text notice, "Please limit requests to one every 5 seconds", instead of data, even with 9-second gaps between requests; the notice directs high-traffic users to GDELT's web ngrams dataset. A 7-day `timelinevolraw` request for "Lagos" returned a single hourly value. The DOC API is therefore not reliable enough to be a connector's primary route.
- `maxrecords` on the DOC API: default 75, maximum 250 ([DOC 2.0](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)). GEO API `maxpoints` up to 1,000 ([GEO 2.0](https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/)).
- BigQuery: subject to Google Cloud quotas and billing ([Data](https://gdeltproject.org/data.html)).

## Terms of use

- License: GDELT Project Terms of Use. GDELT does not use a standard named license such as CC BY; the AWS registry lists the license as the Terms of Use page itself ([AWS Open Data Registry](https://registry.opendata.aws/gdelt/)). The terms state that all GDELT datasets are "available for unlimited and unrestricted use for any academic, commercial, or governmental use of any kind without fee" ([About, Terms of Use](https://www.gdeltproject.org/about.html#termsofuse)).
- Commercial use permitted? Yes, explicitly ([About, Terms of Use](https://www.gdeltproject.org/about.html#termsofuse)).
- Storage permitted? The terms do not mention storage as such, but they allow GDELT data to be rehosted and mirrored "in any form" ([About, Terms of Use](https://www.gdeltproject.org/about.html#termsofuse)), which requires storing it. Storing GDELT records is therefore permitted. This does not extend to the news articles behind each `SOURCEURL`, which belong to their publishers and are not GDELT datasets.
- Redistribution permitted? Yes, with citation (see Attribution requirements) ([About, Terms of Use](https://www.gdeltproject.org/about.html#termsofuse)).

## Attribution requirements

Any use or redistribution "must include a citation to the GDELT Project and a link to this website (https://www.gdeltproject.org/)" ([About, Terms of Use](https://www.gdeltproject.org/about.html#termsofuse)). GDELT prescribes no fixed wording. Proposed form for Africa Pulse outputs: "Event data: The GDELT Project (https://www.gdeltproject.org/)."

## Redistribution restrictions

- Africa Pulse may redistribute raw and derived GDELT records, including rehosting and mirroring, provided each use cites the GDELT Project with a link ([About, Terms of Use](https://www.gdeltproject.org/about.html#termsofuse)).
- Article text is out of scope: GDELT distributes URLs only. Fetching, storing or republishing the linked articles would fall under each publisher's own terms, not GDELT's.
- No bulk GDELT data is committed to this repository; the figures in this entry are aggregates and two trimmed sample records, in line with [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Known limitations

### Media-coverage bias

GDELT counts what the monitored media report. Places, topics and days with more coverage produce more events, regardless of what actually happens.

- Coverage is concentrated outside Africa. On Sunday 1 Nov 2026, 17,072 of 63,401 events (27%) were geocoded to the United States (FIPS `US`), against 2,551 (4.0%) for Nigeria, 675 for South Africa, 453 for Kenya, 311 for Egypt and 25 for DR Congo (observed, `ActionGeo_CountryCode`).
- Coverage within Africa does not follow population. In the sample week Kinshasa had 3 to 23 city-level events per day, against 66 to 196 for Johannesburg and 192 to 364 for Lagos (observed). A low count for a city means low coverage in the monitored sources, not an absence of events.
- Volume follows the news week: the global total fell from 108,055 to 123,196 events per weekday to 63,401 to 73,394 at the weekend (observed), and Lagos followed the same pattern.
- GDELT's total monitored volume changes over time, so raw counts must be normalised; the DOC API provides `norm` totals for this purpose ([DOC 2.0](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)).
- Coding errors are frequent: a study of GDELT protest events found only 21% referred to real protests ([Wang et al. 2016, Science 353(6307):1502](https://news.northeastern.edu/2016/09/29/study-using-big-data-to-monitor-societal-events-shows-promise-but-the-coding-tech-needs-work)). Observed example: a 1 Nov 2026 Lagos record coded as a demonstration (CAMEO `141`, `IsRootEvent` 1) came from an article in which a cleric recalled protesting during a past presidency, not a current protest.
- Stories are counted more than once: about 3 event records per distinct article for Lagos in the sample week (1,882 events from 623 URLs).

### Other limitations

- City geocoding errors and single-centroid placement (see Reliability of city geocoding).
- `NumMentions`, `NumSources`, `NumArticles` and `IsRootEvent` reflect only the 15-minute update where an event was first seen; the Mentions table must be used to follow later coverage ([Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf)).
- `GoldsteinScale` describes the event type, not the size of a specific event ([Event Codebook V2.0](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf)).
- Machine translation from 65 languages adds a further error source to geocoding and coding ([GEO 2.0](https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/)).
- The DOC API throttled or returned near-empty results during testing (see Rate limits).
- The AWS S3 copy is not being updated ([AWS Open Data Registry](https://registry.opendata.aws/gdelt/)).

## Sample request and response

Requests made on 2026-11-02. No key is required. GDELT terms permit redistribution with citation, so trimmed response data is included. Source: The GDELT Project (https://www.gdeltproject.org/).

```bash
# 1. Find the newest 15-minute files
curl -s http://data.gdeltproject.org/gdeltv2/lastupdate.txt

# 2. Download one Event export file and keep rows placed on Lagos (ActionGeo_FullName is column 53)
curl -s -o events.zip http://data.gdeltproject.org/gdeltv2/20261101140000.export.CSV.zip
unzip -p events.zip | awk -F'\t' '$52 == 4 && $53 == "Lagos, Lagos, Nigeria"' | head -2
```

Response to request 1 (complete, three lines: size in bytes, MD5, URL):

```text
80200 c1781a77025f26f90d1c2c7b03861a25 http://data.gdeltproject.org/gdeltv2/20261102203000.export.CSV.zip
132100 fd75cc98832085cb6f7269583b9b984d http://data.gdeltproject.org/gdeltv2/20261102203000.mentions.CSV.zip
7007475 61d6aa1b81623fa3eabcd4f5bce7cf78 http://data.gdeltproject.org/gdeltv2/20261102203000.gkg.csv.zip
```

Response to request 2, trimmed to two records and 22 of 61 columns, with codebook column names added (the file itself has no header row):

```json
[
  {
    "GlobalEventID": "1330935133",
    "Day": "20261101",
    "Actor1Name": "",
    "Actor2Name": "PRESIDENT",
    "IsRootEvent": "1",
    "EventCode": "141",
    "EventRootCode": "14",
    "QuadClass": "3",
    "GoldsteinScale": "-6.5",
    "NumMentions": "4",
    "NumSources": "1",
    "NumArticles": "4",
    "AvgTone": "-1.70015455950541",
    "ActionGeo_Type": "4",
    "ActionGeo_FullName": "Lagos, Lagos, Nigeria",
    "ActionGeo_CountryCode": "NI",
    "ActionGeo_ADM1Code": "NI05",
    "ActionGeo_Lat": "6.45306",
    "ActionGeo_Long": "3.39583",
    "ActionGeo_FeatureID": "-2017355",
    "DATEADDED": "20261101140000",
    "SOURCEURL": "https://thesun.ng/why-i-carried-placard-hit-the-streets-during-jonathans-presidency-adeboye/"
  },
  {
    "GlobalEventID": "1330935268",
    "Day": "20261101",
    "Actor1Name": "CHRISTIAN CHURCH",
    "Actor2Name": "GOODLUCK JONATHAN",
    "IsRootEvent": "1",
    "EventCode": "120",
    "EventRootCode": "12",
    "QuadClass": "3",
    "GoldsteinScale": "-4.0",
    "NumMentions": "3",
    "NumSources": "1",
    "NumArticles": "3",
    "AvgTone": "-1.18460019743337",
    "ActionGeo_Type": "4",
    "ActionGeo_FullName": "Lagos, Lagos, Nigeria",
    "ActionGeo_CountryCode": "NI",
    "ActionGeo_ADM1Code": "NI05",
    "ActionGeo_Lat": "6.45306",
    "ActionGeo_Long": "3.39583",
    "ActionGeo_FeatureID": "-2017355",
    "DATEADDED": "20261101140000",
    "SOURCEURL": "https://www.premiumtimesng.com/entertainment/naija-fashion/921882-i-didnt-protest-against-jonathan-adeboye-clarifies.html"
  }
]
```

The first record is the demonstration false positive described under Media-coverage bias.

DOC 2.0 API request tried for comparison:

```bash
curl -s "https://api.gdeltproject.org/api/v2/doc/doc?query=Lagos%20sourcecountry:nigeria&mode=artlist&maxrecords=3&format=json&sort=datedesc"
```

On 2026-11-02 this returned the plain-text rate-limit notice described under Rate limits, not JSON.

## Assessment

GDELT is a usable but noisy source for Africa Pulse's news and public-events domain. In its favour: open terms that allow commercial use, storage and redistribution with citation; no authentication; 15-minute updates; history back to 2015 through the same file route; and enough volume for large African cities (about 270 events per day for Lagos).

Risks:

1. **It measures coverage, not events.** Counts must be labelled as media-attention indicators and normalised against total volume. They must not be presented as event counts.
2. **City geocoding.** One centroid per city and systematic false matches (24% extra on Lagos from "Tinubu" in the sample week). The connector should keep `ActionGeo_FeatureID`, and quality rules should flag or exclude known false features per city.
3. **Uneven African coverage.** Kinshasa produced too few events per day for a stable signal; the register should mark low-coverage cities rather than show near-zero values as real quiet.
4. **Coding errors and duplication.** About 3 records per article, and historical references coded as current events. Deduplication by `SOURCEURL` and event-type filtering are needed before any mart.
5. **Access route.** The DOC API throttled during testing; the connector should use the 15-minute raw files, check the MD5 in `lastupdate.txt`, and record the file name as provenance.
6. **Code systems.** FIPS 10-4 country codes and CAMEO codes need crosswalks to Africa Pulse canonical keys.

## Researched by

@Oyetoluzeenat. Documentation and terms of use checked on 2026-11-02. Event files for 2026-10-26 to 2026-11-01 and DOC API requests fetched on 2026-11-02.
