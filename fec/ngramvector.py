'''
Created on Jul 23, 2012

@author: rajdev
'''
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

def vectorize(record):
    """
    For a single record, return a vector containing n-grams
    """
    
def get_ngrams(phrase,n):
    """
    Convert a phrase (sequence of words) to a sequence of ngrams.
    """
    # Tokenize the phrase into a list of words
    tokens = word_tokenize(phrase)

    # Get list ngram tuples. For each tuple, join using '_'
    return ["_".join(t) for t in ngrams(tokens,n)]