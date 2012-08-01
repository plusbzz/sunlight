'''
Created on Jul 23, 2012

@author: rajdev
'''
from __future__ import division

from nltk.tokenize import wordpunct_tokenize
from nltk.util import ngrams
from csv import DictReader,writer
from math import log
import sys
   
class NgramVector(object):
    
    def __init__(self, input_file_name):
        self.punctuation = ' ,.:;#-@1234567890'
        
        # Which fields to keep? Only the ones that seem pretty clean
        # First/Last names, city/state/zip
        self.fields = [
            'contributor_name','contributor_address','contributor_city'
        ]
        
        self.doc_count = 0
        
        self.doc_frequencies  = {}    # number of docs for each term
        self.term_frequencies = []    # term counts for each document
        self.sorted_terms = []
        
        self.convert_to_doc_collection(input_file_name)
        self.tf_idf_normalize()
    
    def clean_term(self,term):
        return term.lower().translate(None,self.punctuation)
        
    
    def convert_to_ngrams_doc(self,record, max_n):
        """
        For each record, convert the specified field to a list of character
        n-grams (bigrams and trigrams). Each field-and-ngram combination
        becomes a feature in our vector. This, the field 'contributor_name'
        generates ~(26^2+26^3) features.
        """
        doc_id = record['id']
        tf_dict = {}
        for field in self.fields:
            field_value = self.clean_term(record[field])
            ng_list = [t for n in xrange(2,4) for t in ngrams(field_value,n)]
            for ng in ng_list:
                field_name = field + ":" + str(ng)
                if field_name in tf_dict:
                    tf_dict[field_name] += 1
                else:
                    tf_dict[field_name] = 1

        self.term_frequencies.append((doc_id,tf_dict))
        
        # Modify document frequencies
        for term in tf_dict.keys():
            if term in self.doc_frequencies:
                self.doc_frequencies[term]['doc_freq'] += 1
            else:                                   
                self.doc_frequencies[term] = {      # and a doc frequency of 1
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
                self.convert_to_ngrams_doc(record, 3)
                self.doc_count += 1
        
        # Assign term ids such that the ids are assigned in sorted order of terms    
        term_count = 1
        for term in sorted(self.doc_frequencies.keys()):
            self.doc_frequencies[term]["term_id"] = term_count;
            term_count += 1
            self.sorted_terms.append(term)
                
    def tf_idf_normalize(self):
        """
        TF/IDF normalization
        """
        term_list = self.doc_frequencies.keys()
        
        #for each document
        for doc_id,tf_dict in self.term_frequencies: # This can get really slow!
            # get each term count
            for term,term_freq in tf_dict.iteritems():
                # multiply tf by idf
                df = self.doc_frequencies[term]['doc_freq']
                idf = log(self.doc_count/df)
                tf_dict[term] = term_freq*idf                
    
            
    # Print mapping in a separate file    
    def generate_ismion_sparse_file(self,out_file_name = "ismion_sparse_matrix.txt",
                                         map_file_name = "ismion_term_mapping.txt"):        
        with open(out_file_name,"wb") as csv_output, open(map_file_name,"wb") as map_file:
            csv_writer = writer(csv_output,delimiter=' ')
            row = []
            row.append("header")
            row.append("meta:1")
            row.append("sparse:double:" + str(len(self.doc_frequencies))) #terms
            csv_writer.writerow(row)
        
            for doc_id,tf_dict in self.term_frequencies:
                row = []
                new_tf_dict = {}
                term_mapping = {}
                for term,term_freq in tf_dict.iteritems():
                    term_id = self.doc_frequencies[term]['term_id']
                    new_tf_dict[term_id] = term_freq
                    term_mapping[term_id] = term
                
                row.append(doc_id)
                for term_id in sorted(new_tf_dict.keys()):
                    row.append(str(term_id) + ":" + ("%.3f" % new_tf_dict[term_id]))
                csv_writer.writerow(row)
        
            for idx,term in enumerate(self.sorted_terms):
                map_file.write(str(idx+1) + "," + term + "\n")
    
if __name__ == "__main__":
    input_file_name = sys.argv[1]
    ngv = NgramVector(input_file_name)
    
    from pprint import PrettyPrinter
    pp = PrettyPrinter()
    #pp.pprint(ngv.term_frequencies)
    ngv.generate_ismion_sparse_file()
    #pp.pprint(ngv.doc_frequencies)
    #print len(ngv.doc_frequencies)