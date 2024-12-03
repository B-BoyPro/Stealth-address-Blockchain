#!/usr/bin/env python3

#from secp256k1 import PrivateKey, PublicKey
#from ecdsa import SigningKey, SECP256k1
#import sha3 #For kekkak hashing


from secrets import token_bytes
from coincurve import PublicKey
from sha3 import keccak_256


def generate_ethereum_address(public_key_hex):

	public_key_bytes = bytes.fromhex(public_key_hex)
	ethereum_address = keccak_256(public_key_bytes).digest()[-20:]

	return "0x"+ethereum_address.hex()

#priv_key
def generate_priv_key():
	
	private_key = keccak_256(token_bytes(32)).digest()
	return private_key.hex()

#Derive public Key
def generate_public_key(priv_key):

	private_key_bytes = bytes.fromhex(priv_key)
	public_key = PublicKey.from_valid_secret(private_key_bytes).format(compressed=False)[1:]
	return public_key.hex()

