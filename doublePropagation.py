
import spacy
from spacy.en import English
from spacy.symbols import amod,prep,nsubj,csubj,dobj,iobj,conj,poss,xcomp,attr,pobj
import pruning as p

relationships = ["amod","prep", "nsubj", "csubj", "dobj", "iobj" ,'pobj', "conj","xcomp"]
noun_tags = ['NN','NNS']
adjective_tags = ['JJ','JJR','JJS']


def doublePropagation(text,seed):
    print "Extraction started!"
    #creates lists for aspects and adjectives
    aspects = []
    adjectives = seed
    extracted_aspects = []
    extracted_adjectives = []
    #set iterator to 1
    iterator = 1
    #start thewhile loop
    while iterator == 1:
        #loop through all sentences in text
        for span in text.sents:
            sent = [text[i] for i in range(span.start,span.end)]
            #find if contains unextracted nouns
            for token in sent:
                if token.tag_ in noun_tags and token.lemma_ not in aspects:
                    #use rule 1 to extract
                    asp = ruleOne(sent,adjectives,aspects)
                    #check that asp is not empty
                    if isAString(asp) == False and len(asp) > 2:
                        if asp not in extracted_aspects: 
                            #add to extracted aspects
                            extracted_aspects.append(asp)
                            
                            
                #find if contains unextracted adjectives
                if token.tag_ in adjective_tags and token.lemma_ not in adjectives:
                    #use rule2 to extract
                    adj = ruleTwo(sent,adjectives)
                    if isAString(adj) == False and len(adj) > 2:
                        if adj not in extracted_adjectives:
                            extracted_adjectives.append(adj)
                        
                        
        aspects = aspects + extracted_aspects
        adjectives = adjectives + extracted_adjectives
        extracted_aspects = []
        extracted_adjectives = []
       
        #loop through all the sentences again
        for span in text.sents:
            sent = [text[i] for i in range(span.start,span.end)]
            #for all tokens in a sentence
            for token in sent:
                #if contains a noun not yet extracted
                if token.tag_ in noun_tags and token.lemma_ not in aspects:
                    #use rule 3 to extract nouns using other nouns
                    asp = ruleThree(sent,aspects)
                    if isAString(asp) == False and len(asp)>2:
                        if asp not in extracted_aspects:
                            extracted_aspects.append(asp)

                          

                if token.tag_ in adjective_tags and token.lemma_ not in aspects:
                    adj = ruleFour(sent,adjectives,aspects)
                    if isAString(adj) == False and len(adj)>2:
                        if adj not in extracted_adjectives:
                            extracted_adjectives.append(adj)
                            
        #check if any aspects and adjectives have been extracted
        if len(extracted_aspects) + len(extracted_adjectives) == 0:
            print "All aspects and adjectives found!"
            iterator = 0
            break
                
        aspects = aspects + extracted_aspects
        adjectives = adjectives + extracted_adjectives
        extracted_aspects = []
        extracted_adjectives = []
    
    p.pruneAspects(aspects,text)
    
            
    
                    
            

        


def isAString(s):
    if s and s.strip():
        return False
    return True

#extraction rule 1
def ruleOne(sent,seed,aspects):
    #iterate through tokens in sent
    for token in sent:
        #if token is an adjective, in seed set and it's relationship is in relationships
        if token.tag_ in adjective_tags and token.lemma_ in seed and token.dep_ in relationships:
            #further if token's head is a noun and token's head not in aspects
            if token.head.tag_ in noun_tags and token.head.lemma_ not in aspects:
                #if token head is a proper word
                if token.head.is_oov == False and token.head.is_stop == False:
                    #return token's head
                    return token.head.lemma_
            
        if token.tag_ in adjective_tags and token.lemma_ in seed and token.dep_ in relationships:
            for child in token.head.children:
                if child.tag_ in noun_tags and child.lemma_ not in aspects and child.dep_ in relationships:
                    if child.is_oov == False and child.is_stop == False:
                        return child.lemma_

        if token.head.tag_ in adjective_tags and token.head.lemma_ in seed and token.dep_ in relationships:
            for child in token.children:
                if child.tag_ in noun_tags and child.lemma_ not in aspects and child.dep_ in relationships:
                    if child.is_oov == False and child.is_stop == False:
                        return child.lemma_

                    
def ruleTwo(sent,adjectives):
    for token in sent:
        if token.tag_ in adjective_tags and token.lemma_ in adjectives and token.dep_ == 'conj':
            if token.head.tag_ in adjective_tags and token.head.lemma_ not in adjectives:
                if token.head.is_stop == False and token.head.is_oov == False:
                    return token.head.lemma_
        if token.tag_ in adjective_tags and token.lemma_ not in adjectives and token.dep_ == 'conj':
                if token.head.tag_ in adjective_tags and token.head.lemma_ in adjectives:
                    if token.is_stop == False and token.is_oov == False:
                        return token.lemma_
                
        if token.tag_ in adjective_tags and token.lemma_ in adjectives and token.dep_ == 'amod':
            for child in token.head.children:
                if child.tag_ in adjective_tags and child.dep_ == 'amod' and child.lemma_ not in adjectives:
                    if child.is_stop == False and child.is_oov == False:
                        return child.lemma_
                    
def ruleThree(sent,aspects):
    #list of equivalent dependencies
    equivalent = {'nsubj','csubj','dobj','obj'}
    for token in sent:
                
        if token.tag_ in noun_tags and token.lemma_ not in aspects and token.dep_ == 'conj':
            if token.head.tag_ in noun_tags and token.head.lemma_ in aspects:
                if token.is_stop == False and token.is_oov == False:
                     return token.lemma_

        if token.tag_ in noun_tags and token.lemma_ in aspects and token.dep_ in equivalent:
            for child in token.head.children:
                if child.tag_ in noun_tags and child.dep_ in equivalent and child.lemma_ not in aspects:
                    if child.is_stop == False and child.is_oov == False:
                        return child.lemma_
                    
        
def ruleFour(sent,adjectives,aspects):

   
    for token in sent:
        if token.tag_ in adjective_tags and token.lemma_ not in adjectives and token.dep_ in relationships:
            if token.head.tag_ in noun_tags and token.head.lemma_ in aspects:
                if token.is_stop == False and token.is_oov == False:
                    return token.lemma_
        
                
    for token in sent:
        if token.tag_ in adjective_tags and token.lemma_ not in adjectives:
            if token.dep_ in relationships:
                for child in token.head.children:
                    if child.tag_ in noun_tags and child.lemma_  in aspects and child.dep_ in relationships:
                        if token.is_stop == False and token.is_oov == False:
                            return token.lemma_

    for token in sent:
        if token.head.tag_ in adjective_tags and token.head.lemma_ not in adjectives:
            if token.dep_ in relationships:
                for child in token.children:
                    if child.tag_ in noun_tags and child.lemma_ in aspects and child.dep_ in relationships:
                        if token.head.is_stop == False and token.head.is_oov == False:
                            return token.head.lemma_
    
    
    
    
        
    
 
    




        
    
