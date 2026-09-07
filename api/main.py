from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "kmeans_final.joblib"
SCALER_PATH = BASE_DIR / "data" / "processed" / "scaler.joblib"


app = FastAPI(
    title="EduCluster API",
    description="API for student learning behavior segmentation",
    version="1.0.0",
)


model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


FEATURES = [
    "total_vle_interactions",
    "total_clicks",
    "active_days",
    "active_weeks",
    "activity_span_days",
    "unique_resource_visits",
    "avg_daily_clicks",
    "median_daily_clicks",
    "max_daily_clicks",
    "clicks_std",
    "avg_clicks_per_event",
    "clicks_content",
    "clicks_forum",
    "clicks_quiz",
    "clicks_wiki",
    "clicks_other",
    "content_ratio",
    "forum_ratio",
    "quiz_ratio",
    "wiki_ratio",
    "other_ratio",
    "assessment_count",
    "expected_assessment_count",
    "submission_rate",
    "avg_assessment_score",
    "min_assessment_score",
    "max_assessment_score",
    "assessment_score_std",
    "late_submission_count",
    "late_submission_rate",
    "avg_submission_delay",
    "median_submission_delay",
    "max_submission_delay",
    "on_time_submission_rate",
]


COUNT_FEATURES = {
    "total_vle_interactions",
    "total_clicks",
    "active_days",
    "active_weeks",
    "activity_span_days",
    "unique_resource_visits",
    "avg_daily_clicks",
    "median_daily_clicks",
    "max_daily_clicks",
    "clicks_std",
    "avg_clicks_per_event",
    "clicks_content",
    "clicks_forum",
    "clicks_quiz",
    "clicks_wiki",
    "clicks_other",
    "assessment_count",
    "expected_assessment_count",
    "late_submission_count",
    "avg_submission_delay",
    "median_submission_delay",
    "max_submission_delay",
}


CLUSTER_NAMES = {
    0: "Active / Engaged Learner",
    1: "Low-Engagement / At-Risk Learner",
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

        X = np.array(values).reshape(1, -1)

        X_scaled = scaler.transform(X)

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