import json
from types import SimpleNamespace

from src.student_score_mlops import predict


def test_model_metadata_reads_available_files(tmp_path, monkeypatch):
    model_path = tmp_path / "model.joblib"
    metrics_path = tmp_path / "metrics.json"
    fingerprint_path = tmp_path / "data_fingerprint.json"

    model_path.write_bytes(b"model")
    metrics_path.write_text(json.dumps({"r2": 0.91}), encoding="utf-8")
    fingerprint_path.write_text(json.dumps({"fingerprint": "abc123"}), encoding="utf-8")

    monkeypatch.setattr(
        predict,
        "settings",
        SimpleNamespace(
            metrics_path=metrics_path,
            data_fingerprint_path=fingerprint_path,
        ),
    )

    metadata = predict.model_metadata(model_path=model_path, loaded_at="2026-07-08T00:00:00Z")

    assert metadata["model_exists"] is True
    assert metadata["metrics"]["r2"] == 0.91
    assert metadata["dataset_fingerprint"]["fingerprint"] == "abc123"
    assert metadata["loaded_at"] == "2026-07-08T00:00:00Z"
