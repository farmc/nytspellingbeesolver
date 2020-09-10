import sys

#read input
errmsg = "Usage: python3 solver.py { 6 lowercase and 1 uppercase letter no spaces }"
if (len(sys.argv) != 2):
    sys.exit(errmsg)

allLetters = sys.argv[1]

lts = ''.join([x for x in allLetters if x.islower()])
if (len(lts) != 6):
    sys.exit(errmsg)

clt = ''.join([x for x in allLetters if x.isupper()])
if (len(clt) != 1):
    sys.exit(errmsg)

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


#print all the words found
words.sort(key=len)
curL = 4
panagrams = []
print('4 Letter Words: ')

for word in words:
    if set(word) >= set(lts):
        panagrams.append(word)

    elif len(word) == curL:
        print(word)
    else:
        curL = len(word)
        print(curL, 'Letter Words: ')
        print(word)

print('PANAGRAMS: ')
for panagram in panagrams:

    print(panagram)
        


