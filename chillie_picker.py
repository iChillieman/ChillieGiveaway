import json
import sqlite3
from chillie_db import db_pick_a_presale_winner_who_never_sold, db_reset_giveaway
from chillie_exception import NoobException
from chillie_util import setLogger

setLogger("log_imma_noob.log")

# TODO - Finish this Script - All the data is there, you just need to know how to use it.
try:
    winner = db_pick_a_presale_winner_who_never_sold()
    second_winner = db_pick_a_winner_who_spent_the_most()
    # TODO - Hook Into [Twitter] ChilliePicker to pull a winner from Twitter Giveaway.
except NoobException as e:
    print("Noob never finished the Database Function.")

# Time to Flush the Database of all Sells, Transfers, and Buys to start a new Giveaway!
db_reset_giveaway()
raise NoobException("Never Finished the chillie_picker script")
