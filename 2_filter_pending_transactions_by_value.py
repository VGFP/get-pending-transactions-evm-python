import json
from pprint import pprint
from web3 import Web3
from dotenv import load_dotenv
import os

# Loading the .env file
load_dotenv()

wss_url = os.getenv("WSS_URL")

web3_client = Web3(Web3.WebsocketProvider(wss_url))

pprint(web3_client.isConnected())

pending_transactions = web3_client.eth.filter("pending").get_new_entries()


for tx in pending_transactions:
    try:
        transaction = web3_client.eth.getTransaction(tx)
        # Remember that value in in Wei and 1 Eth (or other gas token for bockchain like BNB or MATIC) is 10^18 Wei
        if transaction and transaction.get("value") > 2:
            pprint(dict(transaction))
    except Exception:
        # In case of error, just ignore it for this example
        continue
