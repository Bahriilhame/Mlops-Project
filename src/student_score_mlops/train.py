from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
import mlflow
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.student_score_mlops.config import settings
from src.student_score_mlops.data import FEATURE_COLUMNS, feature_target_split, load_dataset
from src.student_score_mlops.data_versioning import (
    fingerprint_dataframe,
    write_fingerprint_metadata,
)


def build_model() -> Pipeline:
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "model",
                RandomForestRegressor(
                    n_estimators=200,
                    max_depth=8,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )


def load_training_data(data_path: Path):
    if settings.duckdb_path.exists():
        try:
            import duckdb

            with duckdb.connect(str(settings.duckdb_path)) as connection:
                return connection.execute("select * from ml_student_training_set").fetchdf()
        except Exception:
            pass

    return load_dataset(data_path)


def metrics_pass_thresholds(metrics: dict[str, float]) -> bool:
    return metrics["r2"] >= settings.min_r2 and metrics["rmse"] <= settings.max_rmse


def write_training_reference(
    df,
    dataset_fingerprint: str,
    path: Path = settings.training_reference_path,
) -> dict[str, Any]:
    reference = {
        "dataset_fingerprint": dataset_fingerprint,
        "row_count": int(len(df)),
        "feature_means": {
            column: float(df[column].mean())
            for column in FEATURE_COLUMNS
            if column in df.columns
        },
        "created_at": datetime.now(UTC).isoformat(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(reference, indent=2), encoding="utf-8")
    return reference


def train(
    data_path: Path = settings.raw_data_path,
    dataset_fingerprint: str | None = None,
    register_model: bool = True,
) -> dict[str, Any]:
    df = load_training_data(data_path)
    dataset_fingerprint = dataset_fingerprint or fingerprint_dataframe(df)
    row_count = int(len(df))
    training_timestamp = datetime.now(UTC).isoformat()
    features, target = feature_target_split(df)

    x_train, x_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )

    model = build_model()

    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment(settings.mlflow_experiment_name)

    with mlflow.start_run(run_name="random-forest-regressor"):
        params = {
            "model_type": "RandomForestRegressor",
            "n_estimators": 200,
            "max_depth": 8,
            "test_size": 0.2,
            "random_state": 42,
            "dataset_fingerprint": dataset_fingerprint,
            "dataset_row_count": row_count,
            "training_timestamp": training_timestamp,
            "min_r2": settings.min_r2,
            "max_rmse": settings.max_rmse,
        }
        mlflow.log_params(params)

        model.fit(x_train, y_train)
        predictions = model.predict(x_test)

        metrics = {
            "mae": float(mean_absolute_error(y_test, predictions)),
            "rmse": float(np.sqrt(mean_squared_error(y_test, predictions))),
            "r2": float(r2_score(y_test, predictions)),
        }
        passed_thresholds = metrics_pass_thresholds(metrics)
        mlflow.log_metrics({**metrics, "passed_thresholds": float(passed_thresholds)})
        mlflow.set_tags(
            {
                "dataset_fingerprint": dataset_fingerprint,
                "training_timestamp": training_timestamp,
                "quality_gate": "passed" if passed_thresholds else "failed",
            }
        )

        settings.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, settings.model_path)
        registered_model_name = (
            settings.mlflow_registered_model_name
            if register_model and passed_thresholds
            else None
        )
        model_info = mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            registered_model_name=registered_model_name,
        )
        mlflow.log_artifact(str(settings.model_path))

        reference = write_training_reference(df, dataset_fingerprint)
        mlflow.log_artifact(str(settings.training_reference_path))

        output = {
            **metrics,
            "passed_thresholds": passed_thresholds,
            "dataset_fingerprint": dataset_fingerprint,
            "dataset_row_count": row_count,
            "training_timestamp": training_timestamp,
            "registered_model_name": registered_model_name,
            "model_uri": model_info.model_uri,
            "training_reference": reference,
        }

        settings.metrics_path.parent.mkdir(parents=True, exist_ok=True)
        settings.metrics_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
        mlflow.log_artifact(str(settings.metrics_path))

    if not passed_thresholds:
        raise RuntimeError(
            "Model failed quality thresholds: "
            f"r2={metrics['r2']:.4f} < {settings.min_r2} or "
            f"rmse={metrics['rmse']:.4f} > {settings.max_rmse}"
        )

    write_fingerprint_metadata(
        fingerprint=dataset_fingerprint,
        row_count=row_count,
        source="duckdb:ml_student_training_set"
        if settings.duckdb_path.exists()
        else str(data_path),
    )

    return output


if __name__ == "__main__":
    print(json.dumps(train(), indent=2))
