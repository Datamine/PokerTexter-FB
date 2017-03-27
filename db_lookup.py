from models import Hand
from sqlalchemy import and_

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


