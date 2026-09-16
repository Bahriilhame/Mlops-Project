"""Log the existing EduCluster K-Means model and metrics into MLflow.

Usage:
  # Against local mlruns directory:
  python scripts/log_to_mlflow.py

  # Against deployed Komodo MLflow server:
  python scripts/log_to_mlflow.py http://<SERVER_IP>:4202
"""
from pathlib import Path
import json
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

from scripts.validate_model_bundle import validate_bundle

MODEL_PATH = PROJECT_ROOT / "models" / "kmeans_final.joblib"
REF_RESULTS_PATH = PROJECT_ROOT / "api" / "reference_results.json"
SCALER_PATH = PROJECT_ROOT / "data" / "processed" / "scaler.joblib"
MANIFEST_PATH = PROJECT_ROOT / "models" / "model_manifest.json"
DEFAULT_MLRUNS = PROJECT_ROOT / "mlruns"


def main(tracking_uri_override=None):
    if tracking_uri_override:
        tracking_uri = tracking_uri_override
    elif len(sys.argv) > 1:
        tracking_uri = sys.argv[1]
    else:
        DEFAULT_MLRUNS.mkdir(exist_ok=True)
        tracking_uri = DEFAULT_MLRUNS.resolve().as_uri()

    manifest = validate_bundle(PROJECT_ROOT)
    print(f"Connecting to MLflow at: {tracking_uri}")
    mlflow.set_tracking_uri(tracking_uri)
    experiment = mlflow.set_experiment("EduCluster-KMeans")

    client = MlflowClient()
    model_sha = manifest["model_sha256"]
    existing = client.search_runs(
        [experiment.experiment_id],
        filter_string=f"tags.model_sha256 = '{model_sha}'",
        max_results=1,
    )
    if existing:
        print(f"Model already logged in MLflow: run {existing[0].info.run_id}")
        return existing[0].info.run_id

    with open(REF_RESULTS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    model = joblib.load(MODEL_PATH)

    required_metrics = (
        "silhouette_score", "davies_bouldin_score",
        "calinski_harabasz_score",
    )
    missing = [key for key in required_metrics if key not in metrics]
    if missing:
        raise ValueError(f"Missing reference metrics: {', '.join(missing)}")

    with mlflow.start_run(run_name=f"kmeans-{manifest['model_version']}") as run:
        print("Logging parameters...")
        mlflow.log_params({
            "algorithm": metrics["model"],
            "n_clusters": metrics["n_clusters"],
            "n_features": metrics["n_features"],
            "n_samples": metrics["n_samples"],
            "random_state": int(getattr(model, "random_state", 42)),
            "n_init": getattr(model, "n_init", 10),
        })

        print("Logging evaluation metrics...")
        mlflow.log_metrics({
            "silhouette_score": float(metrics["silhouette_score"]),
            "davies_bouldin_score": float(metrics["davies_bouldin_score"]),
            "calinski_harabasz_score": float(metrics["calinski_harabasz_score"]),
            "inertia": float(getattr(model, "inertia_")),
        })

        print("Logging model artifact...")
        mlflow.sklearn.log_model(model, "kmeans_model")
        mlflow.log_artifact(str(SCALER_PATH), "preprocessing")
        mlflow.log_artifact(str(MANIFEST_PATH), "bundle")
        mlflow.log_artifact(str(REF_RESULTS_PATH), "evaluation")

        print("Tagging run...")
        mlflow.set_tags({
            "dataset": "OULAD",
            "task": "student_clustering",
            "deployment_stage": "production",
            "bundle_validation": "passed",
            "model_sha256": model_sha,
            "model_version": manifest["model_version"],
            "training_commit": manifest["training_git_commit"],
        })

    print("Success! MLflow experiment 'EduCluster-KMeans' is now populated.")
    return run.info.run_id


if __name__ == "__main__":
    main()

