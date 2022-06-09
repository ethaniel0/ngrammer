tfull = open('timedata full.txt', 'r')

words = set()
duplicates = 0
numWords = 0

for line in tfull:
    numWords += 1
    word = line.split('|')[0]
    if word in words:
        duplicates += 1
    else:
        words.add(word)

print(duplicates, numWords)

tfull.close()
