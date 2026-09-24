# Contributing to Africa Pulse

Thank you for contributing to Africa Pulse.

Africa Pulse is an open-source data infrastructure project maintained by Pipeline Africa. Contributions should improve the reliability, usefulness, reproducibility, or accessibility of the platform.

## Before you start

Please:

- Read this document.
- Search existing issues and pull requests before opening a new one.
- Check the project's source and data-use requirements before adding a connector.
- Never commit secrets, credentials, API keys, private data, or source datasets whose terms do not permit redistribution.
- For significant architectural changes, open an issue first so the design can be discussed before implementation.

## What can I contribute?

Useful contributions include:

- New source connectors
- Source documentation and research
- City/geographic metadata
- Entity-resolution improvements
- Data-quality rules
- Schema and data-model improvements
- ClickHouse optimizations
- Tests
- Observability and operational tooling
- Documentation
- Analytical examples
- Bug fixes
- Developer-experience improvements

### Good first contributions

If you are new to the project, look for issues labelled:

- `good first issue`
- `help wanted`
- `documentation`
- `data-source`
- `testing`

A contribution does not have to be code. Source investigation, documentation, tests, and data-quality work are all first-class contributions.

## Development workflow

### 1. Fork and clone

Fork the repository on GitHub and clone your fork locally:

```bash
git clone https://github.com/<your-username>/africa-pulse.git
cd africa-pulse
```

### 2. Create a branch

Use a focused branch name:

```text
feature/weather-connector
feature/city-entity-resolution
fix/duplicate-ingestion
docs/source-register
test/fx-validation
```

Avoid working directly on `main`.

### 3. Make a focused change

Keep pull requests small enough to review. A pull request should normally address one coherent problem.

### 4. Test your changes

Run the project's relevant test and quality checks before opening a pull request.

As the project tooling matures, the exact commands will be documented here.

### 5. Commit clearly

Prefer short, descriptive commit messages following [Conventional Commits](https://www.conventionalcommits.org/):

```text
feat: add weather source connector
fix: prevent duplicate mobility observations
docs: document city entity model
test: add FX freshness checks
```

### 6. Open a pull request

Explain:

- What changed?
- Why was it necessary?
- How was it tested?
- Are there source/data licensing considerations?
- Are there schema or migration implications?
- Are there follow-up tasks?

## Adding a data source

A source connector is more than an HTTP request.

Before adding one, document the following in the [source register](docs/sources/README.md):

- Source name
- Source owner
- Documentation URL
- Access method
- Authentication requirements
- Geographic coverage
- Update frequency
- Rate limits
- Historical availability
- Identifier scheme
- Timestamp semantics
- Units
- Known limitations
- Terms of use
- Attribution requirements
- Redistribution restrictions

### Source terms matter

Africa Pulse does not grant permission to redistribute third-party data.

A source may permit API access while restricting storage, redistribution, commercial use, or bulk downloads. Check the source's current terms before contributing an implementation.

If redistribution is unclear, contribute the connector and metadata without committing the underlying dataset.

## Data quality expectations

Contributors should consider:

- Duplicate observations
- Missing fields
- Invalid values
- Malformed timestamps
- Time-zone differences
- Unit differences
- Currency differences
- Late-arriving observations
- Changing source schemas
- Source outages
- Unexpected response structures
- Identifier changes

Do not silently discard suspicious data when doing so would hide an important source problem. Prefer explicit validation, quarantine, correction, or documented propagation.

## Data provenance

Where possible, preserve enough metadata to answer:

- Where did this observation come from?
- When did the source produce it?
- When did Africa Pulse receive it?
- What transformations were applied?
- Which source record or request produced it?

## Adding a city

Adding a city should primarily be a data/configuration operation, not an architectural rewrite.

A city contribution should include, where applicable:

- Canonical city name
- Country
- Coordinates
- Geographic identifiers
- Source-specific identifiers
- Administrative context
- Relevant aliases
- Coverage limitations

Do not assume that two sources use the same definition of a city.

## Pull request review

Maintainers will review contributions for:

- Correctness
- Reproducibility
- Test coverage
- Data quality
- Security
- Source compliance
- Maintainability
- Architectural consistency
- Documentation

A contribution may be requested to change even when the implementation works if it introduces long-term maintenance or data-quality problems.

## Breaking changes

Changes affecting schemas, public interfaces, source contracts, warehouse tables, or downstream marts should be clearly identified in the pull request.

Where appropriate, provide:

- Migration notes
- Backward-compatibility information
- Deprecation period
- Documentation updates

## Issues

When reporting a bug, include:

- What happened?
- What did you expect?
- How can it be reproduced?
- What source was involved?
- Relevant logs or error messages
- Environment/version information

Do not include credentials, API keys, personal information, or private source data.

## Security

Do not report security vulnerabilities through public GitHub issues.

Use the repository's private security reporting mechanism if one is configured. If no mechanism is available, contact the maintainers privately before disclosure.

## Code of conduct

All contributors are expected to participate respectfully and constructively. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

By contributing to Africa Pulse, you agree that your contribution is provided under the [Apache License 2.0](LICENSE), subject to the terms of that license.

Copyright © 2026 Pipeline Africa.
