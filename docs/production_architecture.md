# Production-Oriented Architecture

EduScore keeps the original course-friendly tools, but the production architecture changes the ownership of automation:

- Dagster orchestrates the data and model pipeline.
- DVC stores reproducible dataset versions.
- GitHub Actions validates code changes.
- MLflow tracks experiments and registers approved model candidates.
- FastAPI serves the latest approved local model artifact.

## Production Flow

The production-style Dagster flow is:

```text
check data source/freshness
-> ingest with dlt
-> run dbt transformations
-> run dbt tests
-> run pytest/schema checks
-> compute dataset fingerprint
-> train only if data changed or force_train=true
-> evaluate model
-> log metrics/artifacts to MLflow
-> register model candidate if thresholds pass
```

The Dagster definitions live in:

```text
pipelines/dagster_pipeline.py
```

A daily schedule named `daily_student_score_pipeline` runs at 02:00 Africa/Casablanca time.

## Data Change Detection

The fingerprint logic lives in:

```text
src/student_score_mlops/data_versioning.py
```

Dagster computes a deterministic fingerprint of the training dataset after dbt has built and tested it. The previous successful fingerprint is stored locally in:

```text
metadata/data_fingerprint.json
```

If the fingerprint is unchanged, the training asset returns a skipped/up-to-date result. If it changed, training runs and the metadata file is updated only after training succeeds.

## Quality Gates

Bad data should block training.

The pipeline stops before training if:

- dlt ingestion fails
- `dbt run` fails
- `dbt test` fails
- pytest/schema checks fail

Training can also fail after evaluation if metrics do not pass configured thresholds:

```text
MIN_R2
MAX_RMSE
```

These defaults are documented in `.env.example`. The baseline threshold is intentionally modest for this dataset; tighten it after you establish a stronger model or a better validation strategy.

## MLflow Registry

Training logs:

- model parameters
- MAE, RMSE, R2
- dataset fingerprint
- dataset row count
- training timestamp
- model artifact
- metrics JSON
- training reference statistics

If metrics pass the thresholds, the model is registered as:

```text
EduScoreStudentPerformanceModel
```

Registration does not mean automatic production deployment. Promotion to production should be a separate approval step after reviewing metrics, data quality, and monitoring signals.

## DVC Role

DVC is retained for reproducibility and storage, not orchestration.

DVC stores exact raw dataset versions in Google Drive. Git stores the `.dvc` metadata file. Dagster decides when the pipeline runs and whether retraining is needed.

Google Drive is acceptable for a prototype or small team. A production system would normally use storage such as S3, GCS, Azure Blob Storage, Delta Lake, or lakeFS with clearer access control, audit logs, and lifecycle policies.

## GitHub Actions Role

GitHub Actions remains code CI:

- install dependencies
- run `ruff`
- run `pytest`
- build Docker image

It is not the production retraining orchestrator. Dataset refreshes and retraining decisions belong in Dagster.

## Production Serving

FastAPI keeps:

- `GET /health`
- `POST /predict`

It also exposes:

```text
GET /model-info
```

The endpoint returns the model path, metrics if available, dataset fingerprint metadata if available, and the API model load timestamp.

## Monitoring

Prediction events are still written to:

```text
monitoring/predictions.jsonl
```

The monitoring module can compare recent prediction feature means to the training reference means. Production monitoring should also include:

- request latency
- error rates
- input drift
- prediction drift
- model performance feedback when labels arrive
- data freshness

## Run Production-Style Locally

Start Dagster:

```powershell
scripts\dagster_dev.cmd
```

Or directly:

```powershell
dagster dev -f pipelines/dagster_pipeline.py
```

In Dagster:

1. Materialize the assets.
2. Review `training_dataset_fingerprint`.
3. Confirm `train_student_score_model` trained or skipped.
4. Enable the daily schedule if you want periodic runs.

Start MLflow UI:

```powershell
mlflow ui --backend-store-uri mlruns --host 0.0.0.0 --port 5000
```

Use `force_train: true` in Dagster run config when you intentionally want to retrain even if the dataset fingerprint is unchanged.
