import os

data_path = "data"
public_key_file = "public_key"
balance_file = "balance"

def add_wallet_balance(public_key,amount):
	try:
		list_wallet = []
		for path in os.listdir("data"):
			if os.path.isdir(os.path.join(data_path, path)):
				list_wallet.append(path)

		for wallet in list_wallet:
			path_public = data_path + "/" + wallet
			with open(os.path.join(path_public,public_key_file),"r") as f:
				public_key_check = f.read()
				if public_key_check == public_key:
					with open(os.path.join(path_public,balance_file),"r+") as fb:
						balance_old = float(fb.read().strip())
						new_balance = amount + balance_old
						fb.seek(0)
						fb.write(str(new_balance)) 
		return True
	except:
		print("Ethereum address or public key not found")
		return False

def add_wallet_balance_stealth_address(public_key,amount):
	try:
		list_wallet = []
		for path in os.listdir("data"):
			if os.path.isdir(os.path.join(data_path, path)):
				list_wallet.append(path)

		for wallet in list_wallet:
			path_public = data_path + "/" + wallet
			with open(os.path.join(path_public,public_key_file),"r") as f:
				public_key_check = f.read()
				if public_key_check == public_key:
					with open(os.path.join(path_public,balance_file),"r+") as fb:
						balance_old = float(fb.read().strip())
						new_balance = amount + balance_old
						fb.seek(0)
						fb.write(str(new_balance)) 
		return True
	except:
		print("Could not add the balance to the wallet")
		return False
