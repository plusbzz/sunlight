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
        self.ngv = NgramVector("sample.csv")


    def tearDown(self):
        pass


    def test_convert_to_ngrams_doc(self):
        record = {
            'contributor_name': "Smith, John",
            'other': 'Test'
        }
        doc = self.ngv.convert_to_ngrams_doc(record, 3, ['contributor_name','other'])
        self.assertEqual(doc,["Smith, John",'Test','smith', 'john','smith_john'])
    
    def test_clean_token_list(self):
        tokens = self.ngv.clean_token_list(["Smith",",","John"])
        self.assertEqual(tokens,['smith', 'john'])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()