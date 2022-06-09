tfull = open('time compressed.txt', 'r')
t2 = open('filtered.txt', 'w')
removes = 0
numWords = 0

for line in tfull:
    parts = line.split('|')
    if len(parts) > 2:
        removes += 1
        continue
    if ' / ' in parts[0] or ' - ' in parts[0] or '(' in parts[0] or ')' in parts[0]:
        removes += 1
        continue
    t2.write(line)
    numWords += 1

    
print(removes, numWords)
t2.close()
tfull.close()

tfull = open('time compressed.txt', 'w')
t2 = open('filtered.txt', 'r')
for line in t2:
    tfull.write(line)
t2.close()
tfull.close()