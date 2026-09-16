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

import joblib
import mlflow
import mlflow.sklearn

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "kmeans_final.joblib"
REF_RESULTS_PATH = PROJECT_ROOT / "api" / "reference_results.json"
DEFAULT_MLRUNS = PROJECT_ROOT / "mlruns"


def main():
    if len(sys.argv) > 1 and sys.argv[1].startswith("http"):
        tracking_uri = sys.argv[1]
    else:
        DEFAULT_MLRUNS.mkdir(exist_ok=True)
        tracking_uri = DEFAULT_MLRUNS.resolve().as_uri()

    print(f"Connecting to MLflow at: {tracking_uri}")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("EduCluster-KMeans")

    with open(REF_RESULTS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    model = joblib.load(MODEL_PATH)

    with mlflow.start_run(run_name="kmeans-final-k2"):
        print("Logging parameters...")
        mlflow.log_params({
            "algorithm": metrics.get("model", "KMeans"),
            "n_clusters": metrics.get("n_clusters", 2),
            "n_features": metrics.get("n_features", 34),
            "n_samples": metrics.get("n_samples", 32593),
            "random_state": 42,
            "n_init": 10,
        })

        print("Logging evaluation metrics...")
        mlflow.log_metrics({
            "silhouette_score": float(metrics.get("silhouette_score", 0.4569)),
            "davies_bouldin_score": float(metrics.get("davies_bouldin_score", 0.9109)),
            "calinski_harabasz_score": float(metrics.get("calinski_harabasz_score", 24838.61)),
            "inertia": float(getattr(model, "inertia_", 0.0)),
        })

        print("Logging model artifact...")
        mlflow.sklearn.log_model(model, "kmeans_model")

        print("Tagging run...")
        mlflow.set_tags({
            "dataset": "OULAD",
            "task": "student_clustering",
            "status": "production",
        })

    print("Success! MLflow experiment 'EduCluster-KMeans' is now populated.")


if __name__ == "__main__":
    main()

