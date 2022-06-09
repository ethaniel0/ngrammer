import requests
import scipy.stats as stats
import numpy as np
import asyncio
import aiohttp
from math import floor, log10
import numpy as np
from numpy import array
from time import perf_counter
from random import shuffle

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
       


p = PQ(10)

gotback = 0
timeSinceLast = 0
lastind = -1

file = open('timedata2.txt', 'w')
check = open('time compressed.txt', 'r')
checked = set()
for line in check:
    checked.add(line.split('|')[0])
check.close()

def compress(series):
    maxNum = max(series)
    if maxNum <= 0:
        return False
    zeroes = floor(-log10(maxNum))
    series = (np.round(array(series) * (10**zeroes), 5) * 100000).astype(int)
    deltas = [series[0]] + [series[i] - series[i-1] for i in range(1, len(series))]
    newData = '{};{}'.format(zeroes, ','.join(map(lambda x: hex(x).replace('0x', ''), deltas)))
    return newData

async def requestWords(words):
    global gotback, timeSinceLast, lastind
    params = {
        "content": ",".join(words),
        "year_start": "1800",
        "year_end": "2019"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
    }

    undone = True
    count = 0
    while undone:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://books.google.com/ngrams/json', params=params, headers=headers, timeout=30) as resp:
                try:
                    j: list = await resp.json()
                    for i in j:
                        ngram = i['ngram']
                        timeseries = compress(i['timeseries'])
                        if not timeseries:
                            return
                        file.write(ngram + '|')
                        file.write(timeseries + '\n')
                    gotback += 1
                        
                    if (perf_counter() - timeSinceLast > 1):
                        print(gotback)
                        timeSinceLast = perf_counter()
                    if count > 0:
                        print('eyyy')
                    undone = False
                except aiohttp.ContentTypeError:
                    count += 1
                    if count >= 10:
                        return
                    await asyncio.sleep(10)
            
def filterData(word: str):
    parts = line.split('|')
    if len(parts) > 2:
        return False
    if ' / ' in word or ' - ' in word or '(' in word or ')' in word:
        return False
    return True
async def main():
    file = open('frequency-all.txt', 'r')

    print("Gathering words...")

    first = True
    #loop while file has lines
    chunk = []
    count = 0
    sent = 0
    words = []
    for line in file:
        if first:
            first = False
            print('started')
            continue
        if not filterData(line):
            continue

        #split line into words
        parts = list(filter(lambda x: x != '', line.split(' ')))
        word = parts[1]
        words.append(word)
        if word in checked:
            continue
    
    print('read file')
    shuffle(words)
    print('shuffled')

    for word in words:
        chunk.append(word)
        if len(chunk) == 10:
            loop = asyncio.get_event_loop()
            loop.create_task(requestWords(chunk))
            if (count + 1) % 40 == 0:
                await asyncio.sleep(2)
            sent += 1
            chunk = []
        count += 1

    file.close()

    while sent > gotback:
        print(sent, gotback)
        await asyncio.sleep(5)
    print('sent:', sent, 'gotback:', gotback)
    file.close()
    
    print(p)

asyncio.run(main())