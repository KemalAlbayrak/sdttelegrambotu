from datetime import datetime
import requests
import tkinter as tk
from threading import Thread
import module1
from web3 import Web3
from web3.auto import w3
import time
from eth_account import Account








# Telegram bot API adresi
api_url = "https://api.telegram.org/bot{}/".format("6061072792:AAFudxNkyoMaQh1OJ0lxpOZPR_QlFIAfDjE")


# Kullanıcı kimliği
chat_id = "5502678421"

#User Data
global UserMetaMaskPrivateKey
UserMetaMaskPrivateKey = None
private_key = UserMetaMaskPrivateKey

# Mesaj metinleri
merhaba_mesaji = "Merhaba! Benim adım ShoppingDoge AI. Nasıl yardımcı olabilirim?"
telegram_mesaji = "Shopping Doge Telegram adresi: https://t.me/ShoppingDoge benimle işlem yapmak için bu telegram adresine katılmalısınız. Görünüşe göre siz zaten Shopping Doge Telegram grubuna üyesiniz."
komut_mesaji="Komut Listesi:\n/telegram\n/web\n/buy\n/sell\n/account\n/list\n/metainfo"
accountacces_mesaji="İşlem yapmak için Metamask Private Key'inize ihtiyacım var. Lütfen Private Key'inizi buraya yazın:"
web_mesaji="Shopping Doge Web sitesi'ne bu adrese tıklayarak ulaşabilirsiniz: www.shoppingdoge.net"


#console
print("UserMetaMaskPrivateKey:", UserMetaMaskPrivateKey)


########

rpc_url = "https://mainnet.infura.io/v3/5fa20386a6a6414b87bc668959475142"

# Web3 object creation
web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/5fa20386a6a6414b87bc668959475142"))


########


def send_message(mesaj):
    """
    Belirtilen metni Telegram üzerinden belirtilen kullanıcıya gönderir.
    """
    url = api_url + "sendMessage"
    data = {"chat_id": chat_id, "text": mesaj}
    requests.post(url, data=data)


def get_private_key():
    global UserMetaMaskPrivateKey
    while True:
        try:
            url = api_url + "getUpdates"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                result = data["result"]
                if result:
                    last_update_id = result[-1]["update_id"]
                    last_message = result[-1]["message"]
                    chat_id = last_message["chat"]["id"]
                    text = last_message["text"]
                    if len(text) == 64:
                        UserMetaMaskPrivateKey = text
                        send_message("Özel anahtar başarıyla kaydedildi.")
                        break
                    else:
                       print("Private Key'inizi girmeniz bekleniyor... Unutmayın Private Key'iniz 64 karakter uzunluğunda bir onaltılık sayıdır.")
                       time.sleep(1)
                else:
                    continue
            else:
                continue
        except requests.exceptions.RequestException as e:
            print("Hata:", e)

def get_balance(private_key):
    global chat_id
    account = web3.eth.account.from_key(private_key)
    address = account.address
    balance_wei = web3.eth.get_balance(address)

    if balance_wei is None or balance_wei == 0:
        return 0, 0

    balance_eth = web3.fromWei(int(balance_wei), 'ether')

    # Hesap adını almak için RPC çağrısı yap
    try:
        account_name = web3.personal.listAccounts().index(address)
    except ValueError:
        account_name = None

    return account_name, balance_eth

def get_wallet_name(private_key):
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/5fa20386a6a6414b87bc668959475142'))
    account = w3.eth.account.from_key(private_key)
    address = w3.toChecksumAddress(account.address)
    url = f"FBGNTN3JKKUSZDIWHGI5GKUIE1YGJM2CJR"
    response = requests.get(url)
    if response.status_code == 200:
        balance = float(response.json()["result"]) / 10**18
        return f"{address} ({balance:.2f} ETH)"
    else:
        return "Hesap bulunamadı."


def show_private_key():
    global UserMetaMaskPrivateKey
    if not UserMetaMaskPrivateKey:
        print("UserMetaMaskPrivateKey is not set.")
        return
    print("UserMetaMaskPrivateKey:", UserMetaMaskPrivateKey)



def metainfo(update, context):
    global chat_id, UserMetaMaskPrivateKey

    # Eğer private key girmemişse kullanıcıya mesaj gönder
    if not UserMetaMaskPrivateKey:
        send_message("Please enter your MetaMask private key first.")
        return

    # Cüzdan bilgilerini al
    account = web3.eth.account.from_key(UserMetaMaskPrivateKey)
    address = account.address
    balance = get_balance(UserMetaMaskPrivateKey)
    account_name = "My Account"  # Hesap adını burada tanımlayabilirsiniz

    # Cüzdan bilgilerini gönder
    if balance[0] is None:
        send_message(f"Hesap isminiz: {account_name}\nCüzdan adresiniz: {address}\nCüzdanınızdaki ETH miktarı: {balance[1]} ETH.")
    else:
        send_message(f"Hesap isminiz: {account_name}\nCüzdan adresiniz: {address}\nHesap adınız: {balance[0]}\nCüzdanınızdaki ETH miktarı: {balance[1]} ETH.")

def transfer_eth(private_key, to_address, amount):
    account = web3.eth.account.from_key(private_key)
    address = account.address
    value = w3.toWei(amount, 'ether')
    transaction = {
        'to': to_address,
        'value': value,
        'gas': 200000,
        'gasPrice': w3.toWei('50', 'gwei'),
        'nonce': web3.eth.getTransactionCount(address)
    }
    signed_txn = account.sign_transaction(transaction)
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3.toHex(tx_hash)

def read_messages():
    global UserMetaMaskPrivateKey
    last_update_id = None
    while True:
        try:
            url = api_url + "getUpdates"
            if last_update_id:
                url += "?offset={}".format(last_update_id + 1)
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                result = data["result"]

                if result:
                    last_update_id = result[-1]["update_id"]
                    last_message = result[-1]["message"]
                    chat_id = last_message["chat"]["id"]
                    text = last_message["text"]

                    if text == "/start":
                        send_message(merhaba_mesaji)
                        send_message(komut_mesaji)
                    elif text == "/telegram":
                        send_message(telegram_mesaji)
                    elif text == "/buy":
                        send_message(accountacces_mesaji)
                        get_private_key()
                        if UserMetaMaskPrivateKey:
                            send_message("Private key: {}".format(UserMetaMaskPrivateKey))
                    elif text == "/sell":
                        send_message("Bu özellik henüz mevcut değil.")
                    elif text == "/list":
                        send_message(komut_mesaji)
                    elif text == "/web":
                        send_message(web_mesaji)
                    elif text == "/metainfo":
                        if UserMetaMaskPrivateKey:
                            balance = get_balance(UserMetaMaskPrivateKey)
                            message = "Private key: {}\nCüzdanındaki ETH miktarı ({}) ETH.".format(UserMetaMaskPrivateKey, balance)
                            send_message(message)
                        else:
                            send_message("Lütfen önce MetaMask hesabınızı açın ve /buy komutu ile hesabınıza erişin.")
                    else:
                        send_message("Kullanabileceğiniz komutlar: /telegram, /buy, /sell, /web, /metainfo")




        except requests.exceptions.RequestException as e:
            print("Hata:", e)










if __name__ == "__main__":
    send_message(merhaba_mesaji)
    read_messages()











      





