from block import *
import json
from utils import *

class Blockchain:
    def __init__(self):
        self.chain = None        
        self.load_blockchain()

    def load_blockchain(self):
        if self.chain == None:
            prova = blockchain_json_load()
            if prova == None:
                self.chain = [self.create_genesis_block()]
                return

            self.chain = []
            for block in prova:
                self.chain.append(Block(block["index"],block["timestamp"],block["data"],block["previous_hash"],block["hash"]))
            

    def create_genesis_block(self):
        return Block(0, date.datetime.now(), "Genesis Block", "0"*64)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_hash = self.get_latest_block().hash
        new_block = Block(len(self.chain),date.datetime.now(),data,previous_hash)
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
        blockchain_json_save(self)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True
    def to_string(self):
        x = []
        for i in self.chain:
            x.append(
                {
                "index": i.index,
                "timestamp": i.timestamp,
                "data": i.data,
                "previous_hash": i.previous_hash,
                "hash": i.hash
                }
            )
        x = json.dumps(x,indent=4, sort_keys=True, default=str)
        return x


        
# g = Blockchain()
# print(g.chain[0].hash)
# g.add_block("Ciao come va ti voglio bene")
# print((g.to_string()))
# blockchain_json_save(g)
# prova = blockchain_json_load()

# print(prova)