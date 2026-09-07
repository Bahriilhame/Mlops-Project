from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.decomposition import PCA


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

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

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

PCA_DATA_PATH = (
    OUTPUT_DIR
    / "pca_clusters.csv"
)

PCA_PLOT_PATH = (
    OUTPUT_DIR
    / "pca_clusters.png"
)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("PCA - VISUALISATION DES CLUSTERS")
    print("=" * 60)

    # --------------------------------------------------------
    # Chargement
    # --------------------------------------------------------

    if not FEATURES_PATH.exists():
        raise FileNotFoundError(
            f"Features introuvables : {FEATURES_PATH}"
        )

    if not CLUSTERS_PATH.exists():
        raise FileNotFoundError(
            f"Clusters introuvables : {CLUSTERS_PATH}"
        )

    features = pd.read_csv(
        FEATURES_PATH
    )

    clusters = pd.read_csv(
        CLUSTERS_PATH
    )

    print(
        f"Features : {features.shape}"
    )

    print(
        f"Clusters : {clusters.shape}"
    )

    if len(features) != len(clusters):
        raise ValueError(
            "Le nombre de lignes ne correspond pas."
        )

    # --------------------------------------------------------
    # PCA
    # --------------------------------------------------------

    print()
    print("Application de PCA...")

    pca = PCA(
        n_components=2,
        random_state=42,
    )

    X_pca = pca.fit_transform(
        features
    )

    explained_variance = (
        pca.explained_variance_ratio_
    )

    total_variance = (
        explained_variance.sum()
    )

    print(
        f"Variance expliquée PC1 : "
        f"{explained_variance[0] * 100:.2f}%"
    )

    print(
        f"Variance expliquée PC2 : "
        f"{explained_variance[1] * 100:.2f}%"
    )

    print(
        f"Variance expliquée totale : "
        f"{total_variance * 100:.2f}%"
    )

    # --------------------------------------------------------
    # Dataset PCA
    # --------------------------------------------------------

    pca_df = pd.DataFrame(
        {
            "PC1": X_pca[:, 0],
            "PC2": X_pca[:, 1],
            "cluster": clusters["cluster"],
        }
    )

    pca_df.to_csv(
        PCA_DATA_PATH,
        index=False,
    )

    print(
        f"Dataset PCA sauvegardé : "
        f"{PCA_DATA_PATH}"
    )

    # --------------------------------------------------------
    # Visualisation
    # --------------------------------------------------------

    print()
    print("Création du graphique...")

    plt.figure(
        figsize=(10, 7)
    )

    for cluster in sorted(
        pca_df["cluster"].unique()
    ):

        cluster_data = pca_df[
            pca_df["cluster"] == cluster
        ]

        plt.scatter(
            cluster_data["PC1"],
            cluster_data["PC2"],
            label=f"Cluster {cluster}",
            alpha=0.45,
            s=12,
        )

    plt.title(
        "PCA - Student Learning Behavior Clusters"
    )

    plt.xlabel(
        f"PC1 ({explained_variance[0] * 100:.2f}% variance)"
    )

    plt.ylabel(
        f"PC2 ({explained_variance[1] * 100:.2f}% variance)"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3,
    )

    plt.tight_layout()

    plt.savefig(
        PCA_PLOT_PATH,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()

    print(
        f"Graphique sauvegardé : "
        f"{PCA_PLOT_PATH}"
    )

    print()
    print("=" * 60)
    print("PCA TERMINÉE")
    print("=" * 60)


if __name__ == "__main__":
    main()