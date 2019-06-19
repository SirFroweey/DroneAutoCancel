import os
import six
import hmac
import hashlib
from flask import Flask, request, abort, jsonify

from api import *

WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN') # secret

app = Flask(__name__)


def cancel_latest_build(sha_hash):
    api = Drone(DRONE_SERVER, DRONE_ACCESS_TOKEN, DRONE_REPO_OWNER_USERNAME, DRONE_REPO_NAME)
    return api.stop_latest_build(sha_hash)


def get_digest(request):
    """Return message digest if a secret key was provided."""
    return hmac.new(
        WEBHOOK_VERIFY_TOKEN.encode('utf-8'), 
        request.data, 
        hashlib.sha1
    ).hexdigest() if WEBHOOK_VERIFY_TOKEN else None


def process_event(event_type, data):
    print "EVENT:", event_type, "DATA:", data
    payload = {}
    if event_type == 'ping':
        payload = {
            'success': True
        }
    elif event_type == ('pull_request' or 'push'):
        sha_hash = data['ref']
        response = cancel_latest_build(sha_hash)
        payload = {'status': response['message']}
    else:
        abort(400, 'Unsupported event type.')
    return jsonify(payload), 200


def post_receive(request):
    """Callback from Flask"""
    digest = get_digest(request)

    if digest is not None:
        sig_parts = request.headers['X-Hub-Signature'].split('=', 1)
        if not isinstance(digest, six.text_type):
            digest = six.text_type(digest)

        if (len(sig_parts) < 2 or sig_parts[0] != 'sha1'
                or not hmac.compare_digest(sig_parts[1], digest)):
            abort(400, 'Invalid signature.')
    else:
        abort(400, 'ENV VAR not set for WEBHOOK_VERIFY_TOKEN')

    event_type = request.headers['X-Github-Event']

    try:
        data = request.get_json()
    except:
        data = None

    if data is None:
        abort(400, 'Request body must contain json.')

    return process_event(event_type, data)


@app.route('/webhook', methods=['POST'])
def web_hook():
    if request.method == 'POST':
        return post_receive(request)
    else:
        abort(400, 'Invalid HTTP method invoked.')


if __name__ == '__main__':
    app.run(debug=True)
