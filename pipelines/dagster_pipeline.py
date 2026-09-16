# from pathlib import Path
# import subprocess
# import sys

# from dagster import (
#     Definitions,
#     job,
#     op,
# )


# PROJECT_ROOT = Path(__file__).resolve().parent.parent


# @op
# def run_dlt():

#     print("=" * 60)
#     print("STEP 1 - DLT")
#     print("=" * 60)

#     script = (
#         PROJECT_ROOT
#         / "dlt_pipeline"
#         / "load_oulad.py"
#     )

#     subprocess.run(
#         [sys.executable, str(script)],
#         cwd=PROJECT_ROOT,
#         check=True,
#     )

#     print("DLT terminé.")

#     return "dlt_completed"


# @op
# def run_dbt(dlt_result):

#     print("=" * 60)
#     print("STEP 2 - DBT")
#     print("=" * 60)

#     dbt_project = (
#         PROJECT_ROOT
#         / "dbt"
#         / "educluster"
#     )

#     subprocess.run(
#         [
#             "dbt",
#             "run",
#         ],
#         cwd=dbt_project,
#         check=True,
#         shell=True,
#     )

#     print("dbt terminé.")

#     return "dbt_completed"


# @op
# def prepare_features(dbt_result):

#     print("=" * 60)
#     print("STEP 3 - PREPARATION DES FEATURES")
#     print("=" * 60)

#     script = (
#         PROJECT_ROOT
#         / "ml"
#         / "prepare_data.py"
#     )

#     subprocess.run(
#         [sys.executable, str(script)],
#         cwd=PROJECT_ROOT,
#         check=True,
#     )

#     print("Features préparées.")

#     return "features_completed"


# @op
# def train_kmeans(features_result):

#     print("=" * 60)
#     print("STEP 4 - K-MEANS")
#     print("=" * 60)

#     script = (
#         PROJECT_ROOT
#         / "ml"
#         / "clustering.py"
#     )

#     subprocess.run(
#         [sys.executable, str(script)],
#         cwd=PROJECT_ROOT,
#         check=True,
#     )

#     print("K-Means terminé.")

#     return "kmeans_completed"


# @op
# def train_mlflow(kmeans_result):

#     print("=" * 60)
#     print("STEP 5 - MLFLOW")
#     print("=" * 60)

#     script = (
#         PROJECT_ROOT
#         / "ml"
#         / "train_mlflow.py"
#     )

#     subprocess.run(
#         [sys.executable, str(script)],
#         cwd=PROJECT_ROOT,
#         check=True,
#     )

#     print("MLflow terminé.")


# @job
# def educluster_pipeline():

#     dlt_result = run_dlt()

#     dbt_result = run_dbt(
#         dlt_result
#     )

#     features_result = prepare_features(
#         dbt_result
#     )

#     kmeans_result = train_kmeans(
#         features_result
#     )

#     train_mlflow(
#         kmeans_result
#     )


# defs = Definitions(
#     jobs=[
#         educluster_pipeline,
#     ],
# )






from pathlib import Path
import csv
import json
import os
import subprocess
import sys

from dagster import asset, Definitions, MaterializeResult, MetadataValue


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DLT_SCRIPT = PROJECT_ROOT / "dlt_pipeline" / "load_oulad.py"
DBT_PROJECT = PROJECT_ROOT / "dbt" / "educluster"

FEATURE_SCRIPT = PROJECT_ROOT / "ml" / "prepare_data.py"
KMEANS_SCRIPT = PROJECT_ROOT / "ml" / "clustering.py"
MLFLOW_SCRIPT = PROJECT_ROOT / "scripts" / "log_to_mlflow.py"

DUCKDB_PATH = Path(
    os.getenv("EDUCLUSTER_DUCKDB_PATH", str(PROJECT_ROOT / "oulad_pipeline.duckdb"))
)

FEATURES_PATH = PROJECT_ROOT / "data" / "processed" / "clustering_features.csv"
SCALER_PATH = PROJECT_ROOT / "data" / "processed" / "scaler.joblib"

KMEANS_MODEL_PATH = PROJECT_ROOT / "models" / "kmeans_final.joblib"
KMEANS_METRICS_PATH = (
    PROJECT_ROOT / "data" / "processed" / "kmeans_metrics.json"
)

CLUSTERED_STUDENTS_PATH = (
    PROJECT_ROOT / "data" / "processed" / "clustered_students.csv"
)

CLUSTER_PROFILES_PATH = (
    PROJECT_ROOT / "data" / "processed" / "cluster_profiles.csv"
)

CLUSTER_FINAL_RESULT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "cluster_final_result_profile.csv"
)


def csv_shape(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.reader(stream)
        header = next(reader)
        return sum(1 for _ in reader), len(header)


def read_metrics() -> dict:
    with KMEANS_METRICS_PATH.open("r", encoding="utf-8") as stream:
        return json.load(stream)


# ============================================================
# ASSET 1 — DLT
# ============================================================

@asset(
    name="oulad_raw",
    description="OULAD raw data ingested by DLT into DuckDB."
)
def oulad_raw() -> MaterializeResult:

    print("=" * 60)
    print("ASSET 1 - DLT / OULAD RAW")
    print("=" * 60)

    subprocess.run(
        [sys.executable, str(DLT_SCRIPT)],
        cwd=PROJECT_ROOT,
        check=True,
    )

    print("DLT terminé.")

    return MaterializeResult(
        metadata={
            "destination": MetadataValue.path(str(DUCKDB_PATH)),
            "dataset": "raw",
            "database": MetadataValue.path(str(DUCKDB_PATH)),
        }
    )


# ============================================================
# ASSET 2 — DBT
# ============================================================

@asset(
    name="student_learning_features",
    deps=[oulad_raw],
    description="Student learning features generated by dbt."
)
def student_learning_features() -> MaterializeResult:

    print("=" * 60)
    print("ASSET 2 - DBT")
    print("=" * 60)

    subprocess.run(
        [
            "dbt", "build", "--project-dir", str(DBT_PROJECT),
            "--profiles-dir", str(PROJECT_ROOT / "dbt"),
        ],
        cwd=PROJECT_ROOT,
        check=True,
    )

    print("dbt terminé.")

    return MaterializeResult(
        metadata={
            "database": MetadataValue.path(str(DUCKDB_PATH)),
            "table": "main.student_learning_features",
            "validation": "dbt build (models + tests) passed",
        }
    )


# ============================================================
# ASSET 3 — FEATURES
# ============================================================

@asset(
    name="clustering_features",
    deps=[student_learning_features],
    description="Standardized behavioral features used for clustering."
)
def clustering_features() -> MaterializeResult:

    print("=" * 60)
    print("ASSET 3 - FEATURE ENGINEERING")
    print("=" * 60)

    subprocess.run(
        [sys.executable, str(FEATURE_SCRIPT)],
        cwd=PROJECT_ROOT,
        check=True,
    )

    print("Features préparées.")

    rows, columns = csv_shape(FEATURES_PATH)

    return MaterializeResult(
        metadata={
            "file": MetadataValue.path(str(FEATURES_PATH)),
            "scaler": MetadataValue.path(str(SCALER_PATH)),
            "rows": rows,
            "features": columns,
        }
    )


# ============================================================
# ASSET 4 — K-MEANS
# ============================================================

@asset(
    name="kmeans_model",
    deps=[clustering_features],
    description="Final K-Means clustering model with two student profiles."
)
def kmeans_model() -> MaterializeResult:

    print("=" * 60)
    print("ASSET 4 - K-MEANS")
    print("=" * 60)

    subprocess.run(
        [sys.executable, str(KMEANS_SCRIPT)],
        cwd=PROJECT_ROOT,
        check=True,
    )

    print("K-Means terminé.")

    metrics = read_metrics()

    return MaterializeResult(
        metadata={
            "model": MetadataValue.path(str(KMEANS_MODEL_PATH)),
            "metrics": MetadataValue.path(str(KMEANS_METRICS_PATH)),
            "clustered_students": MetadataValue.path(
                str(CLUSTERED_STUDENTS_PATH)
            ),
            "cluster_profiles": MetadataValue.path(
                str(CLUSTER_PROFILES_PATH)
            ),
            "final_result_profile": MetadataValue.path(
                str(CLUSTER_FINAL_RESULT_PATH)
            ),
            "n_clusters": metrics["n_clusters"],
            "n_students": metrics["n_samples"],
            "n_features": metrics["n_features"],
            "silhouette": metrics["silhouette_score"],
            "davies_bouldin": metrics["davies_bouldin_score"],
            "calinski_harabasz": metrics["calinski_harabasz_score"],
        }
    )


# ============================================================
# ASSET 5 — MLFLOW
# ============================================================

@asset(
    name="mlflow_kmeans_experiment",
    deps=[kmeans_model],
    description="K-Means experiment tracked and versioned with MLflow."
)
def mlflow_kmeans_experiment() -> MaterializeResult:

    print("=" * 60)
    print("ASSET 5 - MLFLOW")
    print("=" * 60)

    subprocess.run(
        [sys.executable, str(MLFLOW_SCRIPT)],
        cwd=PROJECT_ROOT,
        check=True,
    )

    print("MLflow terminé.")

    metrics = read_metrics()

    return MaterializeResult(
        metadata={
            "experiment": "EduCluster-KMeans",
            "tracking_directory": MetadataValue.path(
                str(PROJECT_ROOT / "mlruns")
            ),
            "model": MetadataValue.path(str(KMEANS_MODEL_PATH)),
            "silhouette": metrics["silhouette_score"],
            "davies_bouldin": metrics["davies_bouldin_score"],
            "calinski_harabasz": metrics["calinski_harabasz_score"],
        }
    )


# ============================================================
# DAGSTER DEFINITIONS
# ============================================================

defs = Definitions(
    assets=[
        oulad_raw,
        student_learning_features,
        clustering_features,
        kmeans_model,
        mlflow_kmeans_experiment,
    ]
)
