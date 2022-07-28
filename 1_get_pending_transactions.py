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

pprint(pending_transactions)
try:
    pending_transaction = dict(web3_client.eth.get_transaction(pending_transactions[0]))
# Error handling
except Exception as e:
    print(e)
    pending_transaction = None
pprint(pending_transaction)

# Example output:
"""
{
 'blockHash': None,
 'blockNumber': None,
 'from': '0xAE374e55BCEd1a0EA63227d098149EDBc1E38552',
 'gas': 887154,
 'gasPrice': 63000000000,
 'hash': HexBytes('0x14f29214a735b7b1d13b09121b47c834bfe662a1e9f6d1b2cf0348fb987a4e1b'),
 'input': '0xa6417ed600000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000002a407316000000000000000000000000000000000000000000000000000000002a32354a',
 'nonce': 72,
 'r': HexBytes('0x1e4904bf8e3fbfe421957fc7f44fe17d8d03982ac2e6207bcc03609c00733cd9'),
 's': HexBytes('0x75dd9ef127b0f07304ca5981a54330689b6dd9dfadee60012da3cf825a7e3b96'),
 'to': '0x445FE580eF8d70FF569aB36e80c647af338db351',
 'transactionIndex': None,
 'type': '0x0',
 'v': 310,
 'value': 0
}
 """
