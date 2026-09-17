"""Small regression checks; never start training or modify serving artifacts."""
import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import pandas as pd
from dagster import DagsterInstance

ROOT = Path(__file__).resolve().parents[1]


class TrainingResourceTests(unittest.TestCase):
    def test_ingestion_streams_every_row_in_bounded_batches(self):
        # Only the decorator is stubbed; exercise the real pandas CSV reader.
        dlt_stub = types.SimpleNamespace(resource=lambda **kwargs: lambda fn: fn)
        spec = importlib.util.spec_from_file_location(
            "ingestion_under_test", ROOT / "dlt_pipeline/load_oulad.py"
        )
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {"dlt": dlt_stub}):
            spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            module.DATA_DIR = Path(directory)
            expected = pd.DataFrame({"id_student": range(25001), "sum_click": 2})
            expected.to_csv(module.DATA_DIR / "studentVle.csv", index=False)
            batches = list(module.student_vle())
            self.assertEqual([len(batch) for batch in batches], [10000, 10000, 5001])
            pd.testing.assert_frame_equal(pd.concat(batches, ignore_index=True), expected)
            with self.assertRaises(FileNotFoundError):
                list(module.load_csv("missing.csv"))

    def test_dagster_loads_single_run_queue(self):
        with tempfile.TemporaryDirectory() as directory:
            shutil.copyfile(ROOT / "deploy/dagster.yaml", Path(directory) / "dagster.yaml")
            with DagsterInstance.from_config(directory) as instance:
                config = instance.run_coordinator.get_run_queue_config()
                self.assertEqual(config.max_concurrent_runs, 1)


if __name__ == "__main__":
    unittest.main()
