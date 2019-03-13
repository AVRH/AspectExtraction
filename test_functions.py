

with open('iTestTest.txt','r') as tFile:
    aspects = tFile.read().splitlines()
    

def accuracyTest(candidate):
    right = set()
    wrong = set ()
    missed = set()
    
    for asp in candidate:
        if asp in aspects:
            right.add(asp)
        if asp not in aspects:
            wrong.add(asp)
    for asp in aspects:
        if asp not in right:
            missed.add(asp)
    print "I got it right: "
    print right
    print len(right)
    print "I got it wrong: "
    print wrong
    print len(wrong)
    print "Total amount of real aspects: "
    print len(aspects)
    print "Missed aspects: "
    print missed
    print len(missed)
    
    
