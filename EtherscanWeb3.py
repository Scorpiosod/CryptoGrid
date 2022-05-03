import requests
import json
import re
from web3 import Web3


# All functions using Web3
# To create web3 link
def web3CreateLink(infura_url):
    web3 = Web3(Web3.HTTPProvider(infura_url))
    if web3.isConnected():
        print("Web3 Connection is Valid")
        return web3


# Get transaction receipt for a specifie transaction hash using web3
def web3GetReceipt(web3, tx_hash):
    receipt = web3.eth.get_transaction_receipt(tx_hash)
    return receipt


# Create a list of logs from transaction receipt using web3
def web3GetLogs(web3, tx_hash):
    receipt = web3GetReceipt(web3, tx_hash)
    logs = [log for log in receipt["logs"]]
    return logs


# Create a contract using ABI(Application Binary Interface) info downloaded from etherscan.io
def web3Contract(web3, contract_address, api_key):
    abi = getContractAbi(contract_address, api_key)
    contract = web3.eth.contract(address=contract_address, abi=abi["result"])
    return contract


# To find the method used in a transaction from contract abi
def web3ContractMethod(contract, tx):
    try:
        func_obj, func_params = contract.decode_function_input(tx["input"])
        pattern = r"Function (.*)\("
        method = re.search(pattern, str(func_obj)).group(1)
        return method
    except:
        method = "Unkown Contract"
        return method


# Etherscan api
# To find all the transactions in a wallet address
def getTxByAddress(address, api_key, start=1, count=10):
    url = ("https://api.etherscan.io/api"
            "?module=account"
            "&action=txlist"
            f"&address={address}"
            "&startblock=0"
            "&endblock=99999999"
            f"&page={start}"
            f"&offset={count}"
            "&sort=asc"
            f"&apikey={api_key}")
    apiRequest = requests.get(url)
    tx = json.loads(apiRequest.content)
    print(f"{len(tx['result'])} result returned")
    return tx


# To get receipt for a specific transaction hash using etherscan.io
def getReceiptByHash(tx_hash, api_key):
    url = ("https://api.etherscan.io/api"
            "?module=proxy"
            "&action=eth_getTransactionReceipt"
            f"&txhash={tx_hash}"
            f"&apikey={api_key}")
    api_request = requests.get(url)
    receipt = json.loads(api_request.content)
    return receipt


# Create a list of logs from transaction receipt using etherscan.io
def getLogs(tx_hash, api_key):
    receipt = getReceiptByHash(tx_hash, api_key)
    logs = [log for log in receipt["result"]["logs"]]
    return logs


# Get contract ABI(Application Binary Interface) with the contract addresss
def getContractAbi(contract_address, api_key):
    abi_endpoint = ("https://api.etherscan.io/api"
                    "?module=contract"
                    "&action=getabi"
                    f"&address={contract_address}"
                    f"&apikey={api_key}")
    abi = json.loads(requests.get(abi_endpoint).content)
    return abi

