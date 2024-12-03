import json
from utils import *

class Announcement:
	def __init__(self):
		self.chain = []
		self.load_announcement()
	
	def save_announcement(self):
		save_ann(self.to_string())

	def load_announcement(self):
		if self.chain == []:
			chain = load_ann()
			if chain == None:
				return 

			for c in chain: 
				self.chain.append(c)


	def add_announcement(self, data):
		self.chain.append(data)

	def to_string(self):
		return json.dumps(self.chain,indent=4, sort_keys=True, default=str)


# a = Announcement()

# data = {
#         "sender": "sender",
#         "recipient": "stealth_address_json",
#         "amount": "amount",
#         "ephemeral_pubkey": "stealth_address_json[ephemeral_pubkey]",
#         "view_tag": "stealth_address_json[view_tag]"
#     }
# a.add_announcement(data)
# print(a.chain)
# a.save_announcement()