from pathlib import Path
import json

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

FEATURES_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "clustering_features.csv"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "kmeans_final.joblib"
)

METRICS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "kmeans_metrics.json"
)

MLRUNS_DIR = (
    PROJECT_ROOT
    / "mlruns"
)


N_CLUSTERS = 2
RANDOM_STATE = 42
N_INIT = 10


def main():

    print("=" * 60)
    print("MLFLOW - ENTRAINEMENT K-MEANS")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. CONFIGURATION MLFLOW
    # ---------------------------------------------------------

    mlruns_uri = MLRUNS_DIR.resolve().as_uri()

    mlflow.set_tracking_uri(
        mlruns_uri
    )

    mlflow.set_experiment(
        "EduCluster-KMeans"
    )

    print()
    print(
        f"MLflow tracking URI : {mlruns_uri}"
    )

    # ---------------------------------------------------------
    # 2. CHARGEMENT DES DONNEES
    # ---------------------------------------------------------

    if not FEATURES_PATH.exists():
        raise FileNotFoundError(
            f"Features introuvables : {FEATURES_PATH}"
        )

    X = pd.read_csv(
        FEATURES_PATH
    )

    print()
    print(
        f"Dataset : {X.shape}"
    )

    # ---------------------------------------------------------
    # 3. ENTRAINEMENT
    # ---------------------------------------------------------

    with mlflow.start_run(
        run_name="kmeans-final-k2"
    ):

        print()
        print("Entraînement K-Means...")

        model = KMeans(
            n_clusters=N_CLUSTERS,
            random_state=RANDOM_STATE,
            n_init=N_INIT,
        )

        labels = model.fit_predict(
            X
        )

        # -----------------------------------------------------
        # 4. METRIQUES
        # -----------------------------------------------------

        inertia = model.inertia_

        silhouette = silhouette_score(
            X,
            labels,
        )

        davies_bouldin = davies_bouldin_score(
            X,
            labels,
        )

        calinski_harabasz = (
            calinski_harabasz_score(
                X,
                labels,
            )
        )

        # -----------------------------------------------------
        # 5. PARAMETRES
        # -----------------------------------------------------

        mlflow.log_params(
            {
                "algorithm": "KMeans",
                "n_clusters": N_CLUSTERS,
                "random_state": RANDOM_STATE,
                "n_init": N_INIT,
                "n_samples": X.shape[0],
                "n_features": X.shape[1],
            }
        )

        # -----------------------------------------------------
        # 6. LOG DES METRIQUES
        # -----------------------------------------------------

        mlflow.log_metrics(
            {
                "inertia": float(inertia),
                "silhouette_score": float(
                    silhouette
                ),
                "davies_bouldin_score": float(
                    davies_bouldin
                ),
                "calinski_harabasz_score": float(
                    calinski_harabasz
                ),
            }
        )

        # -----------------------------------------------------
        # 7. LOG DU MODELE
        # -----------------------------------------------------

        mlflow.sklearn.log_model(
            model,
            "kmeans_model",
        )

        # -----------------------------------------------------
        # 8. LOG DES ARTEFACTS
        # -----------------------------------------------------

        if MODEL_PATH.exists():

            mlflow.log_artifact(
                str(MODEL_PATH),
                artifact_path="models",
            )

        if METRICS_PATH.exists():

            mlflow.log_artifact(
                str(METRICS_PATH),
                artifact_path="metrics",
            )

        # -----------------------------------------------------
        # 9. INFORMATIONS DU RUN
        # -----------------------------------------------------

        run = mlflow.active_run()

        print()
        print("Run MLflow terminé.")

        print()
        print(
            f"Run ID : {run.info.run_id}"
        )

        print()
        print("Métriques :")

        print(
            f"  Inertia             : "
            f"{inertia:.4f}"
        )

        print(
            f"  Silhouette          : "
            f"{silhouette:.4f}"
        )

        print(
            f"  Davies-Bouldin      : "
            f"{davies_bouldin:.4f}"
        )

        print(
            f"  Calinski-Harabasz   : "
            f"{calinski_harabasz:.2f}"
        )

    print()
    print("=" * 60)
    print("MLFLOW TERMINE")
    print("=" * 60)


if __name__ == "__main__":
    main()