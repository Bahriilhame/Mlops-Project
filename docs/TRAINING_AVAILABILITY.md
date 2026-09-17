# Training and site availability

The observed outage tracks job execution, but no production resource readings or
OOM logs were available when preparing this change. The previous deployment had
no Dagster resource limits, allowed overlapping runs, and loaded entire CSV files
into pandas. These are identified risks, not a confirmed production diagnosis.

## Changes

- Dagster web UI: maximum 0.5 CPU and 512 MiB RAM.
- Separate daemon/worker: maximum 1 CPU and 1536 MiB RAM by default, with no swap.
  Run subprocesses inherit this container's limits.
- Shared Dagster instance configuration queues runs, with one active run across
  the instance. The worker daemon must be running for queued runs to start.
- Native numerical libraries and dlt workers use one thread/worker.
- CSV ingestion yields 10,000-row batches. dbt's DuckDB engine uses one thread
  and a 512 MB engine memory limit (not a limit on all process allocations).
- Silhouette calculation still uses all rows, with a 64 MiB working-memory
  target for distance chunks. This does not cap all Python allocations.
- Runtime Dagster/MLflow stores are excluded from the Docker build context.

API and dashboard continue using their existing deployed model bundle. Training
does not publish a new model to those containers. Training outputs remain in the
worker container and must be exported before that container is recreated.

## Deployment and verification

1. Confirm this checkout matches the affected stack and identify the failing job.
   Stop further manual/scheduled training launches while investigating. Cancel
   active training through Dagster if needed; do not stop the web stack.
2. On the host, capture `docker stats --no-stream`, `docker compose ps`, and
   `docker compose logs --since 30m dagster api mlflow`. Check host memory, disk
   space, and kernel OOM messages. Correlate timestamps with the failed job.
   Preserve Dagster run records. The local run database contained no runs.
3. Size TRAINING_MEMORY and TRAINING_CPUS against actual host capacity. The
   defaults are a starting budget, not proof of capacity. Leave memory for the
   OS, API, MLflow, dashboard, and Dagster UI. If that headroom does not exist,
   keep training paused and move it to separate compute. A worker OOM can fail
   a job; monitor it rather than automatically raising the limit.
4. Validate `docker compose config --quiet`. Build the image away from the live
   host if builds themselves cause pressure. Apply just the orchestration
   services with `docker compose up -d --no-deps --build dagster dagster-worker`
   during an agreed maintenance window. This recreates the Dagster UI but does
   not intentionally restart the API, dashboard, or MLflow. Never use
   `docker compose down` for this change.
5. Confirm both orchestration services are healthy and the daemon has a fresh
   heartbeat. Launch one controlled training run. Probe the dashboard and API
   `/health` every five seconds while recording response times, errors, and
   `docker stats`. Verify a second submitted run remains queued; cancel that
   second test run after verification.
6. Stop the test on an HTTP failure, sustained latency beyond the agreed target,
   host memory pressure, or an OOM/restart. Inspect the failed step before retrying.
   Accept only after a complete run with no site errors or unexpected restarts.
7. Configure host alerts for memory/disk pressure and OOM events, HTTP probes for
   the API/dashboard, and Dagster worker health/run failures. Restore scheduling
   only after the controlled run passes. Alerting requires the host's monitoring
   system and is not provisioned by this repository patch.

Rollback: stop the new worker, revert the configuration/code change, and recreate
only the Dagster service. Keep training paused until the cause is resolved.

References: [Compose resource limits](https://docs.docker.com/reference/compose-file/services/)
and [Dagster run coordinators](https://release-1-8-1.dagster.dagster-docs.io/deployment/run-coordinator).
