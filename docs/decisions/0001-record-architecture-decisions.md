# 0001 — Record architecture decisions

## Status

Accepted

## Context

Africa Pulse is an open-source project that will be shaped by many contributors over time. Decisions about architecture, data modelling, and source handling need to be understandable without reverse-engineering them from code or relying on the memory of early maintainers.

## Decision

We will record significant architectural and data-model decisions as Architecture Decision Records in `docs/decisions/`, numbered sequentially.

A decision warrants an ADR when it affects schemas, source contracts, public interfaces, warehouse design, or cross-cutting concerns such as provenance and quality.

## Alternatives considered

- **Decisions only in issues and pull requests** — discoverable at the time, but hard to find later and easily lost across discussions.
- **A single design document** — tends to be rewritten in place, losing the history of why things changed.

## Consequences

- Significant proposals should include or be followed by an ADR.
- Superseded decisions are kept and marked as superseded rather than deleted.
