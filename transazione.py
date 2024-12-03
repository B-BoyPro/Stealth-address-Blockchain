from Crypto.Hash import keccak
from blockchain import *
from wallet import *
from ecdsa import SECP256k1, SigningKey, VerifyingKey, ellipticcurve
from stealth_meta_address import *
from stealth_address import *
from utils_stealth_address import point_from_hex, point_to_eth_addr
from announcement import *
from add_amount import *

def send_money(sender,recipient,amount,user):
    wallet_user = Wallet(user)
    try: amount = float(amount)
    except ValueError:
        print("Invalid Transaction.")
        return
    if amount > wallet_user.get_balance():
        print("Insufficient Funds.")
        return
    elif sender == recipient or amount <= 0.00:
        print("It's not possible to send to your self")
        return

    data = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount,
    }

    Block_chain = Blockchain()
    signature = wallet_user.sign_transaction(data)

    data["signature"] = signature

    
    if add_wallet_balance(recipient,amount) != False:
        Block_chain.add_block(data)
        wallet_user.balance -= amount
        wallet_user.save_balance()

    print("Transazione creato con successo ")

    
def send_money_with_meta_address(sender,recipient_meta_address,amount,user):
    wallet_user = Wallet(user)

    try: amount = float(amount)
    except ValueError:
        print("Invalid Transaction.")
        return
    if amount > wallet_user.get_balance():
        print("Insufficient Funds.")
        return 
    elif sender == recipient_meta_address or amount <= 0.00:
        print("It's not possible to send to your self")
        return
    
    stealth_address_json = generate_stealth_address(recipient_meta_address)

    data = {
        "sender": sender,
        "recipient": stealth_address_json["stealth_address"],
        "amount": amount,
        "ephemeral_pubkey": stealth_address_json["ephemeral_pubkey"],
        "view_tag": stealth_address_json["view_tag"]
    }

    announ = Announcement()
    signature = wallet_user.sign_transaction(data)

    data["signature"] = signature
    wallet_user.balance -= amount

    wallet_user.save_balance()
    announ.add_announcement(data)
    announ.save_announcement()

    print("Transazione creato con successo ")