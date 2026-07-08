from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from src.student_score_mlops.config import settings
from src.student_score_mlops.data import FEATURE_COLUMNS
from src.student_score_mlops.schemas import StudentFeatures, grade_from_score


def latest_approved_model_path() -> Path:
    return settings.model_path


def load_model(model_path: Path | None = None):
    model_path = model_path or latest_approved_model_path()
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}. Run training before starting the API."
        )
    return joblib.load(model_path)


def model_metadata(model_path: Path | None = None, loaded_at: str | None = None) -> dict[str, Any]:
    model_path = model_path or latest_approved_model_path()
    metrics: dict[str, Any] | None = None
    fingerprint: dict[str, Any] | None = None

    if settings.metrics_path.exists():
        metrics = json.loads(settings.metrics_path.read_text(encoding="utf-8"))

    if settings.data_fingerprint_path.exists():
        fingerprint = json.loads(settings.data_fingerprint_path.read_text(encoding="utf-8"))

    return {
        "model_path": str(model_path),
        "model_exists": model_path.exists(),
        "loaded_at": loaded_at,
        "metrics": metrics,
        "dataset_fingerprint": fingerprint,
        "reported_at": datetime.now(UTC).isoformat(),
    }


def predict_score(model, features: StudentFeatures) -> tuple[float, str]:
    frame = pd.DataFrame([features.model_dump()], columns=FEATURE_COLUMNS)
    predicted_score = float(model.predict(frame)[0])
    predicted_score = max(0.0, min(100.0, predicted_score))
    return predicted_score, grade_from_score(predicted_score)
