# 0003: Use Dagster for orchestration

## Status

Proposed

## Context

Africa Pulse needs an orchestrator to schedule source acquisition, run transformations and quality checks, and surface failures. The choice shapes how connectors are written, how provenance and freshness are tracked (see issue #21, ingestion run metadata and provenance), and how easily a contributor can run the platform on a laptop.

The [README design principles](../../README.md#design-principles) set the bar:

- source evidence is preserved and inspectable;
- provenance travels with the data;
- data quality is measured, not hidden;
- reprocessing of history is possible;
- cities are configuration;
- analytical claims stay traceable;
- missing data is represented, not fabricated.

[ADR 0002](0002-use-python.md) fixes Python as the implementation language and defers the orchestrator to a separate ADR. This is that ADR.

Three Python orchestrators were evaluated: Dagster, Prefect and Apache Airflow. All three are licensed Apache-2.0 (package metadata of the versions tested).

### Proof of concept

The same job was built in each tool on 2026-11-03: fetch one URL (`https://raw.githubusercontent.com/Pipeline-Africa/africa-pulse/main/README.md`), write the response to a file with a JSON provenance record (URL, HTTP status, byte count, SHA-256, UTC fetch time, partition), retry up to 3 times, and test it with pytest. Each tool was then asked to backfill several past dates and to retry against a URL that returns 404. The code is not committed, per the issue.

Environment: Linux, Python 3.13, one virtual environment per tool, installed with pip. Versions: Dagster 1.13.28 (with `dagster-webserver`), Prefect 3.9.1, Airflow 3.3.2 (installed with the official constraints file). Docker images were not run, because the test environment could not pull from Docker registries; Docker requirements below come from each tool's documentation.

| Observation | Dagster 1.13.28 | Prefect 3.9.1 | Airflow 3.3.2 |
|---|---|---|---|
| Packages installed | 69 | 104 | 129 |
| Virtual environment size | 167 MB | 166 MB | 207 MB |
| Local stack with UI | `dagster dev`: 5 processes, 642 MB resident | `prefect server start`: 1 process, 232 MB resident | `airflow standalone`: 5 processes, 781 MB resident |
| Single run | `dagster asset materialize --partition 2026-11-01`: 2 assets and 1 asset check in 8 s | `python flow.py`: ran with no server set up (Prefect started a temporary local server itself); 3 dated runs in 19 s | `airflow db migrate` (6 s), then `airflow dags test`: 2 tasks in 8 s |
| Backfill of past dates | Native daily partitions. A CLI range failed with a message that it needs `BackfillPolicy.single_run()` or a running daemon; `dagster job backfill` with `dagster-daemon` running completed 4 partitions | No partition concept; implemented as a loop calling the flow with a date parameter (3 runs) | `airflow backfill create` created runs for 3 dates; they executed only once the scheduler was running (`airflow standalone`) |
| Retries against a 404 | 3 × `STEP_UP_FOR_RETRY`, then `RUN_FAILURE` | "Retry 1/3" to "3/3", then `Failed` | 3 × `up_for_retry`, then `failed` |
| Provenance of the output | Returned as asset materialization metadata (SHA-256, bytes, URL), visible per partition in the UI | Logged; persisting it is left to our code | Passed between tasks as XCom; persisting it is left to our code |
| pytest | `dagster.materialize()` with a partition key: passed | `prefect_test_harness()`: passed in 12.3 s | DAG structure test with `DagBag`: passed after removing the `include_examples` argument, which raised `TypeError` in 3.3.2 |
| Setup surprises | None beyond the backfill daemon requirement | Sent telemetry by default (blocked in the test environment, logged as an error) | `airflow standalone` starts its components by calling `airflow` on `PATH`; it failed until the virtual environment was activated |

All three retried a permanent 404 the same way as a transient error. Retry rules that tell the two apart will be our code, whichever tool is chosen.

## Comparison

| Criterion | Dagster | Prefect | Airflow |
|---|---|---|---|
| **Local development (laptop, Docker)** | Runs with pip alone: `dagster dev` gives UI, daemon and code server on SQLite (PoC). A Docker Compose example is documented ([Deploy with Docker](https://docs.dagster.io/examples/deploy_docker)). Medium footprint: 642 MB (PoC) | Lightest: a flow runs as a plain Python script with no server set up, and `prefect server start` is one process (PoC). SQLite by default ([Server concepts](https://www.prefect.io/docs/v3/concepts/server.md)) | Heaviest. Docker Compose needs "at least 4.00 GB of memory" for the containers and runs Postgres, Redis, scheduler, DAG processor, API server, worker and triggerer ([Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/)). Without Docker, `airflow standalone` used 781 MB (PoC) |
| **Data model: tasks vs assets** | Asset-first. Each `@asset` is a named data product with dependencies, partitions and checks; jobs select assets (PoC) | Task-first (`@flow`, `@task`). Assets added with the `@materialize` decorator ([materialize API](https://www.prefect.io/docs/v3/api-ref/python/prefect-assets-materialize.md)); dependencies are inferred from the task graph ([Assets guide](https://www.prefect.io/docs/v3/how-to-guides/workflows/assets)) | Task-first (DAGs of tasks). Assets are URI references that tasks update and DAGs can be scheduled on; Airflow tracks update events, not asset contents ([Asset-aware scheduling](https://airflow.apache.org/docs/apache-airflow/3.0.6/authoring-and-scheduling/asset-scheduling.html)) |
| **Lineage, provenance, freshness** | Asset graph is the lineage view. Per-materialization metadata gave a provenance record per partition (PoC). Asset checks run with the asset (PoC). Freshness policies (`FreshnessPolicy.time_window`) exist in open source but are in preview, off by default, and "the APIs may change" ([Freshness policies](https://dagster.io/docs/guides/observe/asset-freshness-policies)) | Asset lineage is shown in the UI in the docs ([Assets guide](https://www.prefect.io/docs/v3/how-to-guides/workflows/assets)), but the self-hosted server in 3.9.1 has no `/assets` API routes (checked in the installed package), so lineage appears to need Prefect Cloud. No freshness feature found in the docs checked | Lineage through the OpenLineage provider, a separate package not installed by default (PoC; [OpenLineage provider](https://airflow.apache.org/docs/apache-airflow-providers-openlineage/stable/guides/structure.html)). No freshness checks; SLAs were removed in 3.0 and replaced by Deadline Alerts in 3.1 (docstring in the installed `airflow.sdk.DAG`) |
| **Backfills and reprocessing** | Native time partitions; backfills run one run per partition by default, or batched or single-run via `BackfillPolicy` ([Backfill strategies](https://dagster.io/docs/examples/best-practices/partition-backfill-strategies)). Needs the daemon (PoC) | No partitions. Reprocessing is a parameterised flow run per date, which we write and track ourselves (PoC) | Scheduler-managed backfills since 3.0 ([3.0 release notes, AIP-78](https://airflow.apache.org/docs/apache-airflow/3.0.0/release_notes.html)); work by logical date and need the scheduler (PoC) |
| **Retries, failure handling, alerting** | `RetryPolicy` per asset (PoC). Open-source alerting through run-failure sensors, including `make_email_on_run_failure_sensor` (present in the installed package). Built-in freshness alerting is a Dagster+ feature ([Freshness policies](https://dagster.io/docs/guides/observe/asset-freshness-policies)) | `retries` and `retry_delay_seconds` per task ([Retries](https://www.prefect.io/docs/v3/how-to-guides/workflows/retries)). Automations and events are stored by the self-hosted server ([Server concepts](https://www.prefect.io/docs/v3/concepts/server.md)) | `retries` and `retry_delay` per task (PoC); failure callbacks; Deadline Alerts from 3.1 |
| **Testing pipelines** | `materialize()` runs assets in-process in pytest, with partition keys and checks (PoC; [Testing assets](https://docs.dagster.io/guides/test)) | Flows are plain functions; `prefect_test_harness()` gives an isolated temporary database (PoC; [Testing](https://docs.prefect.io/latest/guides/testing/)). Slowest test in the PoC (12.3 s) | `dag.test()` runs a DAG in-process (PoC). The DAG-loading test API changed between releases (PoC) |
| **Self-hosting and cost** | Three long-running services: webserver, daemon (single replica) and code-location servers; SQLite or Postgres storage ([OSS deployment architecture](https://dagster.io/docs/deployment/oss/oss-deployment-architecture)). Software cost: none. Optional paid hosted product: Dagster+ | One server plus workers; SQLite or PostgreSQL 14.9+ ([Server concepts](https://www.prefect.io/docs/v3/concepts/server.md)). Software cost: none. Prefect Cloud adds "RBAC, Audit logs, and SSO" ([Server concepts](https://www.prefect.io/docs/v3/concepts/server.md)) | Scheduler, DAG processor, API server, triggerer, workers, Postgres, and Redis for the Celery setup ([Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/)). Software cost: none |
| **Community, docs, license** | Apache-2.0. 16,083 GitHub stars on 2026-09-02 ([data-tool-momentum](https://huggingface.co/datasets/datamatastudios/data-tool-momentum)). Led by one company (Dagster Labs). Several documentation URLs redirected to new locations during this review | Apache-2.0. 23,758 stars on 2026-09-02 ([data-tool-momentum](https://huggingface.co/datasets/datamatastudios/data-tool-momentum)). Led by one company (Prefect) | Apache-2.0, an Apache Software Foundation project. 46,687 stars on 2026-09-02 ([data-tool-momentum](https://huggingface.co/datasets/datamatastudios/data-tool-momentum)). Largest community and question base by far ([ZenML comparison](https://www.zenml.io/blog/orchestration-showdown-dagster-vs-prefect-vs-airflow)) |

## Decision

We will use **Dagster** as the Africa Pulse orchestrator, with sources, raw evidence, standardised tables and marts modelled as software-defined assets.

Reasons, against the design principles:

1. **Assets match the platform's layers.** The README describes data products (raw evidence, standardised observations, integrated tables, marts). Dagster models exactly these, so the lineage graph is the architecture diagram and stays current without extra tooling.
2. **Provenance travels with each output.** In the PoC, the SHA-256, URL and byte count of each fetch were stored against the asset partition without extra code. This is the shape issue #21 asks for.
3. **Reprocessing is built in.** Time partitions and backfill policies cover historical reprocessing per source and per day, with failed partitions retried on their own.
4. **Quality sits next to the data.** Asset checks run with the asset they check and are shown in the same place, which supports "data quality is measured, not hidden".
5. **Contributors can run it on a laptop.** `pip install` plus `dagster dev` on SQLite is enough, with no Postgres or Docker required for development.

### What we give up

- **Airflow's community and governance.** Airflow has about three times Dagster's GitHub stars and is governed by the Apache Software Foundation. Contributors are more likely to know Airflow already, and answers to common problems are easier to find.
- **Prefect's simplicity.** Prefect has the lowest footprint (one 232 MB process in the PoC) and needs no new concepts beyond decorated Python functions. Dagster asks contributors to learn assets, partitions, resources and definitions.
- **Single-vendor stewardship.** Dagster is led by one company. Features can move between the open-source project and Dagster+, as built-in freshness alerting shows.
- **Stable freshness APIs.** Dagster's freshness policies are in preview and the previous API was already renamed `LegacyFreshnessPolicy`. Freshness monitoring may need rework as the API settles.
- **A daemon in every deployment.** Schedules, sensors and multi-run backfills need `dagster-daemon` (PoC), which runs as a single replica.

## Alternatives considered

- **Apache Airflow.** The strongest choice for ecosystem, governance and hiring familiarity. Rejected because its model is tasks rather than data, so lineage needs the separate OpenLineage provider and a lineage backend. It also has no freshness checks (SLAs were removed in 3.0), and its local stack is the heaviest: 4 GB recommended for Docker, 781 MB without it. The DAG-loading test API also changed between minor releases in the PoC.
- **Prefect.** The easiest to start with, and suitable for a smaller project. Rejected because the self-hosted server has no asset lineage (no `/assets` routes in 3.9.1). It also has no partitions, so backfills and per-day provenance would be our own code. Telemetry is on by default and contributors would need to opt out.
- **No orchestrator (cron plus scripts).** Lowest cost, but it gives no retries, lineage, backfills or failure visibility, all of which the design principles require.

## Consequences

- Connectors will be written as Dagster assets, partitioned by day (or by the source's natural period). Each materialization records source URL, response checksum, fetch time and status as metadata (issue #21).
- Quality rules will be implemented as asset checks attached to the assets they test.
- Local development: `pip install` and `dagster dev`, on SQLite. Shared deployments: webserver, daemon and code location in Docker, with Postgres storage. A follow-up issue should document the local workflow and a Docker Compose file.
- Alerting uses open-source run-failure sensors (e.g. email or chat webhook); Dagster+ is not required.
- Freshness monitoring starts with Dagster's preview freshness policies, behind `freshness: enabled: True` in `dagster.yaml`, and will be revisited when the API is stable.
- Retry policies must separate permanent errors (for example HTTP 4xx) from transient ones; none of the tools did this by default.
- Dagster versions will be pinned and upgraded deliberately, given the API changes noted above.
- If adoption or community support becomes a problem, Airflow 3 remains the fallback. Keeping connector logic in plain Python functions called from assets keeps a later migration feasible.
