tfull = open('time compressed.txt', 'r')
t2 = open('timedata2.txt', 'r')
words = set()
duplicates = 0
numWords = 0
lines = []
for line in tfull:
    numWords += 1
    word = line.split('|')[0]
    if word in words:
        duplicates += 1
    else:
        lines.append(line)
        words.add(word)
print(duplicates, numWords)
newwords = 0
for line in t2:
    if line.split('|')[0] not in words:
        lines.append(line)
        newwords += 1
print(newwords, len(lines))
t2.close()
tfull.close()
tfull = open('time compressed.txt', 'w')
tfull.writelines(lines)
tfull.close()