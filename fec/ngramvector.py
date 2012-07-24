'''
Created on Jul 23, 2012

@author: rajdev
'''
from nltk.tokenize import wordpunct_tokenize
from nltk.util import ngrams
from csv import DictReader
   
class NgramVector(object):
    
    def __init__(self, input_file_name):
        self.punctuation = ',.:;'
        self.selected_fields = [
            'organization_name','contributor_name','contributor_address'
        ]
        self.convert_to_doc_collection(input_file_name)
    
    def clean_token_list(self,tokens):
        '''
        Remove punctuation marks from token list and lowercase them
        '''
        return map(lambda y: y.lower(), filter(lambda x: x not in self.punctuation,tokens))
           
    
    def convert_to_ngrams_doc(self,record, max_n, fieldnames):
        """
        For a single record, return a vector containing n-grams for all n = 1..max_n
        Each n-gram has its components separated by '_'
        This function effectively converts each record to a document, where the words
        of the document are n-grams.
        """
        doc = []
        for field in fieldnames:
            doc.append(record[field])
    
        # For select fields, get n-gram lists from 1 to max_n. 
        for phrase_field in self.selected_fields:
            try:
                tokens = self.clean_token_list(wordpunct_tokenize(record[phrase_field]))
            except KeyError:
                continue
            
            for n in xrange(1,max_n+1):
                doc.extend(["_".join(t) for t in ngrams(tokens,n)])
        
        return doc
    
    def convert_to_doc_collection(self,input_file_name):
        '''
        Read a CSV input file and convert each record to a text collection (document)
        of ngrams
        '''
        self.doc_collection = []

        with open(input_file_name,'rb') as csv_input:
            reader = DictReader(csv_input)          # defaults are fine here
            for record in reader:
                doc = self.convert_to_ngrams_doc(record, 3, reader.fieldnames)
                self.doc_collection.append(doc)
                
    def normalize_doc_collection():
        """
        TF/IDF normalization
        """
        pass