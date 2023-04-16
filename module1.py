from web3 import Web3
from web3.auto import w3
import chatbot2deneme

rpc_url = "https://mainnet.infura.io/v3/5fa20386a6a6414b87bc668959475142"

# Web3 object creation
web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/5fa20386a6a6414b87bc668959475142"))

# Function to get the balance of the account
def get_balance(private_key):
    # Open the Metamask account
    account = web3.eth.account.from_key(private_key)

    # Get the account address
    address = account.address

    # Get the balance in Ether
    balance = web3.fromWei(web3.eth.getBalance(address), 'ether')

    return balance

# Function to send ETH to a specified address
def transfer_eth(private_key, to_address, amount):
    # Open the Metamask account
    account = web3.eth.account.from_key(private_key)

    # Get the account address
    address = account.address

    # Calculate the value of ETH to be sent in wei
    value = w3.toWei(amount, 'ether')

    # Prepare the transaction details
    transaction = {
        'to': to_address, # recipient's address
        'value': value, # amount of ETH to be sent
        'gas': 200000, # gas limit
        'gasPrice': w3.toWei('50', 'gwei'), # gas price
        'nonce': web3.eth.getTransactionCount(address) # nonce
    }

    # Sign the transaction using the Metamask account
    signed_txn = account.sign_transaction(transaction)

    # Send the transaction to the network
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    # Return the transaction hash
    return web3.toHex(tx_hash)

def metainfo(update, context):
    # Get the private key of the Metamask account
    private_key = chatbot2deneme.UserMetaMaskPrivateKey

    # Get the balance of the account
    balance = get_balance(private_key)

    # TODO: Call the transfer_eth function with the necessary parameters using the private_key

    return f"Your account balance is {balance} ETH."



