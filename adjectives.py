
import spacy
from spacy.en import English
from collections import Counter
import doublePropagation as parse


#create spacy parser
parser = English()
#list of tags for adjectives
adj_tags = ['JJ','JJR','JJS']

def seedSet(text):
    seed_set = []
    #parse the text
    parsed_text = parser(text)
    #find the list of all adjectives
    adjectives = [token.lemma_ for token in parsed_text if token.is_oov == False and token.is_punct == False and token.is_stop == False and token.tag_ in adj_tags]
    #find three most common adjectives
    adj_freq = Counter(adjectives)
    common_adj = adj_freq.most_common(5)
    #extract just the words from the word,tuple lists
    for i in range(len(common_adj)):
        seed_set.append(str(common_adj[i][0]))
    print "Seed set created"
    #call the double propagation function
    parse.doublePropagation(parsed_text,seed_set)
    

   
    
        
