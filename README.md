# How to get pending transactions using python

Pending transactions are transactions that have not been included in a block. They are signed so EVM will try to execute them but they may fail for a number of reasons (sender cancelled it by front running cancel transaction, smart contract logic will fail or execution's cost will exceed the gas limit).

## Install required libraries

```bash
pip install --no-cache-dir -r requirements.txt
```

## Create websocket client

If we want to lisen to pending transactions, we need to create a websocket connection. You gonna need websocket node endpoint address.


```python
import json
from pprint import pprint
from web3 import Web3
from dotenv import load_dotenv
import os

# Loading the .env file
load_dotenv()

wss_url = os.getenv('WSS_URL')

web3_client = Web3(Web3.WebsocketProvider(wss_url))

pprint(web3_client.isConnected())
```

After that we will get all pending transactions and listen to them. We can get transaction and after that filter them by value or by function.

```python
for tx in pending_transactions:
    transaction = web3_client.eth.getTransaction(tx)
    if transaction and transaction.value > 2:
        pprint(dict(transaction))
```

## Filter transactions by contract address and get input data

To get data from transaction we need to create contract object.

```python
web3_client = Web3(Web3.WebsocketProvider(wss_url))

uniswap_router = web3_client.eth.contract(
    address='0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45',
    abi=json.loads(open('uniswap_router_2.json').read())
)

quickswap_router = web3_client.eth.contract(
    address='0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff',
    abi=json.loads(open('quickswap_router.json').read())
)
```

After that we lisen to pending transactions and like before and filter by address. If address is equal to contract address, we can get input data by using _decode_function_input_ from contract object.

```python
def handle_event(event):
    try:
        transaction = dict(web3_client.eth.getTransaction(event))
    except Exception:
        return

    # Here you can add filtering
    if not transaction.get('to'):
        return
    if transaction.get('to') == uniswap_router.address:
        pprint(transaction)
        decoded_data = uniswap_router.decode_function_input(transaction.get('data'))
    elif transaction.get('to') == quickswap_router.address:
        pprint(transaction)
        decoded_data = quickswap_router.decode_function_input(transaction.get('input'))
        pprint(decoded_data)
```

## Sources and useful links

* [Python web3 docs](https://web3py.readthedocs.io/en/stable/index.html) - Your main source of information about web3 in Python.
* [Alchemy](https://www.alchemy.com/) - You can get websocket endpoint for your blockchain here.
* [How to create your own front running bot with ethers.js and FastlyNode](https://coinsbench.com/how-to-create-your-own-front-running-bot-with-ethers-js-and-fastlynode-f18e31de1c3e) - Same thing as shown in this repo but in node.js.
* [Polyscan](https://polygonscan.com/) - You can get smart contracts ABIs here (for polygon network if you are using diffrent network use ).

In case of futher questions, please create Issue with label "Question".