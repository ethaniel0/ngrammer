import scipy.stats as stats
import numpy as np
from numpy import array

class PQ:
    queue = []
    mxsze = 0

    def __init__(self, maxsize):
        self.mxsze = maxsize

    def put(self, item):
        self.queue.append(item)
        self.queue = sorted(self.queue, key=lambda val: val[0])
        if len(self.queue) > self.mxsze:
            self.queue = self.queue[:self.mxsze]

    def qsize(self):
        return len(self.queue)

    def get(self):
        return self.queue.pop()
    
    def __str__(self):
        return '\n'.join([f'{i[0]}: {i[1]}' for i in self.queue])

file = open('time compressed.txt', 'r')

p = PQ(10)

gotback = 0
timeSinceLast = 0
lastind = -1

def uncompress(data: str):
    data = data.split(';')
    power = int(data[0])
    deltas = [int(i, 16) for i in data[1].split(',')]
    first = deltas[0]
    timeseries = [first]
    for i in range(1, len(deltas)):
        timeseries.append(timeseries[i-1] + deltas[i])
    timeseries = (10**(-power)) * array(timeseries)/100000
    return timeseries
    

count = 0
for line in file:
    if line == '':
        continue
    parts = line.split('|')
    if len(parts) == 3:
        ngram = '|'
        data = line[2]
    else:
        ngram, data = line.replace('\n', '').split('|')
    if ngram.lower() == 'rick astley':
        print('cheese')

file.close()

# print('------------------------------------------------------')
# print(p)