"""EduCluster local dashboard. Python standard library only; project files are read-only."""
import argparse
import csv
import json
import math
from collections import Counter
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ASSETS = Path(__file__).resolve().parent
FILES = {
    'database': 'oulad_pipeline.duckdb',
    'features': 'data/processed/clustering_features.csv',
    'scaler': 'data/processed/scaler.joblib',
    'model': 'models/kmeans_final.joblib',
    'students': 'data/processed/clustered_students.csv',
    'profiles': 'data/processed/cluster_profiles.csv',
    'results': 'data/processed/cluster_final_result_profile.csv',
    'metrics': 'data/processed/kmeans_metrics.json',
    'comparison': 'data/processed/clustering_comparison.csv',
}

def snapshot(root):
    errors, inventory, content = [], [], {}
    for key, relative in FILES.items():
        path = root / relative
        exists = path.is_file()
        inventory.append({'key': key, 'path': relative, 'exists': exists,
                          'modified': datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat() if exists else None})
        if not exists or path.suffix not in ('.json', '.csv') or key == 'features':
            continue
        try:
            with path.open(encoding='utf-8-sig', newline='') as stream:
                content[key] = json.load(stream) if path.suffix == '.json' else list(csv.DictReader(stream))
        except (OSError, ValueError, csv.Error) as exc:
            errors.append(f'{relative} : {exc}')
    rows = content.get('students', [])
    # Only fields needed by the dashboard leave the server.
    fields = ('id_student', 'code_module', 'code_presentation', 'cluster', 'final_result')
    students = [{key: row.get(key, '') for key in fields} for row in rows]
    metrics = content.get('metrics', {})
    if not isinstance(metrics, dict):
        errors.append('Le fichier de métriques doit contenir un objet JSON.')
        metrics = {}
    metrics = {k: (v if isinstance(v, (int, float)) and math.isfinite(v) else None) for k, v in metrics.items()}
    return {'updated': datetime.now(timezone.utc).isoformat(), 'files': inventory,
            'students': students, 'metrics': metrics, 'profiles': content.get('profiles', []),
            'comparison': content.get('comparison', []), 'errors': errors}

def make_handler(root):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            route = urlsplit(self.path).path
            if route == '/api/dashboard':
                try:
                    body = json.dumps(snapshot(root), ensure_ascii=False, allow_nan=False).encode('utf-8')
                    mime = 'application/json; charset=utf-8'
                except Exception:
                    self.send_error(500, 'Impossible de lire les donnees du projet')
                    return
            elif route in ('/', '/index.html', '/style.css', '/app.js'):
                name = 'index.html' if route == '/' else route[1:]
                body = (ASSETS / name).read_bytes()
                mime = {'html': 'text/html', 'css': 'text/css', 'js': 'text/javascript'}[name.rsplit('.', 1)[1]] + '; charset=utf-8'
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
    return Handler

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=ASSETS.parent)
    parser.add_argument('--port', type=int, default=8050)
    args = parser.parse_args()
    if not args.project.is_dir():
        parser.error('Le dossier du projet est introuvable.')
    server = ThreadingHTTPServer(('127.0.0.1', args.port), make_handler(args.project.resolve()))
    print(f'EduCluster : http://127.0.0.1:{args.port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
