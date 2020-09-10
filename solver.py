import sys
import re

#grab letters and seperate
allLetters = sys.argv[1]
lts = ''.join([x for x in allLetters if x.islower()])
clt = ''.join([x for x in allLetters if x.isupper()])
clt = clt.lower()

#search
words = []
with open("words.txt") as f:
    for line in f: 
        line = line.rstrip()
        if len(line) >= 4:
            if line.find(clt) != -1:
                if not any(c not in (lts + clt) for c in line):
                    words.append(line)




