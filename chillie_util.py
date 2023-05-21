import json
import sys
import traceback
import csv
from chillie_db import db_fetch_abi, db_insert_abi, create_tables, db_insert_pool, db_insert_presale
from config import LIQUIDITY_PAIRS, IS_PRESALE_APPLICABLE, PRESALE_CSV_FILENAME, CSV_START_LINE
from web3 import Web3, exceptions
import requests

# Log Content to File as well as Console with this class.
class Logger(object):
    def __init__(self, file_name):
        self.terminal = sys.stdout
        self.log = open(file_name, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        pass    

def setLogger(file_name):
    sys.stdout = Logger(file_name)


# If you dont want to get an Ether Scan API Key to fetch ABI's There, you can change this to use Web3 instead.
def get_contract_abi(contract_address, ether_scan_api_key):
    contract_address = Web3.to_checksum_address(contract_address)
    
    # First Attempt to check 
    from_db = db_fetch_abi(contract_address)
    if from_db == None:
        url = "https://api.etherscan.io/api?module=contract&action=getabi&address={}&apikey={}".format(contract_address, ether_scan_api_key)
        response = requests.get(url).json()
        is_verified = response['status']
        result = response['result']
        if int(is_verified) == 0:
            if not result == 'Contract source code not verified':
                print("Could not get ABI")
                traceback.print_exc()
            abi = None
        else:
            db_insert_abi(contract_address, result)
            abi = result
    else:
        abi = from_db[0]

    return abi
    
def init_db():
    # Create DB, and any other Potential Inits (Import PreSale Addresses?)
    create_tables()

    # Import POOLS to detect 
    for p in LIQUIDITY_PAIRS:
        db_insert_pool(p)

    # Import Presale List from a file:
    # This script assumes the Wallet is the first element of each row.
    if IS_PRESALE_APPLICABLE:
        with open(PRESALE_CSV_FILENAME) as file:
            csv_reader = csv.reader(file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                if line_count < CSV_START_LINE:
                    print('Skipping this Line: {}'.format())
                    line_count += 1
                else:
                    db_insert_presale(row[0])
                    line_count += 1
                    
            print("Imported {} Presale Addresses".format(line_count))