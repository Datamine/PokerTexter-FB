"""
instantiate/reset the postgres database on Heroku.
"""

import os
from app import db
from models import Hand

db.drop_all()
db.create_all()

for lookup_table in os.listdir('/app/lookup-tables'):
    path = '/app/lookup-tables/' + lookup_table
    # get the number of players from the filename
    number_of_players = int(lookup_table.split('-')[-1])

    with open(path, 'r') as f:
        for line in f:
            split_line = line.strip().split("\t")
            rank_one = split_line[0]
            rank_two = split_line[1]
            suited = split_line[2] == 'suited'
            probability_win = float(split_line[3])
            probability_tie = float(split_line[4])
            expected_gain = float(split_line[5])

            hand = Hand(
                rank_one = rank_one,
                rank_two = rank_two,
                suited = suited,
                p_win = probability_win,
                p_tie = probability_tie,
                expected_gain = expected_gain,
                players = number_of_players
            )
            db.session.add(hand)

db.session.commit()

print("Added all Hands to DB. Rows (expect 1521):")
print(Hand.query.count())
