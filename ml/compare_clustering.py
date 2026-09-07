from pathlib import Path
import time

import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
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

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

RESULTS_PATH = (
    OUTPUT_DIR
    / "clustering_comparison.csv"
)


def evaluate_model(name, model, X):

    print()
    print("-" * 60)
    print(f"Modèle : {name}")
    print("-" * 60)

    start = time.time()

    labels = model.fit_predict(X)

    elapsed = time.time() - start

    unique_labels = set(labels)

    # Nombre de clusters hors bruit pour DBSCAN
    if -1 in unique_labels:
        n_clusters = len(unique_labels - {-1})
        n_noise = (labels == -1).sum()
    else:
        n_clusters = len(unique_labels)
        n_noise = 0

    print(f"Nombre de clusters : {n_clusters}")
    print(f"Points bruit : {n_noise}")
    print(f"Temps : {elapsed:.2f} secondes")

    # Pour calculer les métriques correctement avec DBSCAN,
    # on ignore les points considérés comme bruit (-1).
    mask = labels != -1

    X_eval = X[mask]
    labels_eval = labels[mask]

    if len(set(labels_eval)) < 2:
        print("Impossible de calculer les métriques.")
        return {
            "model": name,
            "n_clusters": n_clusters,
            "noise_points": n_noise,
            "silhouette": None,
            "davies_bouldin": None,
            "calinski_harabasz": None,
            "time_seconds": elapsed,
        }

    silhouette = silhouette_score(
        X_eval,
        labels_eval,
    )

    davies_bouldin = davies_bouldin_score(
        X_eval,
        labels_eval,
    )

    calinski_harabasz = calinski_harabasz_score(
        X_eval,
        labels_eval,
    )

    print(f"Silhouette Score      : {silhouette:.4f}")
    print(f"Davies-Bouldin Score  : {davies_bouldin:.4f}")
    print(f"Calinski-Harabasz     : {calinski_harabasz:.2f}")

    return {
        "model": name,
        "n_clusters": n_clusters,
        "noise_points": n_noise,
        "silhouette": silhouette,
        "davies_bouldin": davies_bouldin,
        "calinski_harabasz": calinski_harabasz,
        "time_seconds": elapsed,
    }


def main():

    print("=" * 60)
    print("COMPARAISON DES ALGORITHMES DE CLUSTERING")
    print("=" * 60)

    if not FEATURES_PATH.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {FEATURES_PATH}"
        )

    X = pd.read_csv(
        FEATURES_PATH
    ).values

    print()
    print(f"Données : {X.shape}")

    results = []

    # ---------------------------------------------------------
    # 1. K-MEANS
    # ---------------------------------------------------------

    kmeans = KMeans(
        n_clusters=2,
        random_state=42,
        n_init=10,
    )

    results.append(
        evaluate_model(
            "K-Means",
            kmeans,
            X,
        )
    )

    # ---------------------------------------------------------
    # 2. AGGLOMERATIVE CLUSTERING
    # ---------------------------------------------------------

    agglomerative = AgglomerativeClustering(
        n_clusters=2,
        linkage="ward",
    )

    results.append(
        evaluate_model(
            "Agglomerative",
            agglomerative,
            X,
        )
    )

    # ---------------------------------------------------------
    # 3. DBSCAN
    # ---------------------------------------------------------

    # Plusieurs configurations sont testées.
    dbscan_params = [
        (0.5, 10),
        (0.7, 10),
        (1.0, 10),
        (1.2, 10),
        (1.5, 10),
    ]

    for eps, min_samples in dbscan_params:

        dbscan = DBSCAN(
            eps=eps,
            min_samples=min_samples,
            n_jobs=-1,
        )

        results.append(
            evaluate_model(
                f"DBSCAN eps={eps} min_samples={min_samples}",
                dbscan,
                X,
            )
        )

    # ---------------------------------------------------------
    # SAUVEGARDE
    # ---------------------------------------------------------

    results_df = pd.DataFrame(
        results
    )

    results_df.to_csv(
        RESULTS_PATH,
        index=False,
    )

    print()
    print("=" * 60)
    print("RÉSULTATS")
    print("=" * 60)

    print(
        results_df.to_string(
            index=False
        )
    )

    print()
    print(
        f"Résultats sauvegardés : {RESULTS_PATH}"
    )

    print()
    print("=" * 60)
    print("COMPARAISON TERMINÉE")
    print("=" * 60)


if __name__ == "__main__":
    main()