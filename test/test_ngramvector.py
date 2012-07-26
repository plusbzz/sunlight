'''
Created on Jul 23, 2012

@author: rajdev
'''
import unittest
import sys
from pprint import PrettyPrinter

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
            'id':1,
            'contributor_name': "Smith, John",
            'organization_name': 'Test Org'
        }
        doc_id,doc = self.ngv.convert_to_ngrams_doc(record, 3, ['contributor_name','organization_name'])
        self.assertEqual(doc,["smith, john",'test org','test','org','test_org','smith', 'john','smith_john'])
    
    def test_clean_token_list(self):
        tokens = self.ngv.clean_token_list(["Smith",",","John"])
        self.assertEqual(tokens,['smith', 'john'])

    def test_tf_idf(self):
        pp = PrettyPrinter()
        pp.pprint(self.ngv.term_frequencies)
        
if __name__ == "__main__":
    unittest.main()