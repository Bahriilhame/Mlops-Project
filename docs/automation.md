# DataOps and MLOps Automation

This project has two ways to run the pipeline:

- manual local commands for development
- GitHub Actions automation when data or pipeline code changes

The automated workflow is defined in `.github/workflows/dataops-mlops.yml`.

## What Triggers Automation

The workflow runs on `git push` when any of these paths change:

- `data/raw/*.dvc`
- `dlt_pipeline/**`
- `dbt/**`
- `src/**`
- `requirements.txt`

It can also be started manually from GitHub Actions with `workflow_dispatch`.

## How DVC Triggers The Pipeline

The real dataset file is:

```text
data/raw/student_performance.csv
```

That CSV is not committed to Git. Instead, DVC creates a small metadata file:

```text
data/raw/student_performance.csv.dvc
```

The `.dvc` file contains the data hash, size, and path. When the CSV changes and you run `dvc add`, the metadata file changes. GitHub Actions cannot see the private CSV, but it can see the changed `.dvc` file in Git, so that metadata change indirectly triggers the automated pipeline.

## Why Google Drive Stores Data And GitHub Stores Metadata

GitHub is good for code, configuration, tests, and small metadata files. It is not the right place for large or frequently changing raw datasets.

Google Drive stores the actual dataset through the DVC remote. GitHub stores only the pointer file that says which dataset version should be used. This keeps the repository lightweight while still making each model training run reproducible.

## How DataOps And MLOps Are Connected

The automated workflow connects the data and model lifecycle:

1. DVC restores the exact dataset version from Google Drive.
2. dlt loads the raw CSV into DuckDB.
3. dbt builds the cleaned and training-ready tables.
4. dbt tests validate transformed data.
5. pytest validates Python code and data contracts.
6. the training module creates the model and metrics.
7. MLflow records the training run.
8. GitHub uploads model artifacts, metrics, and MLflow outputs.

This means a dataset version change can automatically produce a new validated model artifact.

## Updating The Dataset Correctly

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

## GitHub Secrets For DVC

The automated workflow needs permission to pull data from the Google Drive DVC remote. Use a Google service account for CI:

1. Create a Google Cloud service account.
2. Enable the Google Drive API.
3. Create a JSON key for the service account.
4. Share the Google Drive DVC folder with the service account email.
5. Base64 encode the JSON key.
6. Add it to GitHub repository secrets as:

```text
DVC_GDRIVE_SERVICE_ACCOUNT_JSON_B64
```

PowerShell base64 example:

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("service-account.json"))
```

Git Bash or Linux example:

```bash
base64 -w 0 service-account.json
```

Do not commit the service account JSON file.

## Verifying Automation Worked

After pushing the `.dvc` metadata change:

1. Open the repository on GitHub.
2. Go to `Actions`.
3. Open `DataOps and MLOps Pipeline`.
4. Confirm these steps passed:
   - `Pull dataset with DVC`
   - `Run dlt ingestion`
   - `Run dbt models`
   - `Run dbt tests`
   - `Run pytest`
   - `Train model`
5. Download the workflow artifacts:
   - `trained-model`
   - `model-metrics`
   - `mlflow-runs`

If `Pull dataset with DVC` fails, check that the GitHub secret exists and that the Google Drive folder is shared with the service account email.
