from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd

from src.student_score_mlops.config import settings


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


def hash_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fingerprint_dataframe(df: pd.DataFrame) -> str:
    normalized = df.sort_index(axis=1).reset_index(drop=True)
    csv_bytes = normalized.to_csv(index=False, lineterminator="\n").encode("utf-8")
    return hashlib.sha256(csv_bytes).hexdigest()


def read_fingerprint_metadata(path: Path = settings.data_fingerprint_path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_fingerprint_metadata(
    fingerprint: str,
    row_count: int,
    source: str,
    path: Path = settings.data_fingerprint_path,
) -> dict[str, Any]:
    metadata = {
        "fingerprint": fingerprint,
        "row_count": row_count,
        "source": source,
        "updated_at": utc_now_iso(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata


def data_changed(
    current_fingerprint: str,
    path: Path = settings.data_fingerprint_path,
) -> bool:
    previous = read_fingerprint_metadata(path)
    if previous is None:
        return True
    return previous.get("fingerprint") != current_fingerprint


def raw_data_status(path: Path = settings.raw_data_path) -> dict[str, Any]:
    if not path.exists():
        return {
            "exists": False,
            "path": str(path),
            "fingerprint": None,
            "row_count": 0,
        }

    try:
        row_count = max(sum(1 for _ in path.open("r", encoding="utf-8")) - 1, 0)
    except UnicodeDecodeError:
        row_count = 0

    return {
        "exists": True,
        "path": str(path),
        "fingerprint": hash_file(path),
        "row_count": row_count,
    }
