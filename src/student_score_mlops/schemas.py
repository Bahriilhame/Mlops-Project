from __future__ import annotations

from pydantic import BaseModel, Field


class StudentFeatures(BaseModel):
    study_hours: float = Field(..., ge=0, le=40)
    attendance_percentage: float = Field(..., ge=0, le=100)
    class_participation: float = Field(..., ge=0, le=10)


class PredictionResponse(BaseModel):
    predicted_score: float
    predicted_grade: str


def grade_from_score(score: float) -> str:
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 55:
        return "C"
    if score >= 40:
        return "D"
    return "F"
