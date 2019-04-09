import unittest
import json
from node import Node

class NodeTests(unittest.TestCase):

    def test_addtransaction(self):        
        n = Node(1)
        self.assertEqual(n.add_transaction({"sender":"me", "recipient":"you", "amount":100}), 1)
    
if __name__ == '__main__':
    unittest.main()