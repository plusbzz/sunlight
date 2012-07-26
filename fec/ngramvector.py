'''
Created on Jul 23, 2012

@author: rajdev
'''
from __future__ import division

from nltk.tokenize import wordpunct_tokenize
from nltk.util import ngrams
from csv import DictReader
from math import log
import sys
   
class NgramVector(object):
    
    def __init__(self, input_file_name):
        self.punctuation = ',.:;'
        self.fields_to_keep = [
            'organization_name','contributor_name','contributor_address'
        ]
        self.fields_to_ngram = [
            'organization_name','contributor_name','contributor_address'
        ]
        self.doc_collection = []
        self.doc_count = 0
        
        self.doc_frequencies  = {}    # number of docs for each term
        self.term_frequencies = []    # term counts for each document
        self.term_count = 0
        
        self.convert_to_doc_collection(input_file_name)
        self.tf_idf_normalize()
    
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
        doc_id = record['id']
        for field in fieldnames:
            if field in self.fields_to_keep:
                value = record[field]
                if len(value) > 0:
                    doc.append(record[field].lower())
    
        # For select fields, get n-gram lists from 1 to max_n. 
        for phrase_field in self.fields_to_ngram:
            try:
                tokens = self.clean_token_list(wordpunct_tokenize(record[phrase_field]))
            except KeyError:
                continue
            
            for n in xrange(1,max_n+1):
                doc.extend(["_".join(t) for t in ngrams(tokens,n)])
        
        return (doc_id,doc)
    
    def get_term_freq_dict(self,doc):
        tf_dict = {}
        for term in doc[1:]:
            if term in tf_dict:
                tf_dict[term] += 1
            else:
                tf_dict[term] = 1
        return tf_dict
    
    def update_tf_idf_info(self,doc,doc_id):
        '''
        Convert list of terms to a dictionary with counts
        Append this dictionary to term frequency list
        
        For each term, add to set of documents in which it occurs
        '''
        self.term_frequencies.append((doc_id,self.get_term_freq_dict(doc)))
        
        # For each term, update #docs in which it occurs 
        for term in doc:
            if term in self.doc_frequencies:
                self.doc_frequencies[term]['doc_freq'] += 1
            else:                                   # a new term
                self.term_count += 1                # Give this term a unique number
                self.doc_frequencies[term] = {      # and a doc frequency of 1
                    'term_id'   : self.term_count,
                    'doc_freq'  : 1
                }
                
                
    def convert_to_doc_collection(self,input_file_name):
        '''
        Read a CSV input file and convert each record to a text collection (document)
        of ngrams
        '''

        with open(input_file_name,'rb') as csv_input:
            reader = DictReader(csv_input)          # defaults are fine here
            for record in reader:
                doc_id,doc = self.convert_to_ngrams_doc(record, 3, reader.fieldnames)
                self.doc_count += 1
                self.update_tf_idf_info(doc,doc_id)
                self.doc_collection.append(doc)
                
    def tf_idf_normalize(self):
        """
        TF/IDF normalization
        """
        term_list = self.doc_frequencies.keys()
        
        #for each document
        for doc_id,tf_dict in self.term_frequencies:
            # get each term count
            for term,term_freq in tf_dict.iteritems():
                # multiply tf by idf
                df = self.doc_frequencies[term]['doc_freq']
                idf = log(self.doc_count/df)
                tf_dict[term] = term_freq*idf                
    
    def generate_ismion_sparse_file(self,out_file_name=None):
        # TODO print header
        for doc_id,tf_dict in self.term_frequencies:
            new_tf_dict = {}
            for term,term_freq in tf_dict.iteritems():
                new_tf_dict[self.doc_frequencies[term]['term_id']] = term_freq
            
            print doc_id,
            for term in sorted(new_tf_dict.keys()):
                print term, new_tf_dict[term],
            print
    
    
if __name__ == "__main__":
    input_file_name = sys.argv[1]
    ngv = NgramVector(input_file_name)
    
    from pprint import PrettyPrinter
    pp = PrettyPrinter()
    pp.pprint(ngv.term_frequencies)
    ngv.generate_ismion_sparse_file()
