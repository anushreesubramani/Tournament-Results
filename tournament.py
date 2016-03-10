#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    # Truncates all the entries in the matches table
    cur.execute("truncate matches;")
    conn.commit()
    cur.close()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    # Truncates all the entries in the players table
    cur.execute("truncate players cascade;")
    conn.commit()
    cur.close()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    # Selects the count of players from players table
    cur.execute("select count(*) from players;")
    count = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return count[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    # Inserts a new player into the player table
    cur.execute("""insert into players (name) values (%s);""", (name, ))
    conn.commit()
    cur.close()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()
    # Fetches all the details of the players and orders it by max wins
    cur.execute("select id, name, wins, matches from players order by wins;")
    players = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return players


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""insert into matches (winner, loser) values (%s, %s);""",
                (winner, loser))
    cur.execute("""update players set matches = matches + 1 where players.id \
                in (%s, %s);""", (winner, loser))
    cur.execute("""update players set wins = wins + 1 where \
                players.id = (%s);""", (winner, ))
    conn.commit()
    cur.close()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    players = playerStandings()
    pairings = []
    pair = ()
    for idx, player in enumerate(players):
        pair = pair + player[:2]
        if ((idx + 1) % 2 == 0):
            pairings.append(pair)
            pair = ()
    return pairings
