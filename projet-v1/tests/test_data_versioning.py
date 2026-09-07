import json

import pandas as pd

from src.student_score_mlops.data_versioning import (
    data_changed,
    fingerprint_dataframe,
    read_fingerprint_metadata,
    write_fingerprint_metadata,
)


def test_dataframe_fingerprint_is_independent_of_column_order():
    left = pd.DataFrame({"b": [2, 4], "a": [1, 3]})
    right = pd.DataFrame({"a": [1, 3], "b": [2, 4]})

    assert fingerprint_dataframe(left) == fingerprint_dataframe(right)


def test_fingerprint_metadata_round_trip(tmp_path):
    metadata_path = tmp_path / "data_fingerprint.json"

    written = write_fingerprint_metadata(
        fingerprint="abc123",
        row_count=10,
        source="test",
        path=metadata_path,
    )

    assert read_fingerprint_metadata(metadata_path) == written
    assert not data_changed("abc123", metadata_path)
    assert data_changed("new456", metadata_path)
    assert json.loads(metadata_path.read_text(encoding="utf-8"))["row_count"] == 10
