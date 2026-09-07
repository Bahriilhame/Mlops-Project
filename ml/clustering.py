from pathlib import Path
import json

import duckdb
import joblib
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DUCKDB_PATH = PROJECT_ROOT / "oulad_pipeline.duckdb"

FEATURES_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "clustering_features.csv"
)

CLUSTERS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "clustered_students.csv"
)

PROFILE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cluster_profiles.csv"
)

FINAL_RESULT_PROFILE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cluster_final_result_profile.csv"
)

METRICS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "kmeans_metrics.json"
)

MODEL_DIR = PROJECT_ROOT / "models"

MODEL_PATH = MODEL_DIR / "kmeans_final.joblib"

N_CLUSTERS = 2
RANDOM_STATE = 42


def load_student_metadata() -> pd.DataFrame:
    """Charge les informations étudiantes depuis le mart dbt."""

    if not DUCKDB_PATH.exists():
        raise FileNotFoundError(
            f"DuckDB introuvable : {DUCKDB_PATH}"
        )

    con = duckdb.connect(str(DUCKDB_PATH))

    query = """
        SELECT
            id_student,
            code_module,
            code_presentation,
            gender,
            region,
            highest_education,
            imd_band,
            age_band,
            num_of_prev_attempts,
            studied_credits,
            disability,
            final_result
        FROM main.student_learning_features
    """

    df = con.execute(query).df()
    con.close()

    return df


def main():

    print("=" * 60)
    print("K-MEANS - MODÈLE FINAL")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. CHARGEMENT DES FEATURES
    # ---------------------------------------------------------

    if not FEATURES_PATH.exists():
        raise FileNotFoundError(
            f"Features introuvables : {FEATURES_PATH}"
        )

    X = pd.read_csv(FEATURES_PATH)

    print()
    print(f"Dataset : {X.shape}")
    print(f"Nombre de features : {X.shape[1]}")

    if X.isnull().sum().sum() > 0:
        raise ValueError(
            "Le dataset contient des valeurs manquantes."
        )

    # ---------------------------------------------------------
    # 2. CHARGEMENT DES INFORMATIONS ETUDIANTES
    # ---------------------------------------------------------

    print()
    print("Chargement des informations étudiantes depuis DuckDB...")

    students = load_student_metadata()

    print(
        f"Informations étudiantes : {students.shape}"
    )

    if len(students) != len(X):
        raise ValueError(
            "Le nombre de lignes du mart dbt "
            "ne correspond pas aux features."
        )

    # ---------------------------------------------------------
    # 3. ENTRAINEMENT K-MEANS
    # ---------------------------------------------------------

    print()
    print("Entraînement de K-Means...")

    model = KMeans(
        n_clusters=N_CLUSTERS,
        random_state=RANDOM_STATE,
        n_init=10,
    )

    labels = model.fit_predict(X)

    print("Entraînement terminé.")

    # ---------------------------------------------------------
    # 4. METRIQUES
    # ---------------------------------------------------------

    print()
    print("Calcul des métriques...")

    silhouette = silhouette_score(X, labels)

    davies_bouldin = davies_bouldin_score(
        X,
        labels,
    )

    calinski_harabasz = calinski_harabasz_score(
        X,
        labels,
    )

    inertia = model.inertia_

    print(
        f"Inertia              : {inertia:.4f}"
    )

    print(
        f"Silhouette Score      : {silhouette:.4f}"
    )

    print(
        f"Davies-Bouldin Score  : {davies_bouldin:.4f}"
    )

    print(
        f"Calinski-Harabasz     : "
        f"{calinski_harabasz:.2f}"
    )

    # ---------------------------------------------------------
    # 5. DISTRIBUTION DES CLUSTERS
    # ---------------------------------------------------------

    cluster_counts = (
        pd.Series(labels)
        .value_counts()
        .sort_index()
    )

    print()
    print("Distribution des clusters :")

    for cluster, count in cluster_counts.items():

        percentage = (
            count / len(labels) * 100
        )

        print(
            f"Cluster {cluster}: "
            f"{count:,} étudiants "
            f"({percentage:.2f}%)"
        )

    # ---------------------------------------------------------
    # 6. SAUVEGARDE DU MODELE
    # ---------------------------------------------------------

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_PATH,
    )

    print()
    print(
        f"Modèle sauvegardé : {MODEL_PATH}"
    )

    # ---------------------------------------------------------
    # 7. SAUVEGARDE DES METRIQUES
    # ---------------------------------------------------------

    metrics = {
        "model": "KMeans",
        "n_clusters": N_CLUSTERS,
        "random_state": RANDOM_STATE,
        "n_samples": int(X.shape[0]),
        "n_features": int(X.shape[1]),
        "inertia": float(inertia),
        "silhouette_score": float(silhouette),
        "davies_bouldin_score": float(
            davies_bouldin
        ),
        "calinski_harabasz_score": float(
            calinski_harabasz
        ),
        "cluster_sizes": {
            str(cluster): int(count)
            for cluster, count
            in cluster_counts.items()
        },
    }

    with open(
        METRICS_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metrics,
            file,
            indent=4,
        )

    print(
        f"Métriques sauvegardées : {METRICS_PATH}"
    )

    # ---------------------------------------------------------
    # 8. DATASET AVEC LES CLUSTERS
    # ---------------------------------------------------------

    students["cluster"] = labels

    students.to_csv(
        CLUSTERS_PATH,
        index=False,
    )

    print(
        f"Dataset clusterisé sauvegardé : "
        f"{CLUSTERS_PATH}"
    )

    # ---------------------------------------------------------
    # 9. PROFIL DES CLUSTERS
    # ---------------------------------------------------------

    profile = (
        students
        .groupby("cluster")
        .agg({
            "num_of_prev_attempts": "mean",
            "studied_credits": "mean",
        })
        .reset_index()
    )

    profile.to_csv(
        PROFILE_PATH,
        index=False,
    )

    print(
        f"Profils sauvegardés : {PROFILE_PATH}"
    )

    # ---------------------------------------------------------
    # 10. PROFIL FINAL_RESULT
    # ---------------------------------------------------------

    final_result_profile = pd.crosstab(
        students["cluster"],
        students["final_result"],
        normalize="index",
    ) * 100

    final_result_profile = (
        final_result_profile
        .reset_index()
    )

    final_result_profile.to_csv(
        FINAL_RESULT_PROFILE_PATH,
        index=False,
    )

    print(
        f"Profil final_result sauvegardé : "
        f"{FINAL_RESULT_PROFILE_PATH}"
    )

    # ---------------------------------------------------------
    # FIN
    # ---------------------------------------------------------

    print()
    print("=" * 60)
    print("MODELE K-MEANS FINAL TERMINÉ")
    print("=" * 60)


if __name__ == "__main__":
    main()