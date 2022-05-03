class Transaction:
    method = ""
    token = ""
    address_from = ""
    address_to = ""
    value = 0


    # def __init__(self, method, token, address_from, address_to, value):
    #     self.method = method
    #     self.token = token
    #     self.address_from = address_from
    #     self.address_to = address_to
    #     self.value = value


    def record_received_tx(self, my_address, receipt, value):
        self.method = "received"
        self.token = "Ether"
        self.address_from = receipt["from"]
        self.address_to = my_address
        self.value = value[2]

    
    def record_sent_tx(self, my_address, receipt, value):
        self.method = "sent"
        self.token = "Ether"
        self.address_from = my_address
        self.address_to = receipt["to"]
        self.value = value[2]


    def record_approval_tx(self, web3, my_address, contract, log):
        # To check if the wallet address is in the logs
        # if my_address[-40:].lower() in web3.toHex(log["topics"][1]) or my_address[-40:].lower() in web3.toHex(log["topics"][2]):
        self.method = "approve"
        self.token = contract.functions.name().call()
        self.address_from = f"0x{log['topics'][1].hex()[-40:]}"
        self.address_to = f"0x{log['topics'][2].hex()[-40:]}"
        if self.token == "Wrapped BTC":
            self.value = web3.fromWei(int(log["data"], 0), "ether")*10000000000
        else:
            self.value = web3.fromWei(int(log["data"], 0), "ether")
    

    def record_trf_tx(self, web3, my_address, contract, log):
        # To check if the wallet address is in the logs
        # if my_address[-40:].lower() in web3.toHex(log["topics"][1]) or my_address[-40:].lower() in web3.toHex(log["topics"][2]):
        self.method = "transfer"
        self.token = contract.functions.name().call()
        self.address_from = f"0x{log['topics'][1].hex()[-40:]}"
        self.address_to = f"0x{log['topics'][2].hex()[-40:]}"
        if self.token == "Wrapped BTC":
            self.value = web3.fromWei(int(log["data"], 0), "ether")*10000000000
        else:
            self.value = web3.fromWei(int(log["data"], 0), "ether")


    def __str__(self):
        """print out different detail base on transaction method used"""
        if self.method == "transfer":
            return f"Sent {self.value} {self.token} from {self.address_from} to {self.address_to}"
        elif self.method == "received":
            return f"Received {self.value} {self.token} from {self.address_from}"
        elif self.method == "sent":
            return f"Sent {self.value} {self.token} to {self.address_to}"
        elif self.method == "approve":
            if self.value >= 115792089237316195423570985008687907853269984665640564039457:
                return f"Approved infinate {self.token} to {self.address_to}"
            else:
                return f"Approved {self.value} {self.token} to {self.address_to}"
        elif self.method == "failed":
            return "Transaction failed!"
        else:
            return "No transaction!"