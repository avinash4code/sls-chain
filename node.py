import hashlib
import json
from time import time

class Node:
    def __init__(self, block_size=1):
        self.chain = []
        self.draft_transactions = []
        self.block_size = block_size

    def add_transaction(self, transaction):
        transactions = self.get_draft_transactions()
        transactions.append({
            'sender': transaction['sender'],
            'recipient': transaction['recipient'],
            'amount': transaction['amount']
        })

        if len(transactions) == self.block_size:
            self.mine(self.proof_of_work())

        if len(self.chain) == 0:
            return 1
        return self.chain[-1]['index'] + 1        

    def mine(self, proof):
        if len(self.chain) == 0:
            previous_hash = 1
        else:
            previous_hash = self.__hash(self.chain[-1])            

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.draft_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }

        self.draft_transactions = []
        self.chain.append(block)        
        return block


    def __get_chain(self):
        # get the chain from persistent storage
        return self.chain

    def __hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            last_block_hash = self.__hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False
            
            last_block = block
            current_index += 1

        return True
    
    def valid_proof(self, last_proof, proof, last_hash):
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def proof_of_work(self):
        last_block = self.chain[-1]
        last_proof = last_block['proof']
        last_hash = self.__hash(last_block)
        
        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1
        
        return proof
   
    def get_draft_transactions(self):
        # get list current unmined transactions from persisitent storage
        return self.draft_transactions

    @property
    def last_block(self):
        return self.__get_chain()[-1]


