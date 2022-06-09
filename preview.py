file = open('frequency-all.txt', 'r')
# out = open('freq-preview.txt', 'w')

# for i in range(500):
#     line = file.readline()
#     out.write(line)

# out.close()
count = 0
for line in file:
    count += 1
print(count)

file.close()