"""Send the original GitHub push event to the configured Komodo stack webhook."""
import hashlib
import hmac
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


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
    return urllib.request.Request(url, data=payload, method='POST', headers={
        'Content-Type': 'application/json', 'X-GitHub-Event': 'push',
        'X-Hub-Signature-256': signature, 'User-Agent': 'EduCluster-GitHub-Actions',
    })


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main():
    if os.environ.get('GITHUB_EVENT_NAME') != 'push':
        raise ValueError('Deployment requires a GitHub push event.')
    payload = Path(os.environ['GITHUB_EVENT_PATH']).read_bytes()
    request = build_request(os.environ.get('KOMODO_WEBHOOK_URL', ''),
                            os.environ.get('KOMODO_WEBHOOK_SECRET', ''), payload)
    # Do not automatically retry: the first request may already have triggered a deployment.
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=45) as response:
            if not 200 <= response.status < 300:
                raise RuntimeError('Komodo rejected the webhook.')
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f'Komodo returned HTTP {exc.code}. Check webhook settings and secret.') from None
    except (urllib.error.URLError, TimeoutError):
        raise RuntimeError('Komodo acknowledgement unavailable. Check Updates before retrying.') from None
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
