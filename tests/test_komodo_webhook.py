import hashlib
import hmac
import unittest
from scripts.trigger_komodo import build_request


class WebhookTests(unittest.TestCase):
    url = 'https://komodo.example.org/listener/github/stack/example/deploy'
    payload = b'{"ref":"refs/heads/main","deleted":false,"after":"example"}'

    def test_signature_matches_exact_payload(self):
        request = build_request(self.url, 'test-only-secret', self.payload)
        expected = 'sha256=' + hmac.new(b'test-only-secret', self.payload, hashlib.sha256).hexdigest()
        self.assertEqual(request.get_header('X-hub-signature-256'), expected)
        self.assertEqual(request.data, self.payload)
        self.assertEqual(request.get_method(), 'POST')

    def test_rejects_wrong_branch_and_deletion(self):
        for body in (b'{"ref":"refs/heads/dev"}', b'{"ref":"refs/heads/main","deleted":true}'):
            with self.assertRaises(ValueError):
                build_request(self.url, 'test', body)

    def test_requires_secret_and_https_stack_deploy_url(self):
        for url, secret in ((self.url, ''), (self.url.replace('https:', 'http:'), 'test'),
                            (self.url.replace('/deploy', '/refresh'), 'test'),
                            (self.url + '?secret=test', 'test')):
            with self.assertRaises(ValueError):
                build_request(url, secret, self.payload)


if __name__ == '__main__':
    unittest.main()
