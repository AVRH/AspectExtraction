import adjectives as adj

#read the review text file into a string
txt_file = open("iTest.txt","r")
text =txt_file.read()
txt_file.close()


#translate into unicode and send to adj seedSet
adj.seedSet(unicode(text))





 



    
