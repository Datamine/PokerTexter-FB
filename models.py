"""
Using the SQLAlchemy ORM to create the model for storing a Poker hand
"""

from app import app

class Hand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # cards are '2', '3', ..., '10', 'J', ..., 'A'
    card_one = db.Column(db.String, nullable=False, required=True)
    card_two = db.Column(db.String, nullable=False, required=True)
    suited = db.Column(db.Boolean, nullable=False, required=True)
    players = db.Column(db.Integer, nullable=False, required=True)
