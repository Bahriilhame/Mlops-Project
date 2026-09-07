from __future__ import annotations

import time
from datetime import UTC, datetime

from fastapi import FastAPI

from src.student_score_mlops.monitoring import log_prediction
from src.student_score_mlops.predict import load_model, model_metadata, predict_score
from src.student_score_mlops.schemas import PredictionResponse, StudentFeatures

app = FastAPI(title="EduScore MLOps API", version="0.1.0")
model = None
model_loaded_at = None


@app.on_event("startup")
def startup_event() -> None:
    global model, model_loaded_at
    model = load_model()
    model_loaded_at = datetime.now(UTC).isoformat()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/model-info")
def model_info() -> dict:
    return model_metadata(loaded_at=model_loaded_at)


@app.post("/predict", response_model=PredictionResponse)
def predict(features: StudentFeatures) -> PredictionResponse:
    start = time.perf_counter()
    predicted_score, predicted_grade = predict_score(model, features)
    latency_ms = (time.perf_counter() - start) * 1000
    log_prediction(features.model_dump(), predicted_score, predicted_grade, latency_ms)
    return PredictionResponse(
        predicted_score=round(predicted_score, 2),
        predicted_grade=predicted_grade,
    )
