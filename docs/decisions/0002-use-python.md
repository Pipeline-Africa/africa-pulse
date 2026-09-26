# 0002 — Use Python as the primary implementation language

## Status

Accepted

## Context

Africa Pulse needs a language for connectors, ingestion, transformations, quality checks, and orchestration. The project expects contributors from a wide range of backgrounds, including students learning data engineering.

## Decision

Python is the primary implementation language for Africa Pulse.

Tooling choices (package management, linting, testing, orchestration) will be recorded in separate ADRs.

## Alternatives considered

- **Go / Rust** — strong for high-throughput ingestion, but a smaller data-engineering ecosystem and a higher barrier for new contributors.
- **SQL-first (e.g. dbt only)** — well suited to warehouse transformations, but does not cover acquisition, validation, or orchestration on its own. SQL-based transformation tooling may still be adopted alongside Python.

## Consequences

- Contributors can rely on the Python data ecosystem (HTTP clients, validation libraries, ClickHouse drivers, orchestrators).
- Performance-critical paths, if any emerge, can be revisited in a later ADR.
