import unittest
import json
from node import Node

class NodeTests(unittest.TestCase):

    def test_addtransaction(self):        
        n = Node(1)
        self.assertEqual(n.add_transaction({"sender":"me", "recipient":"you", "amount":100}), 3)

    def test_mine_1_trn(self):
        n = Node(3)
        n.add_transaction({"sender":"me", "recipient":"you", "amount":100})
        proof = n.proof_of_work()
        block = n.mine(proof)
        self.assertEqual(block['proof'], proof)
        self.assertEqual(len(block['transactions']), 1)
        self.assertEqual(block['transactions'][0]['sender'], 'me')
        self.assertEqual(block['transactions'][0]['amount'], 100)

    def test_mine_2_trn(self):
        n = Node(3)
        n.add_transaction({"sender":"me", "recipient":"you", "amount":100})
        n.add_transaction({"sender":"he", "recipient":"she", "amount":583})
        proof = n.proof_of_work()
        block = n.mine(proof)
        self.assertEqual(block['proof'], proof)
        self.assertEqual(len(block['transactions']), 2)
        self.assertEqual(block['transactions'][0]['sender'], 'me')
        self.assertEqual(block['transactions'][0]['amount'], 100)

        self.assertEqual(block['transactions'][1]['sender'], 'he')
        self.assertEqual(block['transactions'][1]['amount'], 583)
    
if __name__ == '__main__':
    unittest.main()