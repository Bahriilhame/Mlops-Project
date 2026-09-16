from pathlib import Path
import os

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from api.dashboard import model_information, router as dashboard_router
from scripts.validate_model_bundle import validate_bundle


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "kmeans_final.joblib"
SCALER_PATH = BASE_DIR / "data" / "processed" / "scaler.joblib"
MANIFEST = validate_bundle(BASE_DIR)


app = FastAPI(
    title="EduCluster API",
    description="API for student learning behavior segmentation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://localhost:4173,http://localhost:8080"
    ).split(",") if origin.strip()],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
app.include_router(dashboard_router)


model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


FEATURES = MANIFEST["features"]
COUNT_FEATURES = set(MANIFEST["count_features"])
CLUSTER_NAMES = {
    int(cluster): profile
    for cluster, profile in MANIFEST["cluster_profiles"].items()
}


class StudentFeatures(BaseModel):
    total_vle_interactions: float
    total_clicks: float
    active_days: float
    active_weeks: float
    activity_span_days: float
    unique_resource_visits: float
    avg_daily_clicks: float
    median_daily_clicks: float
    max_daily_clicks: float
    clicks_std: float
    avg_clicks_per_event: float
    clicks_content: float
    clicks_forum: float
    clicks_quiz: float
    clicks_wiki: float
    clicks_other: float
    content_ratio: float
    forum_ratio: float
    quiz_ratio: float
    wiki_ratio: float
    other_ratio: float
    assessment_count: float
    expected_assessment_count: float
    submission_rate: float
    avg_assessment_score: float
    min_assessment_score: float
    max_assessment_score: float
    assessment_score_std: float
    late_submission_count: float
    late_submission_rate: float
    avg_submission_delay: float
    median_submission_delay: float
    max_submission_delay: float
    on_time_submission_rate: float


if list(StudentFeatures.model_fields) != FEATURES:
    raise RuntimeError(
        "Le schéma de l'API ne correspond pas à l'ordre des features du bundle."
    )


@app.get("/")
def root():
    return {
        "name": "EduCluster API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": "kmeans_final.joblib",
        "clusters": 2,
        "model_version": MANIFEST["model_version"],
        "model_sha256": MANIFEST["model_sha256"],
    }


@app.post("/predict")
def predict(student: StudentFeatures):
    try:
        data = student.model_dump()

        values = []

        for feature in FEATURES:
            value = float(data[feature])

            if feature in COUNT_FEATURES:
                value = np.log1p(max(value, 0))

            values.append(value)

        X = pd.DataFrame([values], columns=FEATURES)

        X_scaled = scaler.transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=FEATURES)

        cluster = int(model.predict(X_scaled)[0])

        return {
            "cluster": cluster,
            "profile": CLUSTER_NAMES.get(
                cluster,
                f"Cluster {cluster}"
            ),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@app.get("/model-info")
def model_info():
    info = model_information(model, len(FEATURES))
    info.update({
        "model_version": MANIFEST["model_version"],
        "model_sha256": MANIFEST["model_sha256"],
        "training_commit": MANIFEST["training_git_commit"],
    })
    return info
