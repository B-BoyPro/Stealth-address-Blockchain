import hashlib
import datetime as date

class Block:
    def __init__(self, index, timestamp, data, previous_hash, current_hash=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = current_hash
        if self.hash == None:
            self.hash = self.calculate_hash()

        #data contiene sender address, receive address and amount

    def calculate_hash(self):
        hash_string = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(hash_string.encode()).hexdigest()