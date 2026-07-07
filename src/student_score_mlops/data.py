from __future__ import annotations

from pathlib import Path

import pandas as pd


COLUMN_ALIASES = {
    "study_hours": [
        "average_weekly_self_study_hours",
        "weekly_self_study_hours",
        "study_hours",
        "hours_studied",
        "average weekly self study hours",
    ],
    "attendance_percentage": [
        "attendance_percentage",
        "attendance",
        "attendance_rate",
        "attendance percentage",
    ],
    "class_participation": [
        "class_participation",
        "participation",
        "participation_score",
        "class participation",
    ],
    "total_score": [
        "total_score",
        "final_score",
        "score",
        "performance_score",
        "final performance score",
    ],
    "grade": ["grade", "final_grade"],
}

FEATURE_COLUMNS = ["study_hours", "attendance_percentage", "class_participation"]
TARGET_COLUMN = "total_score"


def normalize_column_name(column: str) -> str:
    return (
        column.strip()
        .lower()
        .replace("%", "percentage")
        .replace("-", "_")
        .replace("/", "_")
        .replace(" ", "_")
    )


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    normalized_to_original = {normalize_column_name(col): col for col in df.columns}
    rename_map: dict[str, str] = {}

    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            normalized_alias = normalize_column_name(alias)
            if normalized_alias in normalized_to_original:
                rename_map[normalized_to_original[normalized_alias]] = canonical
                break

    return df.rename(columns=rename_map)


def load_dataset(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return standardize_columns(df)


def validate_training_frame(df: pd.DataFrame) -> None:
    required = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    ranges = {
        "study_hours": (0, 40),
        "attendance_percentage": (0, 100),
        "class_participation": (0, 10),
        "total_score": (0, 100),
    }
    for column, (minimum, maximum) in ranges.items():
        invalid_count = (~df[column].between(minimum, maximum)).sum()
        if invalid_count:
            raise ValueError(f"{column} has {invalid_count} values outside [{minimum}, {maximum}]")


def feature_target_split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    validate_training_frame(df)
    features = df[FEATURE_COLUMNS].copy()
    target = df[TARGET_COLUMN].copy()
    return features, target
