"""
foo
"""

import os
import datetime
import flask
import requests
from flask_sqlalchemy import SQLAlchemy

FACEBOOK_API_MESSAGE_SEND_URL = ('https://graph.facebook.com/v2.6/me/messages?access_token=%s')

app = flask.Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['FACEBOOK_PAGE_ACCESS_TOKEN'] = os.environ['FACEBOOK_PAGE_ACCESS_TOKEN']
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecretkey')
app.config['FACEBOOK_WEBHOOK_VERIFY_TOKEN'] = os.environ['FACEBOOK_WEBHOOK_VERIFY_TOKEN']

db = SQLAlchemy(app)

class Hand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # cards are '2', '3', ..., '10', 'J', ..., 'A'
    card_one = db.Column(db.String, nullable=False, required=True)
    card_two = db.Column(db.String, nullable=False, required=True)
    # true if suited, false if off-suit
    suited = db.Column(db.Boolean, nullable=False, required=True)
    # number of OTHER players on the table.
    players = db.Column(db.Integer, nullable=False, required=True)
    p_win = db.Column(db.Float, nullable=False, required=True)
    p_tie = db.Column(db.Float, nullable=False, required=True)
    expected_gain = db.Column(db.Float, nullable=False, required=True)

def handle_message(*args):
    return "foo"

@app.route('/fb_webhook', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
