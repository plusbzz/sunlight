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
from string import ascii_lowercase
import json
from pprint import PrettyPrinter
   
    
def clean_term(term):
    return term.lower().translate(None,punctuation)
    
def assign_term_ids(doc_frequencies):
    '''
    Assign term ids such that the ids are assigned in sorted order of terms
    '''
    term_count = 1
    for term in sorted(doc_frequencies.keys()):
        doc_frequencies[term]["term_id"] = term_count;
        term_count += 1    
    return doc_frequencies
 
def renormalize_term_ids(doc_frequencies):
    '''
    Assign term ids such that the ids are assigned in sorted order of terms
    '''
    term_count = 1
    for term in sorted(doc_frequencies.keys()):
        df = doc_frequencies[term]["doc_freq"];
        if df == 0:
            del(doc_frequencies[term])
    
    term_count = 1
    for term in sorted(doc_frequencies.keys()):
        doc_frequencies[term]["norm_term_id"] = term_count;
        term_count += 1    
    return doc_frequencies
 
    
def create_doc_freq_dict(fields):
    doc_freq = {}
    chars = [c for c in ascii_lowercase]
    for field in fields:
        f0 = field + ":"
        for c1 in chars:
            for c2 in chars:
                f2 = f0 + str((c1,c2)) 
                doc_freq[f2] = {}  # bigram
                for c3 in chars:
                    f3 = f0 + str((c1,c2,c3))   # trigram
                    doc_freq[f3] = {}
                    
    return assign_term_ids(doc_freq)

def get_tf_dict(record, fields, doc_frequencies):
    """
    For each record, convert the specified field to a list of character
    n-grams (bigrams and trigrams). Each field-and-ngram combination
    becomes a feature in our vector. This, the field 'contributor_name'
    generates ~(26^2+26^3) features.
    """
    doc_id = record['id']
    tf_dict = {}
    for field in fields:
        field_value = clean_term(record[field])
        ng_list = [t for n in xrange(2,4) for t in ngrams(field_value,n)]
        for ng in ng_list:
            term = field + ":" + str(ng)
            if term in doc_frequencies:
                term_id = doc_frequencies[term]['term_id']
                if term_id in tf_dict:
                    tf_dict[term_id] += 1
                else:
                    tf_dict[term_id] = 1

    return (doc_id,tf_dict)

def update_doc_frequencies(doc_frequencies,tf_dict):    
    # Modify document frequencies
    for term in tf_dict.keys():
        if term in doc_frequencies:
            doc_frequencies[term]['doc_freq'] += 1
        else:                                   
            doc_frequencies[term] = {'doc_freq':1}        
    return doc_frequencies


def convert_to_doc_collection(fields,input_file_name,intermediate_file_name="intermediate.txt"):
    '''
    Read a CSV input file and convert each record to a text collection (document)
    of ngrams
    '''
    doc_frequencies = create_doc_freq_dict(fields)
    doc_count = 0
    with open(input_file_name,'rb') as csv_input, open(intermediate_file_name,'wb') as int_output:
        reader = DictReader(csv_input)          # defaults are fine here
        for record in reader:
            doc_id,tf_dict = get_tf_dict(record, fields, doc_frequencies)
            doc_frequencies = update_doc_frequencies(doc_frequencies, tf_dict)
            doc_count += 1
            if doc_count % 1000 == 0:
                print "#records processed: ", doc_count
            # Save tf-dict to intermediate file
            int_output.write(doc_id + ",")
            int_output.write(json.dumps(tf_dict))
            int_output.write("\n")
            
        # renormalize term ids by removing terms with doc_freq = 0
        doc_frequencies = renormalize_term_ids(doc_frequencies)
        # Write ismion header to output file
        # load each record from intermediate file
        # tf-idf normalize it
        # write to ismion output file
    
def tf_idf_normalize(self):
    """
    TF/IDF normalization
    """
    term_list = doc_frequencies.keys()
    
    #for each document
    for doc_id,tf_dict in term_frequencies: # This can get really slow!
        # get each term count
        for term,term_freq in tf_dict.iteritems():
            # multiply tf by idf
            df = doc_frequencies[term]['doc_freq']
            idf = log(doc_count/df)
            tf_dict[term] = term_freq*idf                

        
# Print mapping in a separate file    
def generate_ismion_sparse_file(out_file_name = "ismion_sparse_matrix.txt",
                                     map_file_name = "ismion_term_mapping.txt"):        
    with open(out_file_name,"wb") as csv_output, open(map_file_name,"wb") as map_file:
        csv_writer = writer(csv_output,delimiter=' ')
        row = []
        row.append("header")
        row.append("meta:1")
        row.append("sparse:double:" + str(len(doc_frequencies))) #terms
        csv_writer.writerow(row)
    
        for doc_id,tf_dict in term_frequencies:
            row = []
            new_tf_dict = {}
            term_mapping = {}
            for term,term_freq in tf_dict.iteritems():
                term_id = doc_frequencies[term]['term_id']
                new_tf_dict[term_id] = term_freq
                term_mapping[term_id] = term
            
            row.append(doc_id)
            for term_id in sorted(new_tf_dict.keys()):
                row.append(str(term_id) + ":" + ("%.3f" % new_tf_dict[term_id]))
            csv_writer.writerow(row)
    
        for idx,term in enumerate(sorted_terms):
            map_file.write(str(idx+1) + "," + term + "\n")

if __name__ == "__main__":
    input_file_name = sys.argv[1]
    
    punctuation = ' ,.:;#-@1234567890'
    
    # Which fields to keep? Only the ones that seem pretty clean
    # First/Last names, city/state/zip
    fields = ['contributor_name','contributor_address','contributor_city']
    

    pp = PrettyPrinter()
    convert_to_doc_collection(fields,input_file_name)
    #pp.pprint(ngv.term_frequencies)
