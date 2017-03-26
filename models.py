"""
Using the SQLAlchemy ORM to create the model for storing a Poker hand
"""

from app import db

class Hand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # cards are '2', '3', ..., '10', 'J', ..., 'A'
    card_one = db.Column(db.String, nullable=False)
    card_two = db.Column(db.String, nullable=False)
    # true if suited, false if off-suit
    suited = db.Column(db.Boolean, nullable=False)
    # number of OTHER players on the table.
    players = db.Column(db.Integer, nullable=False)
    p_win = db.Column(db.Float, nullable=False)
    p_tie = db.Column(db.Float, nullable=False)
    expected_gain = db.Column(db.Float, nullable=False)

