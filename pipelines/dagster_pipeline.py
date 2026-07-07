from __future__ import annotations

import os
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DAGSTER_HOME = PROJECT_ROOT / ".dagster_home"
DAGSTER_HOME.mkdir(exist_ok=True)
os.environ.setdefault("DAGSTER_HOME", str(DAGSTER_HOME))

from dagster import Definitions, asset

from dlt_pipeline.load_student_data import run_pipeline
from src.student_score_mlops.train import train


@asset
def ingest_raw_student_data() -> str:
    run_pipeline()
    return "raw_data_loaded"


@asset(deps=[ingest_raw_student_data])
def transform_student_data() -> str:
    subprocess.run(
        [
            "dbt",
            "run",
            "--project-dir",
            "dbt/student_score",
            "--profiles-dir",
            "dbt/student_score",
        ],
        check=True,
    )
    subprocess.run(
        [
            "dbt",
            "test",
            "--project-dir",
            "dbt/student_score",
            "--profiles-dir",
            "dbt/student_score",
        ],
        check=True,
    )
    return "dbt_models_built"


@asset(deps=[transform_student_data])
def train_student_score_model() -> dict[str, float]:
    return train()


defs = Definitions(
    assets=[
        ingest_raw_student_data,
        transform_student_data,
        train_student_score_model,
    ]
)
