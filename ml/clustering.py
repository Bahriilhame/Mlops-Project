# from pathlib import Path

# import joblib
# import matplotlib.pyplot as plt
# import pandas as pd

# from sklearn.cluster import KMeans
# from sklearn.metrics import (
#     calinski_harabasz_score,
#     davies_bouldin_score,
#     silhouette_score,
# )


# # ============================================================
# # CONFIGURATION
# # ============================================================

# PROJECT_ROOT = Path(__file__).resolve().parent.parent

# DATA_PATH = (
#     PROJECT_ROOT
#     / "data"
#     / "processed"
#     / "clustering_features.csv"
# )

# OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
# OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# RESULTS_PATH = OUTPUT_DIR / "kmeans_evaluation.csv"
# PLOT_PATH = OUTPUT_DIR / "kmeans_evaluation.png"
# MODEL_DIR = PROJECT_ROOT / "models"
# MODEL_DIR.mkdir(parents=True, exist_ok=True)


# # ============================================================
# # PARAMÈTRES
# # ============================================================

# K_VALUES = range(2, 9)

# RANDOM_STATE = 42

# N_INIT = 10

# MAX_ITER = 300


# # ============================================================
# # CHARGEMENT
# # ============================================================

# def load_data() -> pd.DataFrame:
#     """Charge les données standardisées."""

#     print("=" * 60)
#     print("CHARGEMENT DES FEATURES")
#     print("=" * 60)

#     if not DATA_PATH.exists():
#         raise FileNotFoundError(
#             f"Dataset introuvable : {DATA_PATH}"
#         )

#     df = pd.read_csv(DATA_PATH)

#     print(f"Dataset : {DATA_PATH}")
#     print(f"Nombre d'étudiants : {len(df)}")
#     print(f"Nombre de features : {len(df.columns)}")

#     return df


# # ============================================================
# # ÉVALUATION K-MEANS
# # ============================================================

# def evaluate_kmeans(df: pd.DataFrame) -> pd.DataFrame:
#     """Teste plusieurs valeurs de K."""

#     print()
#     print("=" * 60)
#     print("ÉVALUATION DE K-MEANS")
#     print("=" * 60)

#     X = df.values

#     results = []

#     for k in K_VALUES:

#         print(f"\nK = {k}")

#         model = KMeans(
#             n_clusters=k,
#             random_state=RANDOM_STATE,
#             n_init=N_INIT,
#             max_iter=MAX_ITER,
#         )

#         labels = model.fit_predict(X)

#         inertia = model.inertia_

#         silhouette = silhouette_score(
#             X,
#             labels
#         )

#         davies_bouldin = davies_bouldin_score(
#             X,
#             labels
#         )

#         calinski_harabasz = calinski_harabasz_score(
#             X,
#             labels
#         )

#         results.append(
#             {
#                 "k": k,
#                 "inertia": inertia,
#                 "silhouette_score": silhouette,
#                 "davies_bouldin_score": davies_bouldin,
#                 "calinski_harabasz_score": calinski_harabasz,
#             }
#         )

#         print(
#             f"  Inertia              : {inertia:.2f}"
#         )

#         print(
#             f"  Silhouette           : {silhouette:.4f}"
#         )

#         print(
#             f"  Davies-Bouldin       : {davies_bouldin:.4f}"
#         )

#         print(
#             f"  Calinski-Harabasz    : {calinski_harabasz:.2f}"
#         )

#     return pd.DataFrame(results)


# # ============================================================
# # MEILLEUR K
# # ============================================================

# def select_best_k(results: pd.DataFrame) -> int:
#     """
#     Sélection initiale du meilleur K selon
#     le Silhouette Score.
#     """

#     best_row = results.loc[
#         results["silhouette_score"].idxmax()
#     ]

#     best_k = int(best_row["k"])

#     print()
#     print("=" * 60)
#     print("MEILLEUR K")
#     print("=" * 60)

#     print(
#         f"K sélectionné selon Silhouette Score : {best_k}"
#     )

#     print(
#         f"Silhouette : "
#         f"{best_row['silhouette_score']:.4f}"
#     )

#     print(
#         f"Davies-Bouldin : "
#         f"{best_row['davies_bouldin_score']:.4f}"
#     )

#     print(
#         f"Calinski-Harabasz : "
#         f"{best_row['calinski_harabasz_score']:.2f}"
#     )

#     return best_k


# # ============================================================
# # GRAPHIQUE
# # ============================================================

# def create_plot(results: pd.DataFrame) -> None:
#     """Crée les courbes d'évaluation."""

#     print()
#     print("=" * 60)
#     print("CRÉATION DU GRAPHIQUE")
#     print("=" * 60)

#     fig, axes = plt.subplots(
#         2,
#         2,
#         figsize=(12, 9)
#     )

#     # Inertia
#     axes[0, 0].plot(
#         results["k"],
#         results["inertia"],
#         marker="o"
#     )

#     axes[0, 0].set_title(
#         "Méthode du coude - Inertia"
#     )

#     axes[0, 0].set_xlabel("Nombre de clusters (K)")
#     axes[0, 0].set_ylabel("Inertia")
#     axes[0, 0].grid(True)

#     # Silhouette
#     axes[0, 1].plot(
#         results["k"],
#         results["silhouette_score"],
#         marker="o"
#     )

#     axes[0, 1].set_title(
#         "Silhouette Score"
#     )

#     axes[0, 1].set_xlabel("Nombre de clusters (K)")
#     axes[0, 1].set_ylabel("Silhouette")
#     axes[0, 1].grid(True)

#     # Davies-Bouldin
#     axes[1, 0].plot(
#         results["k"],
#         results["davies_bouldin_score"],
#         marker="o"
#     )

#     axes[1, 0].set_title(
#         "Davies-Bouldin Index"
#     )

#     axes[1, 0].set_xlabel("Nombre de clusters (K)")
#     axes[1, 0].set_ylabel("Davies-Bouldin")
#     axes[1, 0].grid(True)

#     # Calinski-Harabasz
#     axes[1, 1].plot(
#         results["k"],
#         results["calinski_harabasz_score"],
#         marker="o"
#     )

#     axes[1, 1].set_title(
#         "Calinski-Harabasz Index"
#     )

#     axes[1, 1].set_xlabel("Nombre de clusters (K)")
#     axes[1, 1].set_ylabel("Calinski-Harabasz")
#     axes[1, 1].grid(True)

#     plt.tight_layout()

#     plt.savefig(
#         PLOT_PATH,
#         dpi=150,
#         bbox_inches="tight"
#     )

#     plt.close()

#     print(f"Graphique sauvegardé : {PLOT_PATH}")


# # ============================================================
# # MODÈLE FINAL
# # ============================================================

# def train_final_model(
#     df: pd.DataFrame,
#     best_k: int,
# ):
#     """Entraîne le modèle K-Means final."""

#     print()
#     print("=" * 60)
#     print("ENTRAÎNEMENT DU MODÈLE FINAL")
#     print("=" * 60)

#     X = df.values

#     model = KMeans(
#         n_clusters=best_k,
#         random_state=RANDOM_STATE,
#         n_init=N_INIT,
#         max_iter=MAX_ITER,
#     )

#     labels = model.fit_predict(X)

#     model_path = (
#         MODEL_DIR
#         / f"kmeans_k{best_k}.joblib"
#     )

#     joblib.dump(
#         model,
#         model_path
#     )

#     print(
#         f"Modèle sauvegardé : {model_path}"
#     )

#     print()
#     print("Répartition des clusters :")

#     cluster_counts = pd.Series(
#         labels
#     ).value_counts().sort_index()

#     for cluster, count in cluster_counts.items():

#         percentage = (
#             count / len(labels) * 100
#         )

#         print(
#             f"  Cluster {cluster} : "
#             f"{count} étudiants "
#             f"({percentage:.2f}%)"
#         )

#     return model, labels


# # ============================================================
# # SAUVEGARDE DES RÉSULTATS
# # ============================================================

# def save_results(results: pd.DataFrame) -> None:

#     results.to_csv(
#         RESULTS_PATH,
#         index=False
#     )

#     print(
#         f"\nRésultats sauvegardés : {RESULTS_PATH}"
#     )


# # ============================================================
# # MAIN
# # ============================================================

# def main():

#     df = load_data()

#     results = evaluate_kmeans(df)

#     print()
#     print("=" * 60)
#     print("TABLEAU COMPARATIF")
#     print("=" * 60)

#     print(
#         results.to_string(
#             index=False,
#             float_format=lambda x: f"{x:.4f}"
#         )
#     )

#     save_results(results)

#     best_k = select_best_k(results)

#     create_plot(results)

#     model, labels = train_final_model(
#         df,
#         best_k
#     )

#     print()
#     print("=" * 60)
#     print("CLUSTERING TERMINÉ")
#     print("=" * 60)

#     print(
#         f"Meilleur K : {best_k}"
#     )

#     print(
#         f"Nombre d'étudiants : {len(labels)}"
#     )


# if __name__ == "__main__":
#     main()








from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "clustering_features.csv"
)

DUCKDB_PATH = PROJECT_ROOT / "oulad_pipeline.duckdb"

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RESULTS_PATH = OUTPUT_DIR / "kmeans_evaluation.csv"
PLOT_PATH = OUTPUT_DIR / "kmeans_evaluation.png"

LABELS_PATH = OUTPUT_DIR / "clustered_students.csv"
PROFILE_PATH = OUTPUT_DIR / "cluster_profiles.csv"
RESULT_PROFILE_PATH = OUTPUT_DIR / "cluster_final_result_profile.csv"

MODEL_DIR = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# PARAMÈTRES
# ============================================================

K_VALUES = range(2, 9)

RANDOM_STATE = 42
N_INIT = 10
MAX_ITER = 300


# ============================================================
# CHARGEMENT
# ============================================================

def load_data() -> pd.DataFrame:
    """Charge les données standardisées."""

    print("=" * 60)
    print("CHARGEMENT DES FEATURES")
    print("=" * 60)

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset introuvable : {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    print(f"Dataset : {DATA_PATH}")
    print(f"Nombre d'étudiants : {len(df)}")
    print(f"Nombre de features : {len(df.columns)}")

    return df


# ============================================================
# ÉVALUATION K-MEANS
# ============================================================

def evaluate_kmeans(df: pd.DataFrame) -> pd.DataFrame:
    """Teste plusieurs valeurs de K."""

    print()
    print("=" * 60)
    print("ÉVALUATION DE K-MEANS")
    print("=" * 60)

    X = df.values

    results = []

    for k in K_VALUES:

        print(f"\nK = {k}")

        model = KMeans(
            n_clusters=k,
            random_state=RANDOM_STATE,
            n_init=N_INIT,
            max_iter=MAX_ITER,
        )

        labels = model.fit_predict(X)

        inertia = model.inertia_

        silhouette = silhouette_score(
            X,
            labels,
        )

        davies_bouldin = davies_bouldin_score(
            X,
            labels,
        )

        calinski_harabasz = calinski_harabasz_score(
            X,
            labels,
        )

        results.append(
            {
                "k": k,
                "inertia": inertia,
                "silhouette_score": silhouette,
                "davies_bouldin_score": davies_bouldin,
                "calinski_harabasz_score": calinski_harabasz,
            }
        )

        print(
            f"  Inertia              : {inertia:.2f}"
        )

        print(
            f"  Silhouette           : {silhouette:.4f}"
        )

        print(
            f"  Davies-Bouldin       : {davies_bouldin:.4f}"
        )

        print(
            f"  Calinski-Harabasz    : {calinski_harabasz:.2f}"
        )

    return pd.DataFrame(results)


# ============================================================
# MEILLEUR K
# ============================================================

def select_best_k(results: pd.DataFrame) -> int:

    best_row = results.loc[
        results["silhouette_score"].idxmax()
    ]

    best_k = int(best_row["k"])

    print()
    print("=" * 60)
    print("MEILLEUR K")
    print("=" * 60)

    print(
        f"K sélectionné selon Silhouette Score : {best_k}"
    )

    print(
        f"Silhouette : "
        f"{best_row['silhouette_score']:.4f}"
    )

    print(
        f"Davies-Bouldin : "
        f"{best_row['davies_bouldin_score']:.4f}"
    )

    print(
        f"Calinski-Harabasz : "
        f"{best_row['calinski_harabasz_score']:.2f}"
    )

    return best_k


# ============================================================
# GRAPHIQUE
# ============================================================

def create_plot(results: pd.DataFrame) -> None:

    print()
    print("=" * 60)
    print("CRÉATION DU GRAPHIQUE")
    print("=" * 60)

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(12, 9),
    )

    axes[0, 0].plot(
        results["k"],
        results["inertia"],
        marker="o",
    )

    axes[0, 0].set_title(
        "Méthode du coude - Inertia"
    )

    axes[0, 0].set_xlabel("Nombre de clusters (K)")
    axes[0, 0].set_ylabel("Inertia")
    axes[0, 0].grid(True)

    axes[0, 1].plot(
        results["k"],
        results["silhouette_score"],
        marker="o",
    )

    axes[0, 1].set_title(
        "Silhouette Score"
    )

    axes[0, 1].set_xlabel("Nombre de clusters (K)")
    axes[0, 1].set_ylabel("Silhouette")
    axes[0, 1].grid(True)

    axes[1, 0].plot(
        results["k"],
        results["davies_bouldin_score"],
        marker="o",
    )

    axes[1, 0].set_title(
        "Davies-Bouldin Index"
    )

    axes[1, 0].set_xlabel("Nombre de clusters (K)")
    axes[1, 0].set_ylabel("Davies-Bouldin")
    axes[1, 0].grid(True)

    axes[1, 1].plot(
        results["k"],
        results["calinski_harabasz_score"],
        marker="o",
    )

    axes[1, 1].set_title(
        "Calinski-Harabasz Index"
    )

    axes[1, 1].set_xlabel("Nombre de clusters (K)")
    axes[1, 1].set_ylabel("Calinski-Harabasz")
    axes[1, 1].grid(True)

    plt.tight_layout()

    plt.savefig(
        PLOT_PATH,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()

    print(
        f"Graphique sauvegardé : {PLOT_PATH}"
    )


# ============================================================
# MODÈLE FINAL
# ============================================================

def train_final_model(
    df: pd.DataFrame,
    best_k: int,
):
    """Entraîne le modèle K-Means final."""

    print()
    print("=" * 60)
    print("ENTRAÎNEMENT DU MODÈLE FINAL")
    print("=" * 60)

    X = df.values

    model = KMeans(
        n_clusters=best_k,
        random_state=RANDOM_STATE,
        n_init=N_INIT,
        max_iter=MAX_ITER,
    )

    labels = model.fit_predict(X)

    model_path = (
        MODEL_DIR
        / f"kmeans_k{best_k}.joblib"
    )

    joblib.dump(
        model,
        model_path,
    )

    print(
        f"Modèle sauvegardé : {model_path}"
    )

    print()
    print("Répartition des clusters :")

    cluster_counts = pd.Series(
        labels
    ).value_counts().sort_index()

    for cluster, count in cluster_counts.items():

        percentage = (
            count / len(labels) * 100
        )

        print(
            f"  Cluster {cluster} : "
            f"{count} étudiants "
            f"({percentage:.2f}%)"
        )

    return model, labels


# ============================================================
# SAUVEGARDE ÉVALUATION
# ============================================================

def save_results(results: pd.DataFrame) -> None:

    results.to_csv(
        RESULTS_PATH,
        index=False,
    )

    print(
        f"\nRésultats sauvegardés : {RESULTS_PATH}"
    )


# ============================================================
# PROFILAGE DES CLUSTERS
# ============================================================

def profile_clusters(
    labels,
    best_k: int,
) -> None:

    print()
    print("=" * 60)
    print("PROFILAGE DES CLUSTERS")
    print("=" * 60)

    # --------------------------------------------------------
    # Charger les données originales depuis DuckDB
    # --------------------------------------------------------

    import duckdb

    if not DUCKDB_PATH.exists():
        raise FileNotFoundError(
            f"DuckDB introuvable : {DUCKDB_PATH}"
        )

    con = duckdb.connect(
        str(DUCKDB_PATH)
    )

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

            total_vle_interactions,
            total_clicks,
            active_days,
            active_weeks,
            activity_span_days,
            unique_resource_visits,

            avg_daily_clicks,
            median_daily_clicks,
            max_daily_clicks,
            clicks_std,
            avg_clicks_per_event,

            clicks_content,
            clicks_forum,
            clicks_quiz,
            clicks_wiki,
            clicks_other,

            content_ratio,
            forum_ratio,
            quiz_ratio,
            wiki_ratio,
            other_ratio,

            assessment_count,
            expected_assessment_count,
            submission_rate,
            avg_assessment_score,
            min_assessment_score,
            max_assessment_score,
            assessment_score_std,

            late_submission_count,
            late_submission_rate,
            avg_submission_delay,
            median_submission_delay,
            max_submission_delay,
            on_time_submission_rate,

            final_result

        FROM main.student_learning_features
    """

    original_df = con.execute(query).df()

    con.close()

    if len(original_df) != len(labels):
        raise ValueError(
            "Le nombre de labels ne correspond pas "
            "au nombre de lignes DuckDB."
        )

    original_df["cluster"] = labels

    # --------------------------------------------------------
    # Sauvegarde des étudiants avec leur cluster
    # --------------------------------------------------------

    original_df.to_csv(
        LABELS_PATH,
        index=False,
    )

    print(
        f"Dataset avec clusters : {LABELS_PATH}"
    )

    # --------------------------------------------------------
    # Profil numérique
    # --------------------------------------------------------

    numeric_columns = [
        "total_vle_interactions",
        "total_clicks",
        "active_days",
        "active_weeks",
        "activity_span_days",
        "unique_resource_visits",
        "avg_daily_clicks",
        "median_daily_clicks",
        "max_daily_clicks",
        "clicks_std",
        "avg_clicks_per_event",
        "clicks_content",
        "clicks_forum",
        "clicks_quiz",
        "clicks_wiki",
        "clicks_other",
        "content_ratio",
        "forum_ratio",
        "quiz_ratio",
        "wiki_ratio",
        "other_ratio",
        "assessment_count",
        "expected_assessment_count",
        "submission_rate",
        "avg_assessment_score",
        "min_assessment_score",
        "max_assessment_score",
        "assessment_score_std",
        "late_submission_count",
        "late_submission_rate",
        "avg_submission_delay",
        "median_submission_delay",
        "max_submission_delay",
        "on_time_submission_rate",
    ]

    profile = (
        original_df
        .groupby("cluster")[numeric_columns]
        .mean()
        .round(3)
    )

    profile.insert(
        0,
        "student_count",
        original_df["cluster"].value_counts().sort_index(),
    )

    profile.insert(
        1,
        "percentage",
        (
            original_df["cluster"]
            .value_counts(normalize=True)
            .sort_index()
            * 100
        ).round(2),
    )

    profile.to_csv(
        PROFILE_PATH
    )

    print(
        f"Profil numérique : {PROFILE_PATH}"
    )

    # --------------------------------------------------------
    # Profil final_result
    # --------------------------------------------------------

    result_profile = pd.crosstab(
        original_df["cluster"],
        original_df["final_result"],
        normalize="index",
    ) * 100

    result_profile = result_profile.round(2)

    result_profile.to_csv(
        RESULT_PROFILE_PATH
    )

    print(
        f"Profil final_result : "
        f"{RESULT_PROFILE_PATH}"
    )

    # --------------------------------------------------------
    # Affichage
    # --------------------------------------------------------

    print()
    print("-" * 60)
    print("PROFIL NUMÉRIQUE DES CLUSTERS")
    print("-" * 60)

    print(
        profile.to_string()
    )

    print()
    print("-" * 60)
    print("DISTRIBUTION DE FINAL_RESULT PAR CLUSTER (%)")
    print("-" * 60)

    print(
        result_profile.to_string()
    )

    print()
    print("-" * 60)
    print("INTERPRÉTATION À FAIRE")
    print("-" * 60)

    print(
        "Les noms des profils ne sont pas encore attribués."
    )

    print(
        "Ils seront déterminés à partir des différences "
        "réelles observées entre les clusters."
    )


# ============================================================
# MAIN
# ============================================================

def main():

    df = load_data()

    results = evaluate_kmeans(df)

    print()
    print("=" * 60)
    print("TABLEAU COMPARATIF")
    print("=" * 60)

    print(
        results.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    save_results(results)

    best_k = select_best_k(results)

    create_plot(results)

    model, labels = train_final_model(
        df,
        best_k,
    )

    profile_clusters(
        labels,
        best_k,
    )

    print()
    print("=" * 60)
    print("CLUSTERING + PROFILAGE TERMINÉS")
    print("=" * 60)

    print(
        f"Meilleur K : {best_k}"
    )

    print(
        f"Nombre d'étudiants : {len(labels)}"
    )


if __name__ == "__main__":
    main()