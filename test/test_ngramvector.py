'''
Created on Jul 23, 2012

@author: rajdev
'''
import unittest
import sys

sys.path.append("../")

import fec
from fec.ngramvector import *

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_vectorize(self):
        pass
    
    def test_get_ngrams_name(self):
        phrase = "John Smith"
        
        result = get_ngrams(phrase,1)       
        self.assertEqual(result,["John","Smith"])

        result = get_ngrams(phrase,2)        
        self.assertEqual(result,["John_Smith"])

        result = get_ngrams(phrase,3)        
        self.assertEqual(result,[])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()