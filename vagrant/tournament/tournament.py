#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
# I used the Udacity forum to help me write the code
# I also looked at different online forum such as Stack Overflow and
# http://www.w3schools.com/sql to help me
# My husband helps me correct this code.

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    my_connection = connect()
    cursor = my_connection.cursor()
    cursor.execute ("update standings set number_win = 0, number_match = 0")
    my_connection.commit()
    my_connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    my_connection = connect()
    cursor = my_connection.cursor()
    cursor.execute ("delete from standings")
    cursor.execute ("delete from players")
    my_connection.commit()
    my_connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    my_connection = connect()
    cursor = my_connection.cursor()
    cursor.execute("select count (*) from players")
    number_players = cursor.fetchall()[0][0]
    my_connection.close()
    return number_players


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # at the same time that a player is registered, he/she is also recoreded in the
    # table standings with no win and no match played. This is to initialize the table standings.
    # The table standing will be updated after each round.
    my_connection = connect()
    cursor = my_connection.cursor()
    clean_name = bleach.clean(name)
    cursor.execute("insert into players(name) values (%s)",(clean_name,))
    cursor.execute("select max(P_id) from players")
    p_id = cursor.fetchall()[0][0]
    cursor.execute("insert into standings(P_id, number_win, number_match) values (%s, %s, %s)",(p_id,0,0))
    my_connection.commit()
    my_connection.close()



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list is the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    my_connection = connect()
    cursor = my_connection.cursor()
    cursor.execute("""select players.P_id as id, players.name as name,
                    standings.number_win as wins,
                    standings.number_match as matches
                    from players left join standings on players.P_id = standings.P_id
                    order by wins desc""")
    standing = cursor.fetchall()
    my_connection.close()
    return standing

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # In this function, the winner got his/her number of wins increased by one and his/her
    # number of matches increased by one.
    # the loser got only his/her number of matches increased by one
    my_connection = connect()
    cursor = my_connection.cursor()
    cursor.execute ("""update standings set number_win = number_win + 1,
                    number_match = number_match + 1
                    where P_id = %s""", (winner,))
    cursor.execute("""update standings set number_match = number_match + 1
                    where P_id = %s""", (loser,))
    my_connection.commit()
    my_connection.close()
 
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
    # for each pair the player1 is the first player and is defined by his/her id and name.
    # the player2 is the second player. He/she is also defined by his/her id and name.
    # in this function all the players in an odd number position in the standing list will be
    # considered as the first player and all players in an even number position in the standing list
    # will be considered as the second player
    # the function first determines the first player then the second one. When this one is determined,
    # then the function merge the 2 tuples player1 and player2 into one tuple and add this tuple to
    # the list of pair of players
    list_of_pairs = []
    player1 = ()
    player2 = ()
    standing = playerStandings()
    player_position_in_standing = 0
    for player in standing:
        player_position_in_standing += 1
        if player_position_in_standing % 2 == 1:
            player1 = (player[0], player[1])
        else:
            player2 = (player[0], player[1])
            players_pair = player1 + player2
            list_of_pairs.append(players_pair)        

    return list_of_pairs        
            





    

