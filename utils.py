import os
import json
import hashlib
import base64

data_path = "data"


def load_ann():
    name_path = "announcement.json"
    try:
        with open(os.path.join(data_path,name_path),"r") as f:
            announcement = json.loads(f.read().strip())
        return announcement
    except :
        return None

def save_ann(data):
    name_path = "announcement.json"
    try:
        with open(os.path.join(data_path,name_path),"w") as f:
            f.write(data)
        return True
    except:
        return False

def blockchain_json_save(blockchain):
    name_path = "blockchain.json"
    try:
        with open(os.path.join(data_path,name_path),"w") as f:
            f.write(blockchain.to_string())
        return True
    except:
        return False

def blockchain_json_load():
    name_path = "blockchain.json"
    try:
        with open(os.path.join(data_path,name_path),"r") as f:
            blockchain = json.loads(f.read().strip())
        return blockchain
    except :
        return None

def add_new_user(username, password):
    try:
        os.makedirs(os.path.join(data_path, username))

        phash = hashlib.md5(password.encode()).hexdigest()

        with open(os.path.join(data_path, username, "pw_hash"), "x") as f:
            f.write(str(phash))

        return True
    except FileExistsError:
        print("User already registered!")
        return False
    except:
        return False

def login(username, password):
    try:
        if not os.path.isfile(os.path.join(data_path, username, "pw_hash")):
            print("User does not exist")
            return False

        phash = hashlib.md5(password.encode()).hexdigest()

        with open(os.path.join(data_path, username, "pw_hash"), "r") as f:
            loaded_hash = f.read().strip()

        if phash != loaded_hash:
            print("Username or password wrond")
            return False
        return True
    except:
        return False

def save_keys_Stealth(username,stealth_meta_address,spending_private_key,viewing_private_key):
    try:
        with open(os.path.join(data_path, username, "stealth_keys"), "w") as f:
            f.write(str(stealth_meta_address)+"\n")
            f.write(str(spending_private_key)+"\n")
            f.write(str(viewing_private_key))
        return True
    except:
        return False

def retrieve_stealth_address(username):
    try:
        if not os.path.isfile(os.path.join(data_path, username, "stealth_keys")):
            return None, None, None

        with open(os.path.join(data_path, username, "stealth_keys"), "r") as f:
            stealth_meta_address = f.readline().strip()
            spending_private_key = f.readline().strip()
            viewing_private_key = f.readline().strip()

        return stealth_meta_address, spending_private_key, viewing_private_key
    except:
        return None, None, None

def save_keys_Wallet(username,private_key,public_key,ethereum_address,balance):
    try:
        with open(os.path.join(data_path, username, "private_key"), "x") as f:
            f.write(str(private_key))
        with open(os.path.join(data_path, username, "public_key"), "x") as f:
            f.write(str(public_key))

        with open(os.path.join(data_path, username, "ethereum_address"), "x") as f:
            f.write(str(ethereum_address))
        with open(os.path.join(data_path, username, "balance"), "x") as f:
            f.write(str(balance))
        return True
    except FileExistsError:
        return False
    except FileNotFoundError:
        print("File Username not found")
        return False
    except:
        print("Something bad happened")
        return False

def save_balance_utils(balance,username):
    try:
        with open(os.path.join(data_path, username, "balance"), "w") as f:
            f.write(str(balance))
        return True
    except:
        return False


def retrieve_key_vault(username):
    try:
        if not os.path.isfile(os.path.join(data_path, username, "private_key")):
            return None, None, None, None

        if not os.path.isfile(os.path.join(data_path, username, "public_key")):
            return None, None, None, None

        if not os.path.isfile(os.path.join(data_path, username, "ethereum_address")):
            return None, None, None, None

        if not os.path.isfile(os.path.join(data_path, username, "balance")):
            return None, None, None, None

        with open(os.path.join(data_path, username, "private_key"), "r") as f:
            private_key = f.read().strip()

        with open(os.path.join(data_path, username, "public_key"), "r") as f:
            public_key = f.read().strip()

        with open(os.path.join(data_path, username, "ethereum_address"), "r") as f:
            ethereum_address = f.read().strip()

        with open(os.path.join(data_path, username, "balance"), "r") as f:
            balance = float(f.read().strip())

        return private_key,public_key,ethereum_address,balance
    except:
        return None, None, None, None