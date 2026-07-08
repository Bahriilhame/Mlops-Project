# Automation Notes

This project previously documented a GitHub Actions data-triggered retraining flow based on changed `.dvc` files. In the production-oriented architecture, GitHub Actions is kept for code CI and Dagster is the automation layer for the DataOps/MLOps pipeline.

## DVC Role

DVC still matters, but it is not the production trigger. It stores exact dataset versions and lets collaborators restore a known raw CSV from Google Drive.

The real dataset file is:

```text
data/raw/student_performance.csv
```

The Git-tracked DVC pointer is:

```text
data/raw/student_performance.csv.dvc
```

GitHub stores the metadata pointer. Google Drive stores the data object. Dagster schedules and materializations decide when the pipeline runs.

## Updating The DVC Dataset Correctly

On Windows, use the project DVC wrappers:

```powershell
scripts\dvc.cmd add data\raw\student_performance.csv
scripts\dvc.cmd push
git add data/raw/student_performance.csv.dvc
git commit -m "Update student performance dataset"
git push
```

On macOS/Linux:

```bash
dvc add data/raw/student_performance.csv
dvc push
git add data/raw/student_performance.csv.dvc
git commit -m "Update student performance dataset"
git push
```

Commit the `.dvc` metadata file. Do not commit the real CSV.

## Verifying Production Automation

Use Dagster, not GitHub Actions, to verify production-style retraining:

```powershell
scripts\dagster_dev.cmd
```

Then materialize the asset graph or enable the daily schedule. The model trains only when `metadata/data_fingerprint.json` does not match the current training dataset fingerprint, unless the Dagster run config sets `force_train: true`.
