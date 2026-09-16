"""Validate that the deployable EduCluster model bundle is internally consistent."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import joblib


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "models" / "model_manifest.json"
MODEL_PATH = ROOT / "models" / "kmeans_final.joblib"
SCALER_PATH = ROOT / "data" / "processed" / "scaler.joblib"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_bundle(root: Path = ROOT) -> dict:
    manifest_path = root / "models" / "model_manifest.json"
    model_path = root / "models" / "kmeans_final.joblib"
    scaler_path = root / "data" / "processed" / "scaler.joblib"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    features = manifest["features"]

    errors = []
    if sha256(model_path) != manifest["model_sha256"]:
        errors.append("model checksum does not match model_manifest.json")
    if sha256(scaler_path) != manifest["scaler_sha256"]:
        errors.append("scaler checksum does not match model_manifest.json")
    if int(model.n_features_in_) != len(features):
        errors.append("model feature count does not match manifest")
    if int(scaler.n_features_in_) != len(features):
        errors.append("scaler feature count does not match manifest")
    if list(getattr(model, "feature_names_in_", features)) != features:
        errors.append("model feature order does not match manifest")
    if list(getattr(scaler, "feature_names_in_", features)) != features:
        errors.append("scaler feature order does not match manifest")
    if set(manifest["count_features"]) - set(features):
        errors.append("count_features contains names absent from features")
    expected_clusters = {str(index) for index in range(int(model.n_clusters))}
    if set(manifest["cluster_profiles"]) != expected_clusters:
        errors.append("cluster profile mapping does not match model clusters")
    if errors:
        raise ValueError("Invalid model bundle: " + "; ".join(errors))
    return manifest


if __name__ == "__main__":
    bundle = validate_bundle()
    print(
        f"Validated {bundle['model_name']} {bundle['model_version']} "
        f"with {len(bundle['features'])} features."
    )
