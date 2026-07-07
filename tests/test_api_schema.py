import pytest
from pydantic import ValidationError

from src.student_score_mlops.schemas import StudentFeatures


def test_student_features_valid_payload():
    payload = StudentFeatures(
        study_hours=12,
        attendance_percentage=88,
        class_participation=7,
    )

    assert payload.study_hours == 12


def test_student_features_rejects_invalid_attendance():
    with pytest.raises(ValidationError):
        StudentFeatures(
            study_hours=12,
            attendance_percentage=120,
            class_participation=7,
        )
