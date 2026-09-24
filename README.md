# Africa Pulse

Africa Pulse is an open-source data platform for collecting, validating, integrating, and analysing near-real-time signals about African cities — weather, air quality, mobility, FX and markets, economic indicators, and public events.

It is a [Pipeline Africa](#community) project.

## Architecture

Africa Pulse is organised as a layered data platform:

1. **Source acquisition** — connectors pull data from external APIs and datasets.
2. **Raw evidence** — source responses are preserved as received, with ingestion metadata.
3. **Standardization and validation** — observations are typed, normalised, and checked.
4. **Entity and temporal integration** — observations are aligned to canonical cities and time.
5. **Analytical warehouse** — integrated data is modelled in ClickHouse.
6. **Data marts** — business and analytical views built for specific questions.
7. **Serving** — dashboards, notebooks, and other analytical consumers.

Cross-cutting concerns include observability, data quality, lineage, provenance, security, failure handling, documentation, testing, and reproducibility.

## Repository structure

```text
africa-pulse/
├── connectors/          # Source-specific acquisition connectors
├── ingestion/           # Extraction, checkpoints, raw-data handling
├── transformations/     # Standardization and integration
├── quality/             # Validation and data-quality rules
├── warehouse/           # ClickHouse schemas, tables and queries
├── marts/               # Business/analytical data marts
├── orchestration/       # Scheduling and workflow definitions
├── observability/       # Logs, metrics, freshness and health checks
├── tests/               # Unit, integration and data tests
├── docs/                # Architecture, sources, models and decisions
├── config/              # Non-secret project configuration
└── .github/             # Issue templates and repository workflows
```

## Design principles

### 1. Source evidence is valuable

Raw observations should remain inspectable. Transformations should not destroy the ability to understand what a source actually returned.

### 2. Provenance should travel with the data

Important analytical observations should be attributable to their source, ingestion context, and transformation path.

### 3. Data quality is measured, not hidden

Missing, invalid, duplicated, late, or suspicious observations should be detected and represented deliberately.

### 4. Reprocessing should be possible

Historical data should be recoverable and reproducible without manually rebuilding the entire platform.

### 5. Cities are configuration, not architecture

Adding a new city should not require redesigning the warehouse or rewriting the ingestion system.

### 6. Analytical claims must remain traceable

A metric should be explainable from its definition back to source observations.

### 7. Don't fabricate completeness

If a source is unavailable or data is missing, the system should represent that limitation rather than manufacture values.

## Current status

**Early-stage / scaffolding.**

Africa Pulse is currently being established as an open-source project. The initial implementation will focus on the architecture, source contracts, connector patterns, data model, quality framework, and a small initial city portfolio before expanding coverage.

Expect APIs, schemas, directories, and interfaces to evolve during this phase. See the [roadmap](docs/roadmap.md).

## Contributing

Contributions are welcome.

Start with [CONTRIBUTING.md](CONTRIBUTING.md), then check the issue tracker for work that is ready to be picked up.

We especially welcome contributions involving:

- Data-source research
- New ingestion connectors
- Geographic/entity resolution
- Data-quality rules
- ClickHouse modelling
- Tests
- Observability
- Documentation
- Analytical examples

## Data and source licensing

The Africa Pulse software is licensed under the Apache License 2.0.

Third-party datasets, APIs, maps, imagery, and other source material are **not** automatically covered by the project's software license. Each source must be used according to its own terms, attribution requirements, access limits, and redistribution permissions.

Do not commit source data to the repository unless its license and redistribution terms permit it.

## Community

Africa Pulse is a Pipeline Africa project.

Pipeline Africa is building open-source data infrastructure and learning communities around real African data problems.

## License

Copyright © 2026 Pipeline Africa.

The software in this repository is licensed under the [Apache License 2.0](LICENSE).
