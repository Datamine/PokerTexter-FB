def get_rank(string):
    """
    Parses a string representing a rank. Returns a string in the correct form
    for the lookup table. Returns None if the input could not be parsed.
    """
    if "ace" in string or string=="a":
        return "A"
    if "king" in string or string=="k":
        return "K"
    if "queen" in string or string=="q":
        return "Q"
    if "jack" in string or string=="j":
        return "J"
    if "ten" in string or string=="10" or string=="t":
        return "T"
    if "nine" in string or string=="9":
        return "9"
    if "eight" in string or string=="8":
        return "8"
    if "seven" in string or string=="7":
        return "7"
    if "six" in string or string=="6":
        return "6"
    if "five" in string or string=="5":
        return "5"
    if "four" in string or string=="4":
        return "4"
    if "three" in string or string=="3":
        return "3"
    if "two" in string or string=="2":
        return "2"

    return None

def get_suiting(string):
    """
    Parses a string representing the suiting (suited/offsuit) of the player's
    two hole cards. Returns True if suited, False if offsuit.
    Returns None if the input could not be parsed.
    """
    if "of" in string or "un" in string:
        # handles offsuit, unsuited, etc.
        return False
    if "suit" in string:
        return True

    return None

def get_players(string):
    """
    Parses a string representing the number of other players (i.e. excluding
    the player) in the round. Currently supports only 1-9 other players.
    Returns a string in the correct form for the lookup table.
    Returns None if the input could not be parsed.
    """
    if "nine" in string or string=="9":
        return 9
    if "eight" in string or string=="8":
        return 8
    if "seven" in string or string=="7":
        return 7
    if "six" in string or string=="6":
        return 6
    if "five" in string or string=="5":
        return 5
    if "four" in string or string=="4":
        return 4
    if "three" in string or string=="3":
        return 3
    if "two" in string or string=="2":
        return 2
    if "one" in string or string=="1":
        return 1

    return None
