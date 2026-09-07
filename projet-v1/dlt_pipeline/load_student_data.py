from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def load_student_performance_frame() -> pd.DataFrame:
    from src.student_score_mlops.config import settings
    from src.student_score_mlops.data import standardize_columns

    if not settings.raw_data_path.exists():
        raise FileNotFoundError(
            f"Raw dataset not found at {settings.raw_data_path}. "
            "Download it from Kaggle and place it in data/raw/student_performance.csv."
        )

    return standardize_columns(pd.read_csv(settings.raw_data_path))


def run_pipeline() -> None:
    from src.student_score_mlops.config import settings

    settings.duckdb_path.parent.mkdir(parents=True, exist_ok=True)
    df = load_student_performance_frame()

    with duckdb.connect(str(settings.duckdb_path)) as connection:
        connection.execute("create schema if not exists raw")
        connection.register("student_performance_df", df)
        connection.execute(
            "create or replace table raw.student_performance as "
            "select * from student_performance_df"
        )
        row_count = connection.execute("select count(*) from raw.student_performance").fetchone()[0]

    print(
        f"Loaded {row_count} rows into "
        f"{settings.duckdb_path.as_posix()}::raw.student_performance"
    )


if __name__ == "__main__":
    run_pipeline()
