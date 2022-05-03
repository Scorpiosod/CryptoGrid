from tkinter import *
from tkinter import messagebox
import DecodeData


class MainWindow:

    def __init__(self):
        window = Tk()  # Create a window
        window.title("CryptoGrid")  # Set title

        Label(window, text = "Please enter etherscan API key").grid(row = 1, column=1, sticky=W)
        Label(window, text="Please enter infura key").grid(row=2, column=1, sticky=W)
        Label(window, text="Please enter wallet address").grid(row=3, column=1, sticky=W)
        Label(window, text="Please enter transaction range wanted to be search").grid(row=4, column=1, sticky=W)
        Label(window, text="Start:").grid(row=4, column=2, sticky=W)
        Label(window, text="   Range must be less then 30!").grid(row=5, column=1, sticky=W)
        Label(window, text="End:  ").grid(row=5, column=2, sticky=W)


        self.api_key = StringVar()
        Entry(window, textvariable=self.api_key, justify=RIGHT).grid(row=1, column=2)

        self.infura_key = StringVar()
        Entry(window, textvariable=self.infura_key, justify=RIGHT).grid(row=2, column=2)

        self.wallet_address = StringVar()
        Entry(window, textvariable=self.wallet_address, justify=RIGHT).grid(row=3, column=2)

        self.start_tx = IntVar()
        Entry(window, textvariable=self.start_tx, justify=RIGHT).grid(row=4, column=2)

        self.end_tx = IntVar()
        Entry(window, textvariable=self.end_tx, justify=RIGHT).grid(row=5, column=2)

        btSaveKeys = Button(window, text="Save Keys", command=self.save_keys).grid(row=2, column=2, sticky=E)
        btSearchTx = Button(window, text="Search Transactions", command=self.search_tx).grid(row=6, column=2, sticky=E)

        self.frame1 = Frame(window)
        self.frame1.grid(row=7, column=1, columnspan=2, sticky=W)
        self.scrollbar = Scrollbar(self.frame1)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.text = Text(self.frame1, width=150, height=10, wrap=WORD,
                    yscrollcommand=self.scrollbar.set)
        self.text.pack()
        self.scrollbar.config(command=self.text.yview)

        window.mainloop()  # Create an event loop


    def save_keys(self):
        DecodeData.api_key = self.api_key.get()
        DecodeData.my_address = self.wallet_address.get()
        DecodeData.infura_url = self.infura_key.get()
        print(DecodeData.api_key)
        print(DecodeData.my_address)
        print(DecodeData.infura_url)



    def search_tx(self):
        range = self.end_tx.get() - self.start_tx.get()
        if range > 30:
            messagebox.showwarning("Warning", "Range is too large, must be less than 30")
        else:
            txs = DecodeData.get_tx_details(range)
            txs = DecodeData.process_tx_details(txs)
            for key, value in txs.items():
                transaction = f"#{value[0]}: Hash({key}), method = {value[1]}, ETH amount {value[2]}"
                self.text.insert(END, transaction + "\n")
                for i in value[3]:
                    transaction = f"====={i}"
                    self.text.insert(END, transaction + "\n")



MainWindow() # Create GUI
