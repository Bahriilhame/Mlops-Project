from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DAGSTER_HOME = PROJECT_ROOT / ".dagster_home"
DAGSTER_HOME.mkdir(exist_ok=True)
os.environ.setdefault("DAGSTER_HOME", str(DAGSTER_HOME))

from dagster import (  # noqa: E402
    AssetSelection,
    Definitions,
    Field,
    ScheduleDefinition,
    asset,
    define_asset_job,
)

from dlt_pipeline.load_student_data import run_pipeline  # noqa: E402
from src.student_score_mlops.config import settings  # noqa: E402
from src.student_score_mlops.data_versioning import (  # noqa: E402
    data_changed,
    fingerprint_dataframe,
    raw_data_status,
)
from src.student_score_mlops.train import load_training_data, train  # noqa: E402


def run_command(command: list[str]) -> None:
    subprocess.run(command, check=True)


@asset
def check_raw_data_freshness() -> dict[str, Any]:
    status = raw_data_status()
    if not status["exists"]:
        raise FileNotFoundError(f"Raw dataset not found at {status['path']}")
    return status


@asset(deps=[check_raw_data_freshness])
def ingest_raw_student_data() -> str:
    run_pipeline()
    return "raw_data_loaded"


@asset(deps=[ingest_raw_student_data])
def transform_student_data() -> str:
    run_command(
        [
            "dbt",
            "run",
            "--project-dir",
            "dbt/student_score",
            "--profiles-dir",
            "dbt/student_score",
        ]
    )
    return "dbt_models_built"


@asset(deps=[transform_student_data])
def validate_student_data() -> str:
    run_command(
        [
            "dbt",
            "test",
            "--project-dir",
            "dbt/student_score",
            "--profiles-dir",
            "dbt/student_score",
        ]
    )
    return "dbt_tests_passed"


@asset(deps=[validate_student_data])
def validate_python_contracts() -> str:
    run_command([sys.executable, "-m", "pytest", "-q"])
    return "pytest_passed"


@asset(deps=[validate_python_contracts])
def training_dataset_fingerprint() -> dict[str, Any]:
    training_frame = load_training_data(settings.raw_data_path)
    fingerprint = fingerprint_dataframe(training_frame)
    return {
        "fingerprint": fingerprint,
        "row_count": int(len(training_frame)),
        "source": "duckdb:ml_student_training_set",
        "changed": data_changed(fingerprint),
    }


@asset(
    config_schema={
        "force_train": Field(
            bool,
            default_value=False,
            description="Retrain even when the dataset fingerprint has not changed.",
        )
    },
)
def train_student_score_model(
    context,
    training_dataset_fingerprint: dict[str, Any],
) -> dict[str, Any]:
    force_train = bool(context.op_config.get("force_train", False))
    should_train = force_train or bool(training_dataset_fingerprint["changed"])

    if not should_train:
        context.log.info("Dataset fingerprint is unchanged; skipping model retraining.")
        return {
            "status": "skipped",
            "reason": "dataset_unchanged",
            **training_dataset_fingerprint,
        }

    result = train(dataset_fingerprint=training_dataset_fingerprint["fingerprint"])
    return {
        "status": "trained",
        **training_dataset_fingerprint,
        "metrics": {
            "mae": result["mae"],
            "rmse": result["rmse"],
            "r2": result["r2"],
            "passed_thresholds": result["passed_thresholds"],
        },
        "registered_model_name": result["registered_model_name"],
    }


daily_student_score_job = define_asset_job(
    name="daily_student_score_pipeline",
    selection=AssetSelection.assets(
        check_raw_data_freshness,
        ingest_raw_student_data,
        transform_student_data,
        validate_student_data,
        validate_python_contracts,
        training_dataset_fingerprint,
        train_student_score_model,
    ),
)


daily_student_score_schedule = ScheduleDefinition(
    job=daily_student_score_job,
    cron_schedule="0 2 * * *",
    execution_timezone="Africa/Casablanca",
    run_config={
        "ops": {
            "train_student_score_model": {
                "config": {
                    "force_train": False,
                }
            }
        }
    },
)


defs = Definitions(
    assets=[
        check_raw_data_freshness,
        ingest_raw_student_data,
        transform_student_data,
        validate_student_data,
        validate_python_contracts,
        training_dataset_fingerprint,
        train_student_score_model,
    ],
    jobs=[daily_student_score_job],
    schedules=[daily_student_score_schedule],
)
