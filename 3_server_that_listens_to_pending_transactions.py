from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pprint import pprint
from web3 import Web3
from dotenv import load_dotenv
import os
import asyncio
from pprint import pprint

# Loading the .env file
load_dotenv()

wss_url = os.getenv('WSS_URL')

web3_client = Web3(Web3.WebsocketProvider(wss_url))

uniswap_router = web3_client.eth.contract(
    address='0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45',
    abi=json.loads(open('uniswap_router_2.json').read())
)

quickswap_router = web3_client.eth.contract(
    address='0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff',
    abi=json.loads(open('quickswap_router.json').read())
)

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


async def log_loop(event_filter, poll_interval):
    while True:
        try:
            for event in event_filter.get_new_entries():
                handle_event(event)
            await asyncio.sleep(poll_interval)
        except Exception:
            await asyncio.sleep(poll_interval)
            continue


def main():
    tx_filter = web3_client.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(tx_filter, 2)))
    finally:
        loop.close()

if __name__ == '__main__':
    main()
