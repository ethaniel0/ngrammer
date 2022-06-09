import requests
import scipy.stats as stats
import numpy as np
import asyncio
import aiohttp
from time import perf_counter

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

file = open('timedata full.txt', 'r')

p = PQ(10)

gotback = 0
timeSinceLast = 0
lastind = -1

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
    timeseries = [float(i) for i in data.split(',')]
    peak = max(stats.zscore(timeseries))
    n = np.argmax(timeseries)
    if n > 3 and n < len(timeseries) - 4:
        p.put((-peak, ngram))
    
    if count % 1000 == 0:
        print('------------------------------------------------------')
        print(p)
    count += 1

file.close()

print('------------------------------------------------------')
print(p)