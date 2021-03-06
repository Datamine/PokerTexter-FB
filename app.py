"""
foo
"""

import os
import datetime
import flask
import requests
import parsers
from sqlalchemy import and_
from flask_sqlalchemy import SQLAlchemy

FACEBOOK_API_MESSAGE_SEND_URL = (
    'https://graph.facebook.com/v2.6/me/messages?access_token=%s'
)

# Response to bad input
STANDARD_ERRORMSG = (
    "Error! I couldn't understand that! "
    "Please respond with `examples` to see some examples of correct use."
)

app = flask.Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FACEBOOK_PAGE_ACCESS_TOKEN'] = os.environ['FACEBOOK_PAGE_ACCESS_TOKEN']
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecretkey')
app.config['FACEBOOK_WEBHOOK_VERIFY_TOKEN'] = os.environ['FACEBOOK_WEBHOOK_VERIFY_TOKEN']

db = SQLAlchemy(app)

class Hand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ranks are '2', '3', ..., '10', 'J', ..., 'A'
    rank_one = db.Column(db.String, nullable=False)
    rank_two = db.Column(db.String, nullable=False)
    # true if suited, false if off-suit
    suited = db.Column(db.Boolean, nullable=False)
    # number of OTHER players on the table.
    players = db.Column(db.Integer, nullable=False)
    p_win = db.Column(db.Float, nullable=False)
    p_tie = db.Column(db.Float, nullable=False)
    expected_gain = db.Column(db.Float, nullable=False)

def get_stats(rank1, rank2, suiting, players):
    """
    Query the Postgres DB for this particular Hand.
    """

    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    # determine which of {rank1, rank2} is higher-ranked.
    # in the lookup table, hands are indexed in form RANK1 RANK2 where RANK1 <= RANK2.
    if ranks.index(rank1) <= ranks.index(rank2):
        lower, higher = rank1, rank2
    else:
        lower, higher = rank2, rank1

    hand = Hand.query.filter(and_(
                                Hand.rank_one == lower,
                                Hand.rank_two == higher,
                                Hand.suited == suiting,
                                Hand.players == players)
                            ).first()

    return hand.p_win, hand.p_tie, hand.expected_gain

def example():
    """
    returns some examples for correct message formatting.
    """

    header = (
        "A message needs to be formatted, in order, like this: \n"
        "  <card rank>\n"
        "  <card rank>\n"
        "  <whether both cards are of the same suit>\n"
        "  <number of other players, excluding yourself>\n\n"
        "Here are some examples:\n\n"
    )

    examples = (
        "ONE EIGHT SUITED ONE\n"
        "7 ace offsuit 9\n"
        "Jack Q suited 5"
    )

    return header + examples

def check_input(rank1, rank2, suiting, players):
    """
    Check that all the input message tokens are valid. Return None if so.
    Return appropriate error message if not.
    """

    # check that all the parsed input is valid
    if players==None:
        return (
            "Error! Couldn't read the number of other players."
            "Only 1-9 other players are currently supported."
        )

    if any(map(lambda x: x==None, [rank1, rank2, suiting])):
        return STANDARD_ERRORMSG

    if rank1==rank2 and suiting:
        return "Error! It is impossible to have a suited pair. You may have meant `offsuit`."

    return None

def handle_message(message):
    """
    Where `message` is a string that has already been stripped and lower-cased,
    tokenize it and find the corresponding Hand in the database. (Also: return some
    helpful examples if requested, or an error message if the input cannot be parsed.)
    """

    if 'example' in message:
        return example()

    message_tokens = filter(lambda x: x != '', message.split(" "))

    if len(message_tokens) != 4:
        # maybe use a better error message here?
        return STANDARD_ERRORMSG

    # handle the described poker hand.
    rank1 = parsers.get_rank(message_tokens[0])
    rank2 = parsers.get_rank(message_tokens[1])
    suiting = parsers.get_suiting(message_tokens[2])
    players = parsers.get_players(message_tokens[3])

    check = check_input(rank1, rank2, suiting, players)
    if check != None:
        return check

    try:
        p_win, p_tie, expected_gain = get_stats(rank1, rank2, suiting, players)
    except:
        print "Input valid but bad db lookup." + str([rank1, rank2, suiting, players])
        return "Error! Input valid but DataBase lookup failed? Please report this bug."

    return (
        "P(win): " + str(p_win * 100) + "%\n"
        "P(tie): " + str(p_tie * 100) + "%\n"
        "Expected unit gain: " + str(expected_gain)
    )

@app.route('/fb_webhook', methods=['GET', 'POST'])
def webhook():
    """
    """

    # Handle the initial handshake request.
    if flask.request.method == 'GET':
        if (flask.request.args.get('hub.mode') == 'subscribe' and
            flask.request.args.get('hub.verify_token') ==
            app.config['FACEBOOK_WEBHOOK_VERIFY_TOKEN']):
            challenge = flask.request.args.get('hub.challenge')
            return challenge
        else:
            print('Received invalid GET request')
            return ''  # Still return a 200, otherwise FB gets upset.

    # Get the request body as a dict, parsed from JSON.
    payload = flask.request.json

    # TODO: Validate app ID and other parts of the payload to make sure we're
    # not accidentally processing data that wasn't intended for us.

    # Handle an incoming message.
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
                message_text = handle_message(message['text'].lower().strip())
                request_url = FACEBOOK_API_MESSAGE_SEND_URL % (
                    app.config['FACEBOOK_PAGE_ACCESS_TOKEN'])
                requests.post(request_url,
                              headers={'Content-Type': 'application/json'},
                              json={'recipient': {'id': sender_id},
                                    'message': {'text': message_text}})

    # Return an empty response (HTTP code 200.)
    return ''

if __name__ == '__main__':
    app.run(debug=True)
