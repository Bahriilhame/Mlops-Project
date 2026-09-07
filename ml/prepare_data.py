from pathlib import Path

import duckdb
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DUCKDB_PATH = (
    PROJECT_ROOT
    / "oulad_pipeline.duckdb"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FEATURES_OUTPUT = OUTPUT_DIR / "clustering_features.csv"
SCALER_OUTPUT = OUTPUT_DIR / "scaler.joblib"


# ============================================================
# FEATURES
# ============================================================

BEHAVIOR_FEATURES = [
    # VLE / engagement
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

    # Types d'activités
    "clicks_content",
    "clicks_forum",
    "clicks_quiz",
    "clicks_wiki",
    "clicks_other",

    # Ratios
    "content_ratio",
    "forum_ratio",
    "quiz_ratio",
    "wiki_ratio",
    "other_ratio",

    # Assessments
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


# Variables de comptage très asymétriques
LOG_FEATURES = [
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
    "assessment_count",
    "expected_assessment_count",
    "late_submission_count",
    "avg_submission_delay",
    "median_submission_delay",
    "max_submission_delay",
]


# ============================================================
# CHARGEMENT DU MART
# ============================================================

def load_features() -> pd.DataFrame:
    """Charge les features depuis le mart dbt."""

    print("=" * 60)
    print("CHARGEMENT DES DONNÉES")
    print("=" * 60)

    print(f"DuckDB : {DUCKDB_PATH}")

    if not DUCKDB_PATH.exists():
        raise FileNotFoundError(
            f"Base DuckDB introuvable : {DUCKDB_PATH}"
        )

    con = duckdb.connect(str(DUCKDB_PATH))

    query = """
        SELECT *
        FROM main.student_learning_features
    """

    df = con.execute(query).df()
    con.close()

    print(f"Nombre de lignes : {len(df)}")
    print(f"Nombre de colonnes : {len(df.columns)}")

    return df


# ============================================================
# PREPARATION
# ============================================================

def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """Sélectionne et prépare les variables pour le clustering."""

    print()
    print("=" * 60)
    print("PRÉPARATION DES FEATURES")
    print("=" * 60)

    missing_features = [
        feature
        for feature in BEHAVIOR_FEATURES
        if feature not in df.columns
    ]

    if missing_features:
        raise ValueError(
            "Features manquantes : "
            + ", ".join(missing_features)
        )

    X = df[BEHAVIOR_FEATURES].copy()

    # Remplacement des valeurs infinies
    X = X.replace(
        [np.inf, -np.inf],
        np.nan
    )

    # Valeurs manquantes
    missing_before = X.isna().sum().sum()

    print(
        f"Valeurs manquantes avant traitement : "
        f"{missing_before}"
    )

    X = X.fillna(0)

    # --------------------------------------------------------
    # LOG1P
    # --------------------------------------------------------

    print()
    print("Application de log1p sur les variables asymétriques...")

    for feature in LOG_FEATURES:
        if feature in X.columns:
            X[feature] = np.log1p(
                X[feature].clip(lower=0)
            )

    # --------------------------------------------------------
    # STANDARDISATION
    # --------------------------------------------------------

    print("Standardisation avec StandardScaler...")

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    X_scaled = pd.DataFrame(
        X_scaled,
        columns=BEHAVIOR_FEATURES
    )

    print(
        f"Shape finale : {X_scaled.shape}"
    )

    return X_scaled, scaler


# ============================================================
# SAUVEGARDE
# ============================================================

def save_outputs(
    X_scaled: pd.DataFrame,
    scaler: StandardScaler,
) -> None:

    print()
    print("=" * 60)
    print("SAUVEGARDE")
    print("=" * 60)

    X_scaled.to_csv(
        FEATURES_OUTPUT,
        index=False
    )

    joblib.dump(
        scaler,
        SCALER_OUTPUT
    )

    print(
        f"Features : {FEATURES_OUTPUT}"
    )

    print(
        f"Scaler   : {SCALER_OUTPUT}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    df = load_features()

    X_scaled, scaler = prepare_features(df)

    save_outputs(
        X_scaled,
        scaler
    )

    print()
    print("=" * 60)
    print("PRÉPARATION TERMINÉE")
    print("=" * 60)

    print(
        f"Dataset clustering : "
        f"{X_scaled.shape[0]} étudiants"
    )

    print(
        f"Features utilisées : "
        f"{X_scaled.shape[1]}"
    )

    print()
    print("Aucune variable démographique ni")
    print("'final_result' n'est utilisée pour le clustering.")


if __name__ == "__main__":
    main()