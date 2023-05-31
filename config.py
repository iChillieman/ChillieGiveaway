# What do you want the Database to be called?
DB_NAME = 'giveaway.db'

#What do you want the Log file to be called?
LOG_NAME = 'log_giveawayToken.log'

# What Contract Addresses should be watched to recognize Buy / Sell?
LIQUIDITY_PAIRS = [
    '0xf08B1E2B69C24D793BD49B32db6527dF769e067E'
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

# What Token are we Tracking??
TOKEN_ADDRESS = '0x8FF5cAc06632935b08DdCa93F357A29cA52f312B'
