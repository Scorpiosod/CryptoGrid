from tkinter import *
import DecodeData


class MainWindow:

    def __init__(self):
        window = Tk()  # Create a window
        window.title("CryptoGrid")  # Set title

        Label(window, text = "Please enter etherscan API key").grid(row = 1, column=1, sticky=W)
        Label(window, text="Please enter infura key").grid(row=2, column=1, sticky=W)
        Label(window, text="Please enter wallet address").grid(row=3, column=1, sticky=W)


        self.apiKey = StringVar()
        Entry(window, textvariable=self.apiKey, justify=RIGHT).grid(row=1, column=2)

        self.infuraKey = StringVar()
        Entry(window, textvariable=self.infuraKey, justify=RIGHT).grid(row=2, column=2)

        self.walletAddress = StringVar()
        Entry(window, textvariable=self.walletAddress, justify=RIGHT).grid(row=3, column=2)

        btSaveKeys = Button(window, text="Save Keys", command=self.saveKeys).grid(row=4, column=1, sticky=E)
        btSearchTx = Button(window, text="Search Transactions", command=self.searchTx).grid(row=4, column=2, sticky=E)

        self.frame1 = Frame(window)
        self.frame1.grid(row=5, column=1, columnspan=2, sticky=W)
        self.scrollbar = Scrollbar(self.frame1)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.text = Text(self.frame1, width=150, height=10, wrap=WORD,
                    yscrollcommand=self.scrollbar.set)
        self.text.pack()
        self.scrollbar.config(command=self.text.yview)

        window.mainloop()  # Create an event loop


    def saveKeys(self):
        DecodeData.api_key = self.apiKey.get()
        DecodeData.my_address = self.walletAddress.get()
        DecodeData.infura_url = self.infuraKey.get()
        print(DecodeData.api_key)
        print(DecodeData.my_address)
        print(DecodeData.infura_url)



    def searchTx(self):
        txs = DecodeData.getTxDetails(5)
        txs = DecodeData.processTxDetails(txs)
        for key, value in txs.items():
            transaction = f"#{value[0]}: Hash({key}), method = {value[1]}, ETH amount {value[2]}"
            self.text.insert(END, transaction + "\n")
            for i in value[3]:
                transaction = f"====={i}"
                self.text.insert(END, transaction + "\n")



MainWindow() # Create GUI
