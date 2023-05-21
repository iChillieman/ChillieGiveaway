import sqlite3
from decimal import Decimal
from config import DB_NAME
from chillie_exception import NoobException

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
            
    c.execute('CREATE TABLE pool (address TEXT PRIMARY KEY)')
    c.execute('CREATE TABLE presale (address TEXT PRIMARY KEY)')
    
    # Base Transfer Event
    c.execute('''CREATE TABLE transfer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                to_address TEXT NOT NULL,
                from_address TEXT NOT NULL,
                txn TEXT NOT NULL
            )''')
    
    # Specific Buy Data
    c.execute('''CREATE TABLE buy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL,
                eth_spent REAL NOT NULL,
                txn TEXT NOT NULL
            )''')

    # Specific Sell Data
    c.execute('''CREATE TABLE sell (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL,
                txn TEXT NOT NULL
            )''')
            
    # Cache for ABIs to Load Contracts.
    c.execute('''CREATE TABLE abi (
                address TEXT PRIMARY KEY,
                abi TEXT NOT NULL
            )''')

    conn.commit()
    conn.close()

# Fetches
def db_fetch_all_pools():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('SELECT * FROM pool')
    all_pools = c.fetchall()

    extract = []
    for p in all_pools:
        extract.append(p[0])
        
    conn.close()
    return extract
    
def db_fetch_abi(address):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('SELECT abi FROM abi WHERE address=:address', {'address': address}) 
    abi = c.fetchone()
    
    conn.close()
    return abi
    
# Inserts
def db_insert_pool(address):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        c.execute('INSERT INTO pool VALUES (:address)' , {'address': address})
        print('{} Pool has been added'.format(address))
    except e as Exception:
        print('Stop being retarded, {} is already added!'.format(address))

    conn.commit()
    conn.close()
    
def db_insert_presale(address):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        c.execute('INSERT INTO presale VALUES (:address)' , {'address': address})
        print('{} Presale Address has been added!'.format(address))
    except e as Exception:
        print('Stop being retarded, {} is already added!'.format(address))

    conn.commit()
    conn.close()
    
def db_insert_transfer(to_address, from_address, txn):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        'INSERT INTO transfer VALUES (null, :to_address, :from_address, :txn)' , 
        {'to_address': to_address, 'from_address': from_address, 'txn': txn}
    )
        
    conn.commit()
    conn.close()


def db_insert_buy(address, eth_spent, txn):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        'INSERT INTO buy VALUES (null, :address, :eth_spent, :txn)' , 
        {'address': address, 'eth_spent': str(eth_spent), 'txn': txn}
    )

    conn.commit()
    conn.close()

def db_insert_sell(address, txn):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        'INSERT INTO sell VALUES (null, :address, :txn)', 
        {'address': address, 'txn': txn}
    )

    conn.commit()
    conn.close()
    
def db_insert_abi(address, abi):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('INSERT INTO abi VALUES (:address, :abi)', 
            {'address': address, 'abi': abi}
        )

    conn.commit()
    conn.close()

# Clear all Transfers / Buys / and Sells
def db_reset_giveaway():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('DELETE FROM buy')
    c.execute('DELETE FROM sell')
    c.execute('DELETE FROM transfer')

    conn.commit()
    conn.close()

# You should know how to complete this function to select your winner. If not, you are not qualified to use this script.
def db_pick_a_winner_who_spent_the_most():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # TODO - Use a SQL Statement to select the TOP wallets in the BUY Table.
    # NOTE - Make sure you subtract the total sum of value in the SELL table.
    raise NoobException("You never implemented the Most Spent Winner Function")

    conn.commit()
    conn.close()
    
# TODO - Consider whether a Presale should even be used
# You should know how to complete this function to select your winner. If not, you are not qualified to use this script.  
def db_pick_a_presale_winner_who_never_sold():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # TODO - Use a SQL Join Statement to someone who appears in the Presale List, But DOES NOT appear in the Sell Table.
    raise NoobException("You never implemented the Presale Winner Function")
    
    conn.commit()
    conn.close()
