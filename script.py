import threading
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from typing import Optional
import time
import os
from pyquery import PyQuery as pq
import requests
import string
import random
import sys
from colorama import Fore, Style

class AddressChecker(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        while True:
            try:
                mnemonic, address = readdr()
                bal = xBal(address)
                if bal > 0:
                    print(self.name, Fore.GREEN, bal, address, mnemonic)
                    file1 = open("valid.txt", "a")
                    file1.write(f"{bal}'ETH' {address} {mnemonic} \n")
                    file1.close()
            except Exception as e:
                print(f"An exception occured: {e}")

def readdr():   
    MNEMONIC: str = generate_mnemonic(language="english", strength=128)
    PASSPHRASE: Optional[str] = None  # "meherett"
    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
    bip44_hdwallet.from_mnemonic(
        mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE
    )
    bip44_hdwallet.clean_derivation()
    address_index=0
    bip44_derivation: BIP44Derivation = BIP44Derivation(
        cryptocurrency=EthereumMainnet, account=0, change=False, address=address_index
    )
    bip44_hdwallet.from_path(path=bip44_derivation)

    return bip44_hdwallet.mnemonic(),bip44_hdwallet.address()

def xBal(address):
    url = "https://api.ethplorer.io/getAddressInfo/"+address+"?apiKey=freekey"
    response = requests.get(url)
    data = response.json()
    balance = data["ETH"]["balance"]
    return balance

# Create new threads
threads = []
for i in range(1,6):
    thread = AddressChecker(i, f"bot{i}")
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for t in threads:
    t.join()
