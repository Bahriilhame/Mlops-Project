"""Send the original GitHub push event to the configured Komodo stack webhook."""
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


RETRYABLE_HTTP_CODES = {502, 503, 504}


def build_request(url, secret, payload):
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.username
            or parsed.password or parsed.query or parsed.fragment
            or not parsed.path.startswith('/listener/github/stack/')
            or not parsed.path.endswith('/deploy')):
        raise ValueError('KOMODO_WEBHOOK_URL must be the HTTPS GitHub deploy webhook of the stack.')
    if not secret:
        raise ValueError('KOMODO_WEBHOOK_SECRET is missing.')
    event = json.loads(payload)
    if event.get('ref') != 'refs/heads/main' or event.get('deleted', False):
        raise ValueError('Only a non-deletion push to main may deploy.')
    signature = 'sha256=' + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    delivery_id = event.get('after') or hashlib.sha256(payload).hexdigest()
    return urllib.request.Request(url, data=payload, method='POST', headers={
        'Content-Type': 'application/json', 'X-GitHub-Event': 'push',
        'X-Hub-Signature-256': signature, 'User-Agent': 'EduCluster-GitHub-Actions',
        'X-GitHub-Delivery': delivery_id,
    })


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def send_request(request, opener=None, attempts=4, retry_delay=5, sleep=time.sleep):
    """Send a webhook, retrying only transient reverse-proxy/server failures."""
    opener = opener or urllib.request.build_opener(NoRedirect())
    for attempt in range(1, attempts + 1):
        try:
            with opener.open(request, timeout=45) as response:
                if not 200 <= response.status < 300:
                    raise RuntimeError('Komodo rejected the webhook.')
                return
        except urllib.error.HTTPError as exc:
            if exc.code in RETRYABLE_HTTP_CODES and attempt < attempts:
                print(f'Komodo returned HTTP {exc.code}; retrying ({attempt}/{attempts}).',
                      file=sys.stderr)
                sleep(retry_delay * attempt)
                continue
            raise RuntimeError(
                f'Komodo returned HTTP {exc.code}. Check webhook settings and secret.'
            ) from None
        except (urllib.error.URLError, TimeoutError):
            raise RuntimeError(
                'Komodo acknowledgement unavailable. Check Updates before retrying.'
            ) from None


def main():
    if os.environ.get('GITHUB_EVENT_NAME') != 'push':
        raise ValueError('Deployment requires a GitHub push event.')
    payload = Path(os.environ['GITHUB_EVENT_PATH']).read_bytes()
    request = build_request(os.environ.get('KOMODO_WEBHOOK_URL', ''),
                            os.environ.get('KOMODO_WEBHOOK_SECRET', ''), payload)
    # A stable delivery ID lets Komodo identify repeated delivery attempts for the same commit.
    send_request(request)
    message = ('Signed deployment request accepted by Komodo. '
               'Check the stack Updates for deployment completion and deployed commit.')
    print(message)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as summary:
            summary.write(message + '\n')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
