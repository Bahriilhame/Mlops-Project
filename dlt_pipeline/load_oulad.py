from pathlib import Path

import dlt
import pandas as pd


DATA_DIR = Path("data/raw/oulad")


FILES = {
    "student_info": "studentInfo.csv",
    "student_assessment": "studentAssessment.csv",
    "student_vle": "studentVle.csv",
    "student_registration": "studentRegistration.csv",
    "assessments": "assessments.csv",
    "courses": "courses.csv",
    "vle": "vle.csv",
}


def load_csv(filename: str):
    path = DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"OULAD file not found: {path}"
        )

    return pd.read_csv(path)


@dlt.resource(
    name="student_info",
    write_disposition="replace",
)
def student_info():
    yield load_csv(FILES["student_info"])


@dlt.resource(
    name="student_assessment",
    write_disposition="replace",
)
def student_assessment():
    yield load_csv(FILES["student_assessment"])


@dlt.resource(
    name="student_vle",
    write_disposition="replace",
)
def student_vle():
    yield load_csv(FILES["student_vle"])


@dlt.resource(
    name="student_registration",
    write_disposition="replace",
)
def student_registration():
    yield load_csv(FILES["student_registration"])


@dlt.resource(
    name="assessments",
    write_disposition="replace",
)
def assessments():
    yield load_csv(FILES["assessments"])


@dlt.resource(
    name="courses",
    write_disposition="replace",
)
def courses():
    yield load_csv(FILES["courses"])


@dlt.resource(
    name="vle",
    write_disposition="replace",
)
def vle():
    yield load_csv(FILES["vle"])


def main():

    pipeline = dlt.pipeline(
        pipeline_name="oulad_pipeline",
        destination="duckdb",
        dataset_name="raw",
    )

    load_info = pipeline.run(
        [
            student_info(),
            student_assessment(),
            student_vle(),
            student_registration(),
            assessments(),
            courses(),
            vle(),
        ]
    )

    print(load_info)


if __name__ == "__main__":
    main()