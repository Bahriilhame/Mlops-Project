from __future__ import annotations

import json
from pathlib import Path

import joblib
import mlflow
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.student_score_mlops.config import settings
from src.student_score_mlops.data import feature_target_split, load_dataset


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


def train(data_path: Path = settings.raw_data_path) -> dict[str, float]:
    df = load_training_data(data_path)
    features, target = feature_target_split(df)

    x_train, x_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )

    model = build_model()

    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment(settings.mlflow_experiment_name)

    with mlflow.start_run(run_name="random-forest-regressor"):
        mlflow.log_params(
            {
                "model_type": "RandomForestRegressor",
                "n_estimators": 200,
                "max_depth": 8,
                "test_size": 0.2,
                "random_state": 42,
            }
        )

        model.fit(x_train, y_train)
        predictions = model.predict(x_test)

        metrics = {
            "mae": float(mean_absolute_error(y_test, predictions)),
            "rmse": float(np.sqrt(mean_squared_error(y_test, predictions))),
            "r2": float(r2_score(y_test, predictions)),
        }
        mlflow.log_metrics(metrics)

        settings.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, settings.model_path)
        mlflow.sklearn.log_model(model, artifact_path="model")
        mlflow.log_artifact(str(settings.model_path))

        settings.metrics_path.parent.mkdir(parents=True, exist_ok=True)
        settings.metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
        mlflow.log_artifact(str(settings.metrics_path))

    return metrics


if __name__ == "__main__":
    print(json.dumps(train(), indent=2))
