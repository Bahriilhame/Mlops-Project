from __future__ import annotations

import joblib
import pandas as pd

from src.student_score_mlops.config import settings
from src.student_score_mlops.data import FEATURE_COLUMNS
from src.student_score_mlops.schemas import StudentFeatures, grade_from_score


def load_model():
    if not settings.model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {settings.model_path}. Run training before starting the API."
        )
    return joblib.load(settings.model_path)


def predict_score(model, features: StudentFeatures) -> tuple[float, str]:
    frame = pd.DataFrame([features.model_dump()], columns=FEATURE_COLUMNS)
    predicted_score = float(model.predict(frame)[0])
    predicted_score = max(0.0, min(100.0, predicted_score))
    return predicted_score, grade_from_score(predicted_score)
