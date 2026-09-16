"""Start MLflow, wait until it is ready, then seed the deployed model once."""
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.request

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.log_to_mlflow import main as log_bundle


PORT = os.getenv("MLFLOW_PORT", "5000")
URI = f"http://127.0.0.1:{PORT}"
DATA_DIR = Path(os.getenv("MLFLOW_DATA_DIR", "/mlflow-store"))


def wait_until_ready(process, timeout=60):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"MLflow stopped with code {process.returncode}")
        try:
            urllib.request.urlopen(f"{URI}/health", timeout=2)
            return
        except OSError:
            time.sleep(1)
    raise TimeoutError("MLflow did not become ready within 60 seconds")


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    process = subprocess.Popen([
        "mlflow", "server", "--host", "0.0.0.0", "--port", PORT,
        "--backend-store-uri", f"sqlite:///{DATA_DIR / 'mlflow.db'}",
        "--artifacts-destination", str(DATA_DIR / "artifacts"),
        "--serve-artifacts",
    ])
    try:
        wait_until_ready(process)
        log_bundle(URI)
        return process.wait()
    except BaseException:
        process.terminate()
        process.wait(timeout=10)
        raise


if __name__ == "__main__":
    sys.exit(main())
