import hashlib
import hmac
import unittest
import urllib.error
from unittest.mock import Mock

from scripts.trigger_komodo import build_request, send_request


class FakeResponse:
    status = 202

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class WebhookTests(unittest.TestCase):
    url = 'https://komodo.example.org/listener/github/stack/example/deploy'
    payload = b'{"ref":"refs/heads/main","deleted":false,"after":"example"}'

    def test_signature_matches_exact_payload(self):
        request = build_request(self.url, 'test-only-secret', self.payload)
        expected = 'sha256=' + hmac.new(b'test-only-secret', self.payload, hashlib.sha256).hexdigest()
        self.assertEqual(request.get_header('X-hub-signature-256'), expected)
        self.assertEqual(request.data, self.payload)
        self.assertEqual(request.get_method(), 'POST')
        self.assertEqual(request.get_header('X-github-delivery'), 'example')

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

    def test_retries_transient_gateway_errors(self):
        request = build_request(self.url, 'test', self.payload)
        gateway_error = urllib.error.HTTPError(self.url, 502, 'Bad Gateway', {}, None)
        opener = Mock()
        opener.open.side_effect = [gateway_error, gateway_error, FakeResponse()]
        sleep = Mock()

        send_request(request, opener=opener, attempts=3, retry_delay=0, sleep=sleep)

        self.assertEqual(opener.open.call_count, 3)
        self.assertEqual(sleep.call_count, 2)

    def test_does_not_retry_authentication_errors(self):
        request = build_request(self.url, 'test', self.payload)
        opener = Mock()
        opener.open.side_effect = urllib.error.HTTPError(
            self.url, 401, 'Unauthorized', {}, None
        )

        with self.assertRaisesRegex(RuntimeError, 'HTTP 401'):
            send_request(request, opener=opener, attempts=3, retry_delay=0)
        self.assertEqual(opener.open.call_count, 1)


if __name__ == '__main__':
    unittest.main()
