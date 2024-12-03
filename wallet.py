from Crypto.Hash import SHA256
import binascii
from generate_keys import *
from utils import *
from ecdsa import SECP256k1, SigningKey, VerifyingKey, ellipticcurve
from Crypto.Hash import keccak
from stealth_meta_address import *
from stealth_address import *
from announcement import *
from blockchain import *

# Wallet class generates a wallet for us which contains our public and private keys & manages transaction signing & verification
class Wallet:

    def __init__(self, user):
        self.user = None
        self.private_key = None
        self.public_key = None
        self.ethereum_addr = None
        self.balance = None  

        #Key for stealth address
        self.stealth_meta_address = None
        self.spending_private_key = None
        self.viewing_private_key = None

        self.load_keys(user)

    # Create a new pair of private and public keys
    def load_keys(self,user):
        if user != None:
            self.private_key,self.public_key,self.ethereum_addr,self.balance = retrieve_key_vault(user)
            self.stealth_meta_address, self.spending_private_key, self.viewing_private_key = retrieve_stealth_address(user)
            
            if self.private_key == None and self.public_key == None and self.ethereum_addr == None:
                self.create_keys()
            
            self.user = user
            self.save_keys()
        return


    def create_keys(self):
        private_key, public_key, ethereum_addr = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key
        self.ethereum_addr = ethereum_addr
        self.balance = 100 # Tutti hanno bonus di 100 ether

    
    # Generate a new pair of private and public key
    def generate_keys(self):

        private_key = generate_priv_key()
        public_key = generate_public_key(private_key)
        ethereum_address = generate_ethereum_address(public_key)

        return private_key,public_key,ethereum_address

    def save_stealth_data(self):
        save_keys_Stealth(self.user,self.stealth_meta_address, self.spending_private_key, self.viewing_private_key)

    def stealth_address_create(self):
        self.stealth_meta_address, self.spending_private_key, self.viewing_private_key = generate_stealth_meta_address()
        #print(self.stealth_meta_address, self.spending_private_key, self.viewing_private_key)
        self.save_stealth_data()
        return self.stealth_meta_address

    def save_balance(self):
        return save_balance_utils(self.balance,self.user)

    # Saves the keys to 
    def save_keys(self):
        if self.public_key != None and self.private_key != None and self.ethereum_addr != None:
            save_keys_Wallet(self.user,self.private_key,self.public_key,self.ethereum_addr,self.balance)

    def get_balance(self):
        return self.balance

    def keccak256(self,data):
        k = keccak.new(digest_bits=256)
        k.update(data)
        return k.digest()

    def check_stealth_address(self):
        if self.spending_private_key == None or self.viewing_private_key == None:
            print("Non hai le chiavi spending e viewing")
            return
        ann = Announcement()
        ann_delete = []
        for i in range(len(ann.chain)):
            announcement = ann.chain[i]
            
            spending_private_key = SigningKey.from_string(bytes.fromhex(self.spending_private_key),curve = SECP256k1)
            spending_public_key = spending_private_key.get_verifying_key()

            point = point_from_hex(announcement["ephemeral_pubkey"])
            
            view_tag = announcement["view_tag"]
            
            stealth = computeStealthAddress(point,self.viewing_private_key,spending_public_key,view_tag)
            if stealth == False:
                continue

            if announcement["recipient"] == stealth:
                print("Got the correct one: ")
                print(announcement["recipient"],stealth)
                self.balance += announcement["amount"]
                print("Amount: ",announcement["amount"]," è stato aggiunto al balance con successo")
                Bc = Blockchain()
                Bc.add_block(announcement)
                self.save_balance()
                ann_delete.append(announcement)

        # Delete announcement 
        for k in ann_delete:
            ann.chain.remove(k)
        ann.save_announcement()


    # Sign a transaction and return the signature
    def sign_transaction(self,data):
        hash_data = self.keccak256(json.dumps(data).encode())
        #print(hash_data)
        sk = SigningKey.from_string(binascii.unhexlify(self.private_key),curve=SECP256k1)
        signature = sk.sign(hash_data)
        #print("signature: ",signature)
        return binascii.hexlify(signature).decode('ascii')

    # Verify signature of transaction
    def verify_transaction(self,transaction):
        public_key = transaction["sender"]
        vk = VerifyingKey.from_string(binascii.unhexlify(public_key),curve=SECP256k1)

        data = {
            "sender":transaction["sender"],
            "recipient": transaction["recipient"],
            "amount": transaction["amount"]
        }
        hash_data = self.keccak256(json.dumps(data).encode())
        print(hash_data)
        print(binascii.unhexlify(transaction["signature"]))
        return vk.verify(binascii.unhexlify(transaction["signature"]),hash_data)
