import spacy
from collections import Counter
import test_functions as test

def pruneAspects(caspects,text):
    print "Starting the aspect pruning"
    caspects = removeSingleCount(caspects,text)
    test.accuracyTest(caspects)
    
        

def removeSingleCount(aspects,text):
    tokens_in_text = [token.lemma_ for token in text]
    for i in aspects:
        count = tokens_in_text.count(i)
        if count < 2:
            aspects.remove(i)
    return aspects
            
        
    
    
        
                                
