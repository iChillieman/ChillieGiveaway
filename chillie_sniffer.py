import json
from web3 import Web3, exceptions
from sqlite3 import OperationalError
import asyncio
from chillie_db import db_insert_transfer, db_insert_sell, db_insert_buy, db_fetch_all_pools
from chillie_util import init_db, get_contract_abi, setLogger
from config import LOG_NAME, TOKEN_ADDRESS
import time
import traceback
from dotenv import load_dotenv
import os

setLogger(LOG_NAME)

# Load Secrets from .env
load_dotenv()
ether_scan_api_key = os.getenv('ETHER_SCAN_API_KEY')
alchemy_key = os.getenv('ALCHEMY_API_KEY')

# Fetch all known Pools 
# If this is the first time running the script, the database will be setup before tracking transfers!
try:
    pre_processed = db_fetch_all_pools()
except OperationalError as e:
    if str(e).find("no such table") != -1:
        print("Lets set up your Database!")
        init_db()
        pre_processed = db_fetch_all_pools()

# Im using Alchemy Here - But you can use whatever RPC you want to use!
rpc_url = "https://eth-mainnet.g.alchemy.com/v2/{}".format(alchemy_key)

# Connect!
web3 = Web3(Web3.HTTPProvider(rpc_url))
if web3.is_connected():
    print('Welcome Chillieman! - Lets Watch some ERC-20 Transactions!')
else:
    print('Failed to connect to Blockchain!')
    exit()

# Token Contract Init
token_address = Web3.to_checksum_address(TOKEN_ADDRESS)
token_abi = get_contract_abi(token_address, ether_scan_api_key)
token_contract = web3.eth.contract(token_address, abi=token_abi)

all_pools = []
for p in pre_processed:
    all_pools.append(web3.to_checksum_address(p))
    
# Contract Disctionary so you dont have to keep creating Contract Objects that were already created.
contact_mapping = {}

def calculate_eth_spent(predicted_buyer, txn):
    try:
        transaction = web3.eth.get_transaction(txn)
        
        # Extract Actual Buyer to make sure this isnt a spoofed transfer.
        actual_buyer = str(web3.to_json(transaction['from'])).strip('"')
        
        wei_spent = web3.to_json(transaction['value'])
        eth_spent = web3.from_wei(int(wei_spent), 'Ether')
        print("{} - Amount Paid in ETH: {}".format(txn, eth_spent))
        if eth_spent == 0:
            contract_address = Web3.to_checksum_address(web3.to_json(transaction['to']).strip('"'))
            try:
                print("[{}] - Found Contract In Map".format(contract_address))
                contract = contact_mapping[contract_address]
            except KeyError as e:
                print("[{}] - Could NOT find Contract In Map".format(contract_address))
                contract_abi = get_contract_abi(contract_address, ether_scan_api_key)
                contract = web3.eth.contract(contract_address, abi=contract_abi)
                contact_mapping[contract_address] = contract
            input_txn = web3.to_json(transaction['input']).strip('"')
            # TODO - This implementation is insufficient - Need to figure out a way to see how much ETH they paid when using an aggregator / Proxy as Vaule is 0
            #print(contract.decode_function_input(input_txn))
            # eth_spent = calculated_buy_amount

       
        actual_buyer = str(web3.to_json(transaction['from'])).strip('"')
        
        if predicted_buyer == actual_buyer:
            # Not Spoofed
            db_insert_buy(predicted_buyer, eth_spent, txn)
        else:
            # Spoofed
            print("Not counting this as a buy....")
            print("Predicted Buyer: {}".format(predicted_buyer))
            print("Actual Buyer: {}".format(actual_buyer))
        
    except exceptions.TransactionNotFound as e:
        print("{} - NOT FOUND - Could not Retrieve transaction for txn. FML".format(txn))
        traceback.print_exc()
    except Exception as e:
        print("{} - EXCEPTION - Could not Retrieve transaction for txn. FML".format(txn))
        traceback.print_exc()
        
        
# Function to handle Transfers
# Detect if the Transfer is a BUY or SELL by comparing the to and from with the known liquidity pairs.
async def handle_transfer(transfer):
    #print(transfer)
    from_address = web3.to_checksum_address(transfer['args']['from'])
    to_address = web3.to_checksum_address(transfer['args']['to'])

    #Get the TXN (Check this if its a Buy - BIGGEST BUYER May get reward)
    txn = str(web3.to_json(transfer['transactionHash'])).strip('"')
    
    # Store Basic Info
    db_insert_transfer(to_address, from_address, txn)
    
    is_buy = False
    is_sell = False
    if(from_address == to_address):
        print("{} - Sent To Self?".format(txn))
        return
    
    #Check for Buy / Sell using all pools
    for p in all_pools:
        if from_address == p:
            print("{} - We got a Buyer!".format(txn))
            is_buy = True
        elif to_address == p:
            print("{} - We got a Seller!".format(txn))
            is_sell = True
            
    if is_sell:
        #Its a Sale - Disqualify this TXN from Giveaway!
        db_insert_sell(from_address, txn)
    elif is_buy:
        # Its a Buy - What a fucking legend!
        calculate_eth_spent(to_address, txn)
    else:
        print("{} - Just a Transfer!".format(txn))
        # Might want to Enter this into DB as a Transfer!
    

# Im Loopy AF!
async def im_loopy(transfer_filter, poll_interval):
    print("Streaming Transfers!")
    while True:
        for t in transfer_filter.get_new_entries():
            
            # Handle Async.
            asyncio.create_task(handle_transfer(t))

        await asyncio.sleep(poll_interval)

# Listen for the Transfer Events of a Token.
# run the im_loopy function above every 5 seconds
def main():
    transfer_filter = token_contract.events.Transfer.create_filter(fromBlock='latest')
    
    while True:
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(
                asyncio.gather(
                    im_loopy(transfer_filter, 5)  # Check for Transfers every 5 seconds.
                )
            )
        except ValueError as err:
            print(err)
            args = err.args[0]
            error = args['code']
            #Error Code -32000 happens when Connection was lost
            if int(error) == -32000:
                print("Restarting... " + args['message'])
                
                # We dont Quit. We Run forever!
                transfer_filter = token_contract.events.Transfer.create_filter(fromBlock='latest')
            else:
                break
        except:
            break

    loop.close()


main()
