# OpenStreetMap (via Overpass API)

## Summary

OpenStreetMap (OSM) is a collaboratively maintained, global geographic database of
roads, buildings, administrative boundaries, and points of interest, published
under the Open Database License (ODbL). For Africa Pulse it is the primary source
of **geospatial and reference data** — city and neighbourhood boundaries,
administrative geographies, the road network, and place/infrastructure points of
interest — which act as the spatial backbone that every other source
(weather, air quality, mobility, FX, events) is joined to. Without a stable
geographic key, per-city signals from different sources cannot be compared.

Data is read through the **Overpass API**, a read-only query service over the
OSM database.

## Owner

OpenStreetMap is built and maintained by the OpenStreetMap Foundation (OSMF) and
its global community of volunteer contributors. There is no single corporate
owner and no formal support contract.

- OSMF: https://osmfoundation.org/
- Community/contributors: https://www.openstreetmap.org/

The Overpass API software is an independent community project, authored and
maintained by Roland Olbricht, licensed GNU AGPL v3.

- Overpass API source: https://github.com/drolbr/Overpass-API

## Documentation

- Main documentation URL: https://www.openstreetmap.org/
- API reference URL: https://wiki.openstreetmap.org/wiki/Overpass_API
  - Overpass API language reference: https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL
  - Overpass API user's manual: https://dev.overpass-api.de/overpass-doc/en/
  - OSM data model (elements): https://wiki.openstreetmap.org/wiki/Elements
- Terms of use URL:
  - Licence: https://www.openstreetmap.org/copyright
  - ODbL 1.0 legal code: https://opendatacommons.org/licenses/odbl/1-0/
  - OSMF Terms of Use: https://osmfoundation.org/wiki/Terms_of_Use
  - Overpass API usage/quota rules: https://dev.overpass-api.de/overpass-doc/en/preface/commons.html
  - OSMF API Usage Policy: https://operations.osmfoundation.org/policies/api/

## Domain

Commercial & geospatial. OSM is the geospatial/reference backbone rather than a
time-series signal source.

## Access method

Primarily the **Overpass API** — a read-only REST-style query API. The client
POSTs a query in Overpass QL to an interpreter endpoint and receives matching
OSM elements as XML or JSON.

- Interpreter endpoint: `https://overpass-api.de/api/interpreter` (POST `data=<query>`)
- Status endpoint (quota/slot introspection): `https://overpass-api.de/api/status`

Other access paths, for different volumes of work:

- **Main OSM editing API** (`https://api.openstreetmap.org/api/0.6/`) — *not* intended
  for read-only or bulk use; the OSMF API Usage Policy directs large/frequent read
  consumers to planet extracts or Overpass instead.
  (https://operations.osmfoundation.org/policies/api/)
- **Bulk download (recommended for bulk access):**
  - Planet: https://planet.openstreetmap.org/
  - Geofabrik regional/country extracts: https://download.geofabrik.de/
    (Africa index: https://download.geofabrik.de/africa.html)
- **Third-party hosted Overpass mirrors** — e.g. `https://overpass.kumi.systems/api/interpreter`
  (listed on the Overpass API wiki under public instances).

Scraping is not required — a documented API exists.

## Authentication

**None.** No API key, token, or OAuth is required for either Overpass or bulk
downloads. No registration and no free tier distinction: the service is free and
open to all, subject to fair-use quotas rather than credentials.
(Confirmed by fetching `https://overpass-api.de/api/interpreter` and
`https://download.geofabrik.de/` with no credentials of any kind.)

Practical caveat, observed while testing: on the instance used here
(`overpass-api.de`), requests **without a `User-Agent` header are rejected with
HTTP 406 Not Acceptable**. This is an instance-specific observation, not a
universal rule of the Overpass protocol — but regardless of instance, a
descriptive User-Agent should always be sent. The OSMF API Usage Policy requires
a "Valid User-Agent identifying application and version" and warns that "Faking
another app's User-Agent WILL get you blocked". Note that this policy governs the
OSMF **editing API**, and does not automatically bind every third-party Overpass
mirror; test the selected instance's behaviour directly.
(https://operations.osmfoundation.org/policies/api/)

## Geographic coverage

**Global, including all of Africa**, but coverage *density* varies enormously by
place. OSM has no fixed list of supported cities — anything a volunteer has mapped
exists, so African megacities such as Lagos, Accra, Nairobi, Cairo and Kinshasa are
mapped in substantial detail while smaller towns and informal settlements may be
sparse or absent. Africa Pulse must treat coverage as **uneven and unverified per
city** rather than assumed.
(Coverage varies by place because OSM is volunteer-contributed; there is no
publisher-side completeness guarantee — see
https://wiki.openstreetmap.org/wiki/Quality_assurance and
https://wiki.openstreetmap.org/wiki/Map_Features.)

A location is specified in one of three ways:

1. **Coordinates / bounding box** — `(south,west,north,east)` in decimal degrees.
   Example: `(5.55,-0.20,5.60,-0.15)` is a box in central Accra.
2. **Named area** — resolved server-side, e.g. `area["ISO3166-1"="GH"]->.gh;` selects
   Ghana, then `(area.gh)` restricts a query to it.
3. **Element ID** — a stable global id, optionally with type
   (`node`/`way`/`relation`), e.g. `relation 12803764;`.

Country-level extracts are available for every African country via Geofabrik, which
is useful as a coverage sanity check. Example `.osm.pbf` extract sizes
(as of 2026-10-09): Nigeria 677 MB, Kenya 335 MB, South Africa 402 MB,
DR Congo 397 MB, Tanzania 673 MB, Ghana 110 MB, Rwanda 64 MB, Cape Verde 11.2 MB,
Seychelles 2.6 MB. (https://download.geofabrik.de/africa.html)

## Update frequency

**Continuous / near-real-time.** OSM is edited by volunteers at all times, so the
database changes minute by minute. There is no scheduled publication window.

How quickly Africa Pulse sees an edit depends on access method:

- **Overpass**: the instance is kept current from planet minutely diffs. Each response
  carries a `timestamp_osm_base` field stating the data's currency. During testing this
  was `2026-10-11T09:06:50Z` against a server clock of `2026-10-11T09:07:40Z` — i.e.
  roughly a minute behind live.
- **Geofabrik bulk extracts**: daily. The Africa extract observed was "last modified
  1 day ago and contains all OSM data up to 2026-10-09T20:21:04Z".

So Overpass is effectively near-real-time; bulk extracts are up to ~1 day stale.

## Historical availability

**Yes, but not through Overpass for arbitrary past states.**

- **Overpass** serves the current state plus a date/date-diff filter for changesets
  (`[date:"..."]`, `[diff:"..."]`, `[adiff:"..."]`), which allows asking *what changed*
  after a given time. It is not a general "give me the map as it was on date X"
  archive for arbitrary elements.
  (https://wiki.openstreetmap.org/wiki/Overpass_API#Meta_data)
- **Full history** requires the planet history file (`africa-internal.osh.pbf`,
  the `*history*` files) or per-object history via the main API. Note Geofabrik states
  history files contain personal data and are served from their **internal server only**.
- **Geofabrik** keeps dated snapshot files, observed annually from 2014
  (`africa-140101.osm.pbf`, 440 MB) and then several times a month in recent years —
  e.g. `africa-261001.osm.pbf` (2026-10-01) and `africa-261009.osm.pbf` (2026-10-09).
  This makes coarse historical reconstruction possible but not day-by-day.

**Implication for Africa Pulse:** reprocessing a historical run against a true past
OSM state is not straightforwardly supported and should be treated as a known
limitation, not a guaranteed capability.

application is required in practice (and is explicitly required by the OSMF API
Usage Policy for the editing API: "Valid User-Agent identifying application and
version. Faking another app's User-Agent WILL get you blocked.").

## Identifiers

Every element carries a global **`id`**, combined with its **`type`** to form the
unique key. Ids are assigned sequentially at creation and should be treated as stable
type-scoped identifiers. Deletion is recorded in OSM's history; do not assume a deleted
element's id is freed for reuse — treat ids as non-recyclable application keys.

**Critical caveat:** nodes, ways and relations **do not share an id space**. The same
numeric id can refer to a node and a relation simultaneously. Any key must therefore
be `(type, id)`, never bare `id`. (https://wiki.openstreetmap.org/wiki/Elements)

Secondary metadata on each element:

- `version` — edit version, starts at 1, incremented server-side on each edit.
- `changeset` — the changeset number of the last edit.
- `user` / `uid` — display name / numeric id of the last editor. **A user may change
  their display name at any time, and existing elements silently reflect the new name
  without a version bump** — so `user` is not a stable identifier; `uid` is
  ("User identifiers never change").
- `visible` — `false` if the element is deleted.

(All four fields, their semantics, and the mutable-display-name behaviour are
specified at https://wiki.openstreetmap.org/wiki/Elements.)

Places also carry cross-reference identifiers useful for entity resolution,
e.g. `wikidata` and `wikipedia` tags — the Accra boundary relation returns
`"wikidata": "Q3761"`. These give a bridge to external knowledge graphs.

**Note on privacy-scrubbed fields:** Geofabrik's public extracts deliberately omit
usernames, user ids and changeset ids, stating these are assumed to contain personal
data subject to EU data-protection rules, with full metadata available to OSM
contributors only. Expect these fields to be absent from bulk extracts.

## Timestamp semantics

- **What the timestamp represents:** OSM's `timestamp` is the **time of the last
  modification** of that element, *not* an observation time and not a period
  start/end. There is no notion of a measurement window. A hospital node's timestamp
  means "when a mapper last touched this record", which may be years ago.
- **Time zone:** **UTC**, in W3C / ISO 8601 format with a trailing `Z`, without
  fractional seconds — e.g. `"2026-10-11T09:06:50Z"`.
- **Granularity:** one-second resolution on the element timestamp.

(Timestamp semantics — last-modified rather than observation time, UTC, and
one-second resolution — are specified at https://wiki.openstreetmap.org/wiki/Elements.)

Distinct time values Africa Pulse should keep separate:

| Field | Meaning |
|---|---|
| Element `timestamp` | last modification of that element (UTC) |
| `timestamp_osm_base` (JSON `osm3s` metadata field, not an HTTP header) | currency of the whole response dataset (UTC) |
| Africa Pulse ingest time | when we fetched it — must be recorded locally |

**Implication:** element `timestamp` must not be treated as an event time or used for
freshness scoring. Freshness should be measured against `timestamp_osm_base` or our
own ingest time.

## Units

OSM is a **tagged, unit-free schema**: values are mostly untyped strings whose meaning
comes from the key, so units are conventional rather than enforced.

- **Coordinates:** decimal degrees, WGS 84 (EPSG:4326). Node `lat`/`lon`; way geometry
  as arrays of `{lat, lon}`. Positive lat = north, positive lon = east — Accra is
  ~`5.55, -0.18`, so its longitude is negative (west of Greenwich).
- **Distances / dimensions:** metric by convention, but values are free-form strings and
  units are *not globally enforced* — a `maxspeed` value may be a bare number, carry an
  explicit unit suffix (e.g. `30 mph`), or rely on local convention. The Accra sample
  returned `"maxspeed": "50"`, which in Ghana's context reads as 50 km/h, but that is
  this specific sample's interpretation only. Heights, widths, lengths and `ele`
  (elevation) are conventionally metres. Parse the actual tag representation and validate
  regional conventions rather than assuming a unit.
- **No currency fields** in the core schema. Where present (e.g. `fee`, `charge`) the
  currency is generally *not* stated in the tag and must not be assumed.
- **Untyped values:** tags such as `"lanes": "2"`, `"oneway": "yes"`, `"lit": "yes"` are
  strings; counts and booleans require explicit parsing.
- **Free-text / locale-suffixed tags:** `name:en`, `name:zh`, `name:sk` etc. coexist with
  a default `name`. No canonical-name guarantee.
- **Multi-value tags:** values may be `;`-separated lists, e.g. the Accra sample
  returned `"healthcare": "birthing_center;doctor"`. These are not atomic and must be
  split.

Because the schema is open, **any tag not in a known allowlist is effectively unknown
type** — Africa Pulse must validate and type-cast defensively rather than trust the tag.
(Tag definitions, including units and the `;`-separated multi-value convention, are
documented per-key at https://wiki.openstreetmap.org/wiki/Map_Features; the `maxspeed`
unit convention is at https://wiki.openstreetmap.org/wiki/Key:maxspeed — note that
`maxspeed` may carry an explicit unit and should not be assumed to be km/h.)


## Rate limits

Overpass enforces **slot-based quota**, not simple requests-per-minute, and the limits
are per instance. From the official commons documentation and live `status` output:

- **Fair-use guideline:** ~**10,000 requests/day** and **< ~1 GB download/day** per user.
  (https://dev.overpass-api.de/overpass-doc/en/preface/commons.html)
- **Concurrency:** each user gets a small number of slots. Live status on
  `overpass-api.de` reported `Rate limit: 4` — i.e. 4 concurrent slots, with lines such
  as "3 slots available now".
- **Quota accounting is by IP** (or an optional user key if supplied). For IPv6 only the
  upper 64 bits are considered.
- **Cool-down:** run-time-to-cool-down ratio is 1:1 — a query taking 1s must wait ~1s
  before its slot frees. Requests that cannot secure a slot in time are dropped after
  ~15 seconds.
- **Denials:** HTTP **429** for quota/rate-limit refusals; HTTP **504** for
  time/memory resource mismatch.
- **Default limits per query:** `timeout` **180 seconds**, `maxsize` **512 MiB**.
  Max accepted declared run time is ~262144 s and max accepted declared memory is
  currently **12 GiB**, but admission requires the request to promise ≤ half of
  remaining free capacity.
- Explicitly named **problematic behaviour**: sending the same request tens of thousands
  of times a day, requesting individual elements one at a time millions of times, and
  "stitching bounding boxes to scrape the full data of the complete world". The
  documentation says for these cases "one better ought use a planet dump instead".

(The figures above — daily volume, slot count, cool-down ratio, 429/504 mapping,
default `timeout`/`maxsize` — are taken from the official commons page,
https://dev.overpass-api.de/overpass-doc/en/preface/commons.html, cross-checked
against the live `https://overpass-api.de/api/status` output quoted below.)

**Observed during this research (2026-10-11):** several legitimate small queries were
refused with **504** while the server was load-shedding, and succeeded on retry.
A production connector must therefore **treat 429/5xx, timeouts and connection
failures as expected, not exceptional**. The 429/504 mapping above reflects common
observed behaviour, not an exhaustive or universal contract, so clients should also
handle other 5xx responses, transport timeouts and malformed bodies.

**Required retry behaviour (audit note):**

- Use **bounded** retries with **exponential backoff plus jitter** — do not retry
  endlessly.
- Honour a `Retry-After` header when the server supplies one.
- **Distinguish transient from persistent failures.** A 429 or 504 under load is
  transient and worth retrying; a genuine query error (malformed Overpass QL, a bad
  tag filter) will fail identically every time — that is a defect to fix, not a
  condition to retry forever.
- Add caching in front of the API to keep repeat traffic off the shared instance.

Verbatim live `https://overpass-api.de/api/status` response (2026-10-11), showing the
4-slot quota and the 1:1 slot-availability delay in practice:

```text
Connected as: 1769411020
Current time: 2026-10-11T09:10:52Z
Announced endpoint: lambert.openstreetmap.de/
Rate limit: 4
2 slots available now.
Slot available after: 2026-10-11T09:11:16Z, in 24 seconds.
Slot available after: 2026-10-11T09:11:17Z, in 25 seconds.
Currently running queries (pid, space limit, time limit, start time):
```

Also note the separate OSMF API Usage Policy for the *editing* API, which caps
download threads at 2 and states clients "may be blocked without notice". That policy
is for the editing API, not Overpass, but it signals how strictly the project guards
shared infrastructure.

## Terms of use

- **License (quoted name):** **Open Data Commons Open Database License (ODbL) v1.0**,
  applied to the database by the OpenStreetMap Foundation. Quoting
  https://www.openstreetmap.org/copyright: "OpenStreetMap is open data, licensed under
  the Open Data Commons Open Database License (ODbL) by the OpenStreetMap Foundation
  (OSMF)." Every Overpass JSON response also embeds:
  `"copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL."`
- **Commercial use permitted?** **Yes.** ODbL imposes no non-commercial restriction.
  Africa Pulse may use OSM data commercially, provided attribution and share-alike
  obligations are met. Note that OSMF's *services* are a separate matter: access to
  shared API infrastructure may be withdrawn at any time, and the OSMF states it cannot
  provide a free-of-charge map API or tiles for third parties.
- **Storage permitted?** **Yes.** ODbL expressly grants the right to "store" the
  database or derivative works, subject to the licence's attribution and share-alike
  conditions.

### ODbL share-alike and the Africa Pulse warehouse

ODbL distinguishes two categories of output, and the obligations differ sharply
(https://opendatacommons.org/licenses/odbl/1-0/):

1. **Produced Work** (ODbL 1.0, 4.5) — a *result* that does not require copying a
   substantial part of the database, e.g. a chart, a rendered map, a report, or an
   aggregate statistic. A Produced Work is **not** subject to share-alike: you may
   publish it under your own terms. **You must still attribute** (ODbL §4.5 requires
   the attribution notice and licence reference where technically feasible).

2. **Derivative Database** (ODbL 1.0, 4.5, 5.1.1) — a database you build by
   adapting or incorporating a substantial part of the OSM database. This **is**
   subject to share-alike: it must be offered under **ODbL** (or a future version, or a
   compatible licence per 4.4), with the notice required by 4.6, and the public-use
   provision of 4.7 applies.

Applied to Africa Pulse's warehouse, the decisive question is therefore — and the
honest answer is that **it is case-specific, not settled by a general rule**:

- Whether loading OSM alongside weather, air quality, FX and other data creates a
  **Derivative Database** depends on what is actually done to the data: adaptation,
  selection, transformation, and how the records are combined. Merely storing OSM in
  a warehouse is not by itself adaptation. ODbL explicitly recognises **Collective
  Databases** (ODbL 1.0, §1.0) — OSM left in unmodified form, merely *collected*
  alongside other independent databases — which are **not** Derivative Databases.
- If OSM data **is** adapted, or a substantial part is incorporated into a database
  built from it, the result is a Derivative Database and share-alike attaches to that
  database as a whole or a substantial part.
- **Separating OSM rows into their own tables is good provenance practice but is not a
  legal safe harbour.** Partitioning does not by itself decide the licence boundary.
  What determines it is the schema, the transformations, the lineage, and how the
  data is exported and distributed.
- **Produced Works are often the safe path for outputs** — a chart, a rendered map, a
  report, or an aggregate statistic is a Produced Work and is not share-alike. But
  *not every analytical mart is automatically a Produced Work*: if a mart is designed
  so the underlying OSM data can be extracted from it, or if it embeds a database
  derived from OSM, the analysis changes. Do not promise blanket Apache-2.0 release
  for every mart without case-specific review.

**This is a licensing analysis, not legal advice.** Before any public distribution of
a combined warehouse or derived product, document the data lineage and obtain a
qualified legal opinion on the concrete schema, transformation pipeline, and
distribution model — the ODbL itself warns that database rights vary by jurisdiction.
  Storing unmodified OSM extracts next to other data, without adaptation, stays in this
  category.

**This is a licensing analysis, not legal advice.** Before any public distribution of a
combined warehouse, Africa Pulse should get a qualified legal opinion, because the
ODbL itself warns that database rights vary by jurisdiction.


## Attribution requirements

OSM requires two things (https://www.openstreetmap.org/copyright):

> "Provide credit to OpenStreetMap by displaying our attribution notice."
> "Make clear that the data is available under the Open Database License."

The standard attribution string is **"© OpenStreetMap contributors"**.

Requirements by medium:

- **Browsable/rendered map:** visible credit on the map, conventionally
  "© OpenStreetMap contributors".
- **Data form / warehouse / API responses:** name and link directly to the licence.
  OSM states: "If you are distributing OSM in data form, please name and link directly
  to the license(s)."
- **Print / no-link media:** include the full URL, e.g. `https://www.openstreetmap.org/copyright`.

**Practical guidance for Africa Pulse:** the attribution and licence statement should
travel with the data (see design principle 2, "Provenance should travel with the data").
Recommend recording on every OSM-derived table: source = OpenStreetMap, licence = ODbL 1.0,
licence URL, and the string "© OpenStreetMap contributors".

Note that **trademarks** are separate from data licensing: "OpenStreetMap", the
magnifying-glass logo and "State of the Map" are registered trademarks of the OSMF and
are *not* covered by ODbL. Using the logo requires permission per the Trademark Policy.

## Redistribution restrictions

**May Africa Pulse redistribute?** Yes, with conditions, and the answer differs by form:

- **Raw / unmodified OSM extracts:** redistribution is permitted. These count as OSM
  "in unmodified form" and should keep the attribution + licence notice. Loading a
  Geofabrik extract into the warehouse falls here — note Geofabrik's own footer:
  "Data processed by Geofabrik GmbH and created by OpenStreetMap Contributors |
  License: ODbL 1.0".
- **Derived / adapted data (Derivative Database):** permitted **only if** offered under
  ODbL with the required notices. This is the share-alike condition described above.
- **Produced Works (aggregates, charts, marts, reports):** permitted under Africa Pulse's
  own licence, with attribution.

**Two constraints that are easy to trip over:**

1. **Geofabrik public extracts are metadata-scrubbed.** Usernames, user ids and changeset
   ids are removed as personal data. Africa Pulse must not expect or re-inject those
   fields, and must not redistribute them from elsewhere.
2. **Do not commit bulk data to the repository.** Africa Pulse's own README and
   CONTRIBUTING.md require this: "Do not commit source data to the repository unless its
   license and redistribution terms permit it." The Africa planet extract alone is
   **7.4 GB**, and Nigeria is 677 MB — far beyond any repository. Only trimmed sample
   responses (as in this document) belong in the repo.

Because ODbL is permissive on redistribution once attribution and share-alike are
respected, including a small trimmed sample below is acceptable — every Overpass
response itself carries the required copyright and ODbL notice.

## Known limitations

- **Wildly uneven African coverage.** OSM is volunteer-driven. Lagos, Accra, Nairobi,
  Cairo and Kinshasa are detailed; secondary cities, informal settlements and rural
  roads are frequently incomplete or absent. There is no completeness guarantee, and
  Africa Pulse should represent absent data as absent rather than interpolate it.
- **No quality guarantee.** Anyone can edit. Positional and attribute errors,
  vandalism, and stale data all occur. Data is **crowd-sourced, not authoritative**
  and should not be presented as survey-grade.
- **No schema enforcement.** Tags are free-form, so field presence varies per element,
  units are conventional, and multi-value `;`-separated strings are common.
- **Element `timestamp` is not an event time** — see Timestamp semantics. Naively using
  it for freshness or trend analysis is a real modelling hazard.
- **Id spaces are type-scoped** — a bare numeric id is ambiguous (see Identifiers).
- **Display names are mutable** — `user` changes silently; only `uid` is stable.
- **Per-instance instability.** Public Overpass instances load-shed and rate-limit under
  pressure; this research hit repeated **504** refusals and an HTTP **406** for a
  missing User-Agent. One mirror (`overpass.kumi.systems`) returned **500** during
  testing. Public instances are best-effort shared infrastructure, not an SLA-backed
  service, and OSMF notes access "may be withdrawn at any point".
- **No SLA on the public instance.** The specific public Overpass instance used here
  (`overpass-api.de`) is best-effort shared infrastructure with no service-level
  commitment unless its operator states otherwise; OSMF notes access to its shared
  services "may be withdrawn at any point". This is a statement about *this public
  instance*, not the whole ecosystem — third-party providers do sell hosted Overpass
  access and support, so a commercial option exists if reliability requirements demand
  one. For sustained production volume, evaluate hosted providers, regional extracts
  with diff pipelines, or self-hosting, chosen against the measured workload rather
  than assumed to require self-hosting.
- **History is awkward.** Reconstructing an arbitrary past OSM state is not directly
  supported by Overpass; full history files are personal-data restricted on Geofabrik.
- **Not a time-series source.** OSM provides geographic *reference* data, not dated
  observations. It cannot supply weather/AQ/mobility/FX signals by itself.


## Sample request and response

All examples below are **real requests made against `https://overpass-api.de/api/interpreter`
on 2026-10-11** (server generator: `Overpass API 0.7.62.11`), trimmed to a few records.
Requests are HTTP POST with body `data=<urlencoded query>`, content type
`application/x-www-form-urlencoded`, and a descriptive `User-Agent` (omitting it yields
HTTP 406).

### Example 1 — Points of interest: hospitals in central Accra (JSON)

Request:

```text
[out:json][timeout:25];
node[amenity=hospital](5.55,-0.20,5.60,-0.15);
out 2;
```

Response (trimmed to 1 element; note `timestamp_osm_base` and the ODbL copyright line
returned in every payload):

```json
{
  "version": 0.6,
  "generator": "Overpass API 0.7.62.11 87bfad18",
  "osm3s": {
    "timestamp_osm_base": "2026-10-11T09:06:50Z",
    "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL."
  },
  "elements": [
    {
      "type": "node",
      "id": 7308441494,
      "lat": 5.5537470,
      "lon": -0.1852280,
      "tags": {
        "addr:city": "Accra",
        "addr:street": "Reverend Richter Street",
        "amenity": "hospital",
        "contact:phone": "0302775259",
        "healthcare": "birthing_center;doctor",
        "name": "Osu Maternity Home Hospital"
      }
    }
  ]
}
```

### Example 2 — Linear feature: a primary road with geometry

Request:

```text
[out:json][timeout:25];
way[highway=primary](5.55,-0.20,5.60,-0.15);
out geom 1;
```

Response (trimmed; the three coordinate pairs shown are copied unchanged with
intermediate vertices omitted — this is `Independence Avenue` in Accra; its `maxspeed`
value `"50"` reads as 50 km/h under Ghana's local convention):

```json
{
  "elements": [
    {
      "type": "way",
      "id": 5019318,
      "bounds": {
        "minlat": 5.5594636, "minlon": -0.1969610,
        "maxlat": 5.5615908, "maxlon": -0.1958957
      },
      "nodes": [1837568457, 1837568465, 104287876, 6015588944, 107391740],
      "geometry": [
        { "lat": 5.5594636, "lon": -0.1969610 },
        { "lat": 5.5597090, "lon": -0.1968830 },
        { "lat": 5.5615908, "lon": -0.1958957 }
      ],
      "tags": {
        "highway": "primary",
        "lanes": "2",
        "lit": "yes",
        "maxspeed": "50",
        "maxspeed:type": "sign",
        "name": "Independence Avenue",
        "oneway": "yes",
        "smoothness": "good",
        "surface": "asphalt"
      }
    }
  ]
}
```


### Example 3 — Administrative boundary for a city (relation + cross-ids)

Request:

```text
[out:json][timeout:25];
relation[boundary=administrative][admin_level=8](5.55,-0.20,5.62,-0.17);
out tags 5;
```

Response (trimmed; `admin_level=8` is Accra's municipal level, and `wikidata`/`wikipedia`
give entity-resolution handles):

```json
{
  "elements": [
    {
      "type": "relation",
      "id": 12803764,
      "tags": {
        "admin_level": "8",
        "boundary": "administrative",
        "name": "Accra",
        "name:sk": "Akkra",
        "type": "boundary",
        "wikidata": "Q3761",
        "wikipedia": "en:Accra"
      }
    }
  ]
}
```

### Example 4 — CSV output form

Request:

```text
[out:csv(::id,name;true;",")][timeout:25];
node[amenity=hospital](5.553,-0.187,5.557,-0.183);
out 5;
```

Response (verbatim, one record):

```csv
@id,name
7308441494,Osu Maternity Home Hospital
```

### Example 5 — Empty result and a failed query (both are real)

A query by exact name for `"Accra Metropolitan Assembly"` at `admin_level=8` returned a
**200 with zero elements** — an empty `elements` array is a valid, meaningful result
(no match), not an error:

```json
{ "version": 0.6, "generator": "Overpass API 0.7.62.11 87bfad18", "elements": [] }
```

Conversely, a heavier query (`area["ISO3166-1"="GH"]` then selecting all `admin_level=4`
relations inside it) returned **HTTP 504 Gateway Timeout** on first attempt and
succeeded later once server load dropped. This is the documented resource/rate-limit
behaviour, and it is why the connector needs retry with backoff.

**Licensing note on these samples:** only a handful of records are included, each
response carries OSM's required ODbL notice, and OSM requires that data distributed in
data form "name and link directly to the license(s)" — satisfied by the Terms of use
and Attribution requirements sections above.

## Assessment

**Verdict: a strong, widely used open-data candidate for the geospatial backbone, with
several caveats that must be designed around.**

Why it fits Africa Pulse:

- It is a strong, widely used open-data candidate for **African city boundaries,
  administrative geographies, road networks and POIs** at the granularity this platform
  needs. The main alternative is purchasing commercial geodata; other open options
  should be compared against required city coverage, accuracy, licensing, and update
  cadence before concluding OSM is the best fit.
- **No API key is ordinarily needed for the public endpoints used here, and ODbL
  permits commercial use** — but note that no credentials ≠ guaranteed availability:
  infrastructure uptime, provider terms and compliance work are separate concerns.
- **Near-real-time via Overpass** — the sampled response on 2026-10-11 was about 50
  seconds behind the server clock, with daily bulk extracts as a fallback. This is a
  dated observation, not a freshness guarantee; `timestamp_osm_base` should be
  monitored continuously.
- **Good entity-resolution hooks**: `wikidata`/`wikipedia` tags and stable `(type, id)`
  keys let OSM act as the spatial join key tying the other sources together —
  directly serving design principle 5, "Cities are configuration, not architecture".
  Note these external identifiers are optional and may be missing or wrong.
- Licence is permissive for the outputs Africa Pulse cares about: charts, rendered
  maps, reports and aggregate statistics are Produced Works, publishable under
  Apache-2.0 with attribution — subject to case-specific review per the Terms of use
  section above.

Risks and required mitigations:

| Risk | Mitigation |
|---|---|
| Uneven African coverage; no completeness guarantee | Per-city coverage measurement before onboarding a city; represent missing data as missing (design principle 7) |
| Crowd-sourced, unverified data | Treat as reference data, not ground truth; never present as authoritative |
| No schema enforcement; untyped tags | Strict allowlist + explicit type-casting; quarantine unknown tags |
| Element `timestamp` ≠ event time | Never use it for freshness/trends; measure against `timestamp_osm_base` and ingest time |
| Id spaces are type-scoped | Composite primary key `(type, id)` |
| 429/504 load-shedding, no SLA | Retry with backoff; cache; fall back to bulk extracts; self-host if volume grows |
| **ODbL share-alike on a combined warehouse** | **Classification depends on the actual transformations and distribution model, not on table layout. Keep OSM-derived tables separated and provenance-tagged for governance, document lineage, and get legal review before public distribution** |

The share-alike question raised in the issue is the most strategically significant
item here, and the honest answer is that it cannot be settled by this document. ODbL
draws a distinction that turns on what is actually *done* to the data — adaptation,
selection, transformation and how information is combined — not on how tables are
laid out. Putting OSM rows in separate tables is useful provenance governance, but it
is not by itself a legal boundary. Loading OSM alongside weather, air quality, FX and
other data does not automatically make every combined dataset a Derivative Database;
equally, a mart or report is not automatically a Produced Work if it lets the
underlying OSM data be extracted from it. So the practical path is: keep OSM-derived
data separated and provenance-tagged, document transformations and lineage, treat
rendered outputs and aggregate statistics as the safest route to publication, and
obtain a qualified legal opinion on the concrete schema, pipeline and distribution
model before releasing anything publicly. See the Terms of use section above.

## Researched by

GitHub handle: **@abeenoch** (researched and authored by the contributor opening
issue #6).

Date checked: **2026-10-11** — all live queries against `overpass-api.de`, the Geofabrik
Africa index, and the ODbL/OSMF policy pages were verified on this date. Terms and
quotas change, so re-check before relying on this entry.

### What is verified vs. unknown

In line with the acceptance criterion that unknowns are marked Unknown with a note on
what was checked:

**Verified on 2026-10-11 by live request or direct fetch:**

- Overpass endpoint behaviour, JSON/CSV output forms, way geometry, and the
  `timestamp_osm_base` field — confirmed by executing real queries.
- Absence of any authentication requirement — confirmed by fetching the API with no
  credentials.
- HTTP 406 on a missing `User-Agent`, and HTTP 504 under load — both observed.
- Slot quota of 4 and slot-availability delay — observed in live `/api/status` output.
- Licence name, attribution wording, and ODbL section numbering — read directly from
  https://opendatacommons.org/licenses/odbl/1-0/ and
  https://www.openstreetmap.org/copyright.
- Geofabrik extract availability, sizes, and metadata scrubbing — from
  https://download.geofabrik.de/africa.html.

**Unknown — deliberately not asserted:**

- **Exact per-day request ceiling in production.** The ~10,000/day figure is the
  published fair-use guideline, but the real limit varies with server load and is not
  a hard published contract. Do not design against it as a guarantee.
- **Coverage completeness for any specific African city.** No per-city audit was run;
  only that coverage is uneven. A city-specific coverage measurement is required
  before onboarding, and is listed as a follow-up task.
- **Current OSMF position on third-party API access.** OSMF policy pages have changed
  over time; the policy links are checked for existence but the project's current
  stance should be re-confirmed at implementation time.
- **Legal interpretation of ODbL share-alike as applied to a combined warehouse.** The
  analysis above is documentary reasoning, not legal advice. **Unknown until a
  qualified lawyer reviews it.** This is the single most important open item.

