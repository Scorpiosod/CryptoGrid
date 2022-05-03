import EtherscanWeb3 as eth
import time
import pandas as pd
from Transaction import Transaction


api_key = ""
my_address = ""
infura_url = ""


transfer_hex = ["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
                "0xe19260aff97b920c7df27010903aeb9c8d2be5d310a2c67824cf3f15396e4c16"]



# Create CSV file for all transaction in a wallet address
def createCSV(tx):
    df = pd.DataFrame(tx["result"])
    df.to_csv("testwallet.csv")


# Create .txt file for all transaction from search result
def createFile(filename, tx):
    with open(filename, "w") as file:
        if "result" in tx:
            if type(tx["result"]) == list:
                for i in tx["result"]:
                    file.writelines(f"{i}\n")
            elif type(tx["result"]) == dict:
                for key, value in tx["result"].items():
                        file.write("{}: {}\n".format(key, value))
        else:
            if type(tx) == list:
                for i in tx:
                    file.writelines(f"{i}\n")
            else:
                for key, value in tx.items():
                        file.write("{}: {}\n".format(key, value))


# Return a dictionary of transactions
# Return format: {transaction hash: [index, method used, amount transfered]}
def getTxDetails(count):
    web3 = eth.web3CreateLink(infura_url)
    tx = eth.getTxByAddress(my_address, api_key, count=count)
    tx = tx["result"]
    txs_details = {}
    for tx, i in zip(tx, range(len(tx)+1)):
        tx_data = []
        # If input = 0x, there is no input data
        if tx["input"] != "0x":
            contract_address = web3.toChecksumAddress(tx["to"])
            contract = eth.web3Contract(web3, contract_address, api_key)
            method = eth.web3ContractMethod(contract, tx)
            # print(f"{i + 1}. {method}")
        else:
            method = "transfer"
        # print(f"{i + 1}. {method}")
        # print(f"tx_hash: {tx['hash']}")
        # print("=" * 50)
        tx_data.append(i + 1)
        tx_data.append(method)
        tx_data.append(web3.fromWei(int(tx["value"]), "ether"))
        txs_details[tx["hash"]] = tx_data
        # Free account for etherscan.io api only can do 5 search per second, this pause is to avoid overuse search limit
        time.sleep(0.3)
    return txs_details


# To decode logs into readable transactions data
def processLogDetails(web3, log):
    # Free account for etherscan.io api only can do 5 search per second, this pause is to avoid overuse search limit
    time.sleep(0.3)
    transaction = Transaction()
    contract = eth.web3Contract(web3, log["address"], api_key)
    events = {}
    abi_events = [abi for abi in contract.abi if abi["type"] == "event"]
    for event in abi_events:
        # Get event signature components
        name = event["name"]
        inputs = [param["type"] for param in event["inputs"]]
        input = ",".join(inputs)
        # Hash event signature
        event_signature_text = f"{name}({input})"
        event_signature_hex = web3.toHex(web3.keccak(text=event_signature_text))
        events[event_signature_hex] = event_signature_text
    receipt_event_signature_hex = web3.toHex(log["topics"][0])
    # Find match between log's event signature and ABI's event signature
    # for key, value in events.items():
    #     print(f"{key}:{value}")
    if receipt_event_signature_hex in transfer_hex:
        for hex in transfer_hex:
            if hex in events:
                if "transfer" in events[hex].lower():
                    transaction.record_trf_tx(web3, my_address, contract, log)
    elif receipt_event_signature_hex in events:
        if "approval" in events[receipt_event_signature_hex].lower():
            transaction.record_approval_tx(web3, my_address, contract, log)
    return transaction


#to decode transactions
def processTxDetails(txs_details={}):
    web3 = eth.web3CreateLink(infura_url)
    for key, value in txs_details.items():
        # To show processing progress
        print(f"Processing tx #{value[0]}")
        receipt = eth.web3GetReceipt(web3, key)
        transactions = []
        #status 0x0 means failed transaction
        if receipt["status"] == 0:
            transaction = Transaction()
            transaction.method = "failed"
            transactions.append(transaction)
        else:
            # If the receipt has no log, it means it is a sending or receiving ETH only transaction
            if not receipt["logs"] and value[1] == "transfer":
                if receipt["to"].lower() == my_address.lower():
                    transaction = Transaction()
                    transaction.record_received_tx(my_address, receipt, value)
                    transactions.append(transaction)
                elif receipt["from"].lower() == my_address.lower():
                    transaction = Transaction()
                    transaction.record_sent_tx(my_address, receipt, value)
                    transactions.append(transaction)
            else:
                # If the receit had logs, then decode the logs one at a time
                logs = eth.web3GetLogs(web3, key)
                for log in logs:
                    transaction = processLogDetails(web3, log)
                    # Making sure valid transaction detail has returned
                    if transaction.method != "":
                        transactions.append(transaction)
        txs_details[key].append(transactions)
    return txs_details


if __name__ == "__main__":
    txs = getTxDetails(5)
    txs = processTxDetails(txs)
    for key, value in txs.items():
        print(f"#{value[0]}: Hash({key}), method = {value[1]}, ETH amount {value[2]}")
        for i in value[3]:
            print(f"====={i}")



