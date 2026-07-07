from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    raw_data_path: Path = PROJECT_ROOT / os.getenv(
        "RAW_DATA_PATH", "data/raw/student_performance.csv"
    )
    duckdb_path: Path = PROJECT_ROOT / os.getenv(
        "DUCKDB_PATH", "data/student_score.duckdb"
    )
    model_path: Path = PROJECT_ROOT / os.getenv(
        "MODEL_PATH", "models/student_score_model.joblib"
    )
    metrics_path: Path = PROJECT_ROOT / os.getenv("METRICS_PATH", "models/metrics.json")
    mlflow_tracking_uri: str = os.getenv("MLFLOW_TRACKING_URI", "mlruns")
    mlflow_experiment_name: str = os.getenv(
        "MLFLOW_EXPERIMENT_NAME", "eduscore-student-performance"
    )
    prediction_log_path: Path = PROJECT_ROOT / os.getenv(
        "PREDICTION_LOG_PATH", "monitoring/predictions.jsonl"
    )


settings = Settings()
