"""Regression tests against the real persisted scaler and KMeans model."""
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from fastapi.testclient import TestClient

from api import dashboard
from api.main import app, FEATURES, COUNT_FEATURES, CLUSTER_NAMES, model, scaler


class DashboardApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_existing_root_and_health(self):
        self.assertEqual(self.client.get('/').json()['name'], 'EduCluster API')
        self.assertEqual(self.client.get('/health').json()['status'], 'healthy')

    def test_prediction_uses_unchanged_preprocessing_and_real_model(self):
        self.assertEqual(len(FEATURES), 34)
        self.assertEqual(model.n_features_in_, 34)
        for base in (0, 1, 10):
            payload = {feature: float(base) for feature in FEATURES}
            payload['avg_submission_delay'] = -4
            row = [np.log1p(max(payload[f], 0)) if f in COUNT_FEATURES else payload[f] for f in FEATURES]
            expected = int(model.predict(scaler.transform(np.array([row])))[0])
            response = self.client.post('/predict', json=payload)
            self.assertEqual(response.status_code, 200, response.text)
            self.assertEqual(response.json(), {'cluster': expected, 'profile': CLUSTER_NAMES[expected]})

    def test_prediction_requires_all_fields(self):
        response = self.client.post('/predict', json={FEATURES[0]: 1})
        self.assertEqual(response.status_code, 422)

    def test_prediction_rejects_nonnumeric_values(self):
        payload = dict.fromkeys(FEATURES, 0)
        payload['active_days'] = 'not a number'
        self.assertEqual(self.client.post('/predict', json=payload).status_code, 422)

    def test_cors_preflight(self):
        response = self.client.options('/predict', headers={
            'Origin': 'http://localhost:5173', 'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'content-type'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['access-control-allow-origin'], 'http://localhost:5173')
        rejected = self.client.options('/predict', headers={
            'Origin': 'https://unlisted.example', 'Access-Control-Request-Method': 'POST'})
        self.assertNotIn('access-control-allow-origin', rejected.headers)

    def test_reference_endpoints(self):
        with patch.object(Path, 'is_file', return_value=False):
            stats = self.client.get('/statistics')
            info = self.client.get('/model-info')
        self.assertEqual(stats.status_code, 200)
        self.assertEqual(stats.json()['total_students'], 32593)
        self.assertEqual(stats.json()['clusters']['0'], {'count': 25612, 'percentage': 78.58})
        self.assertEqual(stats.json()['source'], 'reference_results')
        self.assertEqual(info.status_code, 200)
        self.assertEqual(info.json()['silhouette_score'], .4569)
        self.assertEqual(info.json()['features'], 34)

    def test_local_metrics_take_priority(self):
        metrics = {'n_samples': 10, 'cluster_sizes': {'0': 7, '1': 3},
                   'silhouette_score': .6, 'davies_bouldin_score': .7, 'calinski_harabasz_score': 12}
        with patch.object(Path, 'is_file', return_value=True), patch.object(dashboard, 'read_json', return_value=metrics):
            self.assertEqual(self.client.get('/statistics').json()['clusters']['0']['percentage'], 70)
            self.assertEqual(self.client.get('/model-info').json()['silhouette_score'], .6)

    def test_malformed_metrics_and_inconsistent_counts(self):
        metrics = {'n_samples': 10, 'cluster_sizes': {'0': 7, '1': 4}, 'silhouette_score': float('nan')}
        with patch.object(Path, 'is_file', return_value=True), patch.object(dashboard, 'read_json', return_value=metrics):
            self.assertEqual(self.client.get('/statistics').status_code, 503)
            self.assertEqual(self.client.get('/model-info').status_code, 503)

    def test_csv_source_and_empty_state(self):
        from io import StringIO
        with patch.object(Path, 'is_file', lambda p: p.name == 'clustered_students.csv'):
            with patch.object(Path, 'open', return_value=StringIO('id_student,cluster\n1,0\n2,1\n3,0\n')):
                result = self.client.get('/statistics').json()
                self.assertEqual(result['total_students'], 3)
                self.assertEqual(result['source'], 'clustered_students.csv')
            with patch.object(Path, 'open', return_value=StringIO('id_student,cluster\n')):
                result = self.client.get('/statistics').json()
                self.assertEqual(result['total_students'], 0)


if __name__ == '__main__':
    unittest.main()
