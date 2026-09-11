"""Read-only presentation data. Never runs or changes the ML pipeline."""
import csv
import json
import math
from collections import Counter
from pathlib import Path

from fastapi import APIRouter, HTTPException

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
REFERENCE_PATH = Path(__file__).with_name("reference_results.json")
router = APIRouter()


def read_json(path):
    try:
        with path.open(encoding="utf-8-sig") as stream:
            value = json.load(stream)
        if not isinstance(value, dict):
            raise ValueError("Expected a JSON object")
        return value
    except (OSError, ValueError) as exc:
        raise HTTPException(503, f"Impossible de lire {path.name}.") from exc


def read_metrics():
    path = PROCESSED / "kmeans_metrics.json"
    if path.is_file():
        return read_json(path), "kmeans_metrics.json"
    return read_json(REFERENCE_PATH), "reference_results"


def normalized_counts(raw):
    if not isinstance(raw, dict) or not raw or any(
        key not in ("0", "1") or isinstance(value, bool)
        or not isinstance(value, int) or value < 0
        for key, value in raw.items()
    ):
        raise HTTPException(503, "Les effectifs des segments sont invalides.")
    return {key: raw.get(key, 0) for key in ("0", "1")}


@router.get("/statistics")
def statistics():
    metrics_path = PROCESSED / "kmeans_metrics.json"
    students_path = PROCESSED / "clustered_students.csv"
    # This artifact contains counts and scores from the same training run.
    if metrics_path.is_file() and "cluster_sizes" in (metrics := read_json(metrics_path)):
        counts = normalized_counts(metrics["cluster_sizes"])
        source = "kmeans_metrics.json"
        if "n_samples" in metrics and metrics["n_samples"] != sum(counts.values()):
            raise HTTPException(503, "Les effectifs ne correspondent pas à n_samples.")
    elif students_path.is_file():
        try:
            with students_path.open(encoding="utf-8-sig", newline="") as stream:
                reader = csv.DictReader(stream)
                if not reader.fieldnames or "cluster" not in reader.fieldnames:
                    raise ValueError("Missing cluster column")
                counts = Counter(row["cluster"] for row in reader)
            counts = normalized_counts(dict(counts)) if counts else {"0": 0, "1": 0}
            source = "clustered_students.csv"
        except (OSError, ValueError, csv.Error) as exc:
            raise HTTPException(503, "Impossible de lire clustered_students.csv.") from exc
    elif metrics_path.is_file():
        raise HTTPException(503, "Les résultats locaux ne contiennent pas les effectifs des segments.")
    else:
        counts = normalized_counts(read_json(REFERENCE_PATH)["cluster_sizes"])
        source = "reference_results"
    total = sum(counts.values())
    return {
        "total_students": total,
        "clusters": {key: {"count": count, "percentage": round(100 * count / total, 2) if total else 0}
                     for key, count in counts.items()},
        "source": source,
    }


def finite_metric(value):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise HTTPException(503, "Une métrique du modèle est invalide.")
    return value


def model_information(model, feature_count):
    metrics, source = read_metrics()
    return {
        "algorithm": type(model).__name__,
        "n_clusters": int(model.n_clusters),
        "features": feature_count,
        "silhouette_score": finite_metric(metrics.get("silhouette_score")),
        "davies_bouldin_score": finite_metric(metrics.get("davies_bouldin_score")),
        "calinski_harabasz_score": finite_metric(metrics.get("calinski_harabasz_score")),
        "source": source,
    }
