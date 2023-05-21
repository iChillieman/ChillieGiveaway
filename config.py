# What do you want the Database to be called?
DB_NAME = 'giveaway.db'

#What do you want the Log file to be called?
LOG_NAME = 'log_chillieman.log'

# What Contract Addresses should be watched to recognize Buy / Sell?
# As an Example, Im using a couple of PEPE's Pairs
LIQUIDITY_PAIRS = [
    '0xa43fe16908251ee70ef74718545e4fe6c5ccec9f',
    '0x11950d141ecb863f01007add7d1a342041227b58'
]

# Do you have a list of Presales you want to Import? 
# Debating, but probably not - Fair Launches are better
IS_PRESALE_APPLICABLE = False

# What is the CSV called to import Presale?
# IMPORTANT - Wallet Address must be the first value of every row.
PRESALE_CSV_FILENAME = 'example.csv'

# Does your CSV have column Headers?
# IF the First line of your CSV contains Columns, Set this to 1
CSV_START_LINE = 0

# What Token are we Tracking?? For Example im Using PEPE
TOKEN_ADDRESS = '0x6982508145454ce325ddbe47a25d4ec3d2311933'
