from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import pandas as pd

from src.student_score_mlops.config import settings
from src.student_score_mlops.data import FEATURE_COLUMNS


def log_prediction(
    features: dict[str, Any],
    predicted_score: float,
    predicted_grade: str,
    latency_ms: float,
    log_path: Path = settings.prediction_log_path,
) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": time.time(),
        "features": features,
        "predicted_score": predicted_score,
        "predicted_grade": predicted_grade,
        "latency_ms": latency_ms,
    }
    with log_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event) + "\n")


def simple_drift_status(current_mean: float, reference_mean: float, threshold: float = 10.0) -> str:
    difference = abs(current_mean - reference_mean)
    if difference > threshold:
        return "drift_alert"
    return "ok"


def load_prediction_events(
    log_path: Path = settings.prediction_log_path,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    if not log_path.exists():
        return []

    lines = log_path.read_text(encoding="utf-8").splitlines()
    if limit is not None:
        lines = lines[-limit:]
    return [json.loads(line) for line in lines if line.strip()]


def feature_means_from_prediction_log(
    log_path: Path = settings.prediction_log_path,
    limit: int = 500,
) -> dict[str, float]:
    events = load_prediction_events(log_path, limit=limit)
    rows = [event.get("features", {}) for event in events]
    if not rows:
        return {}
    frame = pd.DataFrame(rows)
    return {
        column: float(frame[column].mean())
        for column in FEATURE_COLUMNS
        if column in frame.columns
    }


def drift_report(
    reference_path: Path = settings.training_reference_path,
    prediction_log_path: Path = settings.prediction_log_path,
    threshold: float = 10.0,
    limit: int = 500,
) -> dict[str, Any]:
    if not reference_path.exists():
        return {"status": "missing_reference", "features": {}}

    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    reference_means = reference.get("feature_means", {})
    current_means = feature_means_from_prediction_log(prediction_log_path, limit=limit)
    features: dict[str, Any] = {}

    for column in FEATURE_COLUMNS:
        if column not in reference_means or column not in current_means:
            continue
        difference = abs(current_means[column] - reference_means[column])
        features[column] = {
            "reference_mean": reference_means[column],
            "current_mean": current_means[column],
            "absolute_difference": difference,
            "status": simple_drift_status(current_means[column], reference_means[column], threshold),
        }

    status = "drift_alert" if any(item["status"] == "drift_alert" for item in features.values()) else "ok"
    return {"status": status, "features": features}
