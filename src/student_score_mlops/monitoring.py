from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from src.student_score_mlops.config import settings


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
