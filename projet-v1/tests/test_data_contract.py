import pandas as pd
import pytest

from src.student_score_mlops.data import standardize_columns, validate_training_frame
from src.student_score_mlops.schemas import grade_from_score


def test_standardize_columns_accepts_kaggle_style_names():
    df = pd.DataFrame(
        {
            "Average weekly self study hours": [10],
            "Attendance percentage": [80],
            "Class participation": [6],
            "Final performance score": [75],
            "Grade": ["B"],
        }
    )

    standardized = standardize_columns(df)

    assert {"study_hours", "attendance_percentage", "class_participation", "total_score", "grade"}.issubset(
        standardized.columns
    )


def test_validate_training_frame_rejects_out_of_range_values():
    df = pd.DataFrame(
        {
            "study_hours": [100],
            "attendance_percentage": [80],
            "class_participation": [5],
            "total_score": [70],
        }
    )

    with pytest.raises(ValueError):
        validate_training_frame(df)


@pytest.mark.parametrize(
    ("score", "grade"),
    [(90, "A"), (75, "B"), (60, "C"), (45, "D"), (20, "F")],
)
def test_grade_from_score(score, grade):
    assert grade_from_score(score) == grade
