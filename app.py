"""
foo
"""

import os
import datetime
import flask
import requests
from flask_sqlalchemy import SQLAlchemy

FACEBOOK_API_MESSAGE_SEND_URL = (
    'https://graph.facebook.com/v2.6/me/messages?access_token=%s')

app = flask.Flask(__name__)

# TODO: Set environment variables appropriately.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['FACEBOOK_PAGE_ACCESS_TOKEN'] = os.environ[
    'FACEBOOK_PAGE_ACCESS_TOKEN']
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecretkey')
app.config['FACEBOOK_WEBHOOK_VERIFY_TOKEN'] = 'mysecretverifytoken'

@app.route('/', methods=['GET', 'POST'])
def index():
    """Simple example handler.

    This is just an example handler that demonstrates the basics of SQLAlchemy,
    relationships, and template rendering in Flask.

    """

    # Handle the initial handshake request.
    if flask.request.method == 'GET':
        if (flask.request.args.get('hub.mode') == 'subscribe' and
            flask.request.args.get('hub.verify_token') ==
            app.config['FACEBOOK_WEBHOOK_VERIFY_TOKEN']):
            challenge = flask.request.args.get('hub.challenge')
            return challenge
        else:
            print 'Received invalid GET request'
            return ''  # Still return a 200, otherwise FB gets upset.

    """
    # Get the request body as a dict, parsed from JSON.
    payload = flask.request.json

    # TODO: Validate app ID and other parts of the payload to make sure we're
    # not accidentally processing data that wasn't intended for us.

    # Handle an incoming message.
    # TODO: Improve error handling in case of unexpected payloads.
    for entry in payload['entry']:
        for event in entry['messaging']:
            if 'message' not in event:
                continue
            message = event['message']
            # Ignore messages sent by us.
            if message.get('is_echo', False):
                continue
            # Ignore messages with non-text content.
            if 'text' not in message:
                continue
            else:
                sender_id = event['sender']['id']
                message_text = handle_message(sender_id, message['text'].lower().strip())
                request_url = FACEBOOK_API_MESSAGE_SEND_URL % (
                    app.config['FACEBOOK_PAGE_ACCESS_TOKEN'])
                requests.post(request_url,
                              headers={'Content-Type': 'application/json'},
                              json={'recipient': {'id': sender_id},
                                    'message': {'text': message_text}})

    # Return an empty response.
    return ''
    """

if __name__ == '__main__':
    app.run(debug=True)
