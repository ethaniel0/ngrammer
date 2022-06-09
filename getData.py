import requests
from math import floor, log10
import numpy as np
from numpy import array

def compress(series):
    maxNum = max(series)
    if maxNum <= 0:
        return False
    zeroes = floor(-log10(maxNum))
    series = (np.round(array(series) * (10**zeroes), 5) * 100000).astype(int)
    deltas = [series[0]] + [series[i] - series[i-1] for i in range(1, len(series))]
    newData = '{};{}'.format(zeroes, ','.join(map(lambda x: hex(x).replace('0x', ''), deltas)))
    return newData


params = {
    "content": ",".join(['Rick Astley']),
    "year_start": "1800",
    "year_end": "2019"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}

undone = True
count = 0

resp = requests.request("GET", "https://books.google.com/ngrams/json", params=params, headers=headers, timeout=30)
j: list = resp.json()
for i in j:
    ngram = i['ngram']
    timeseries = compress(i['timeseries'])
    print(timeseries)