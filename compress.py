import numpy as np
from numpy import array
from math import log10, floor
tf = open('timedata full.txt', 'r')
compressed = open('time compressed.txt', 'w')

def compress(series):
    maxNum = max(series)
    if maxNum <= 0:
        print(word)
        return False
    zeroes = floor(-log10(maxNum))
    series = (np.round(array(series) * (10**zeroes), 5) * 100000).astype(int)
    deltas = [series[0]] + [series[i] - series[i-1] for i in range(1, len(series))]
    newData = '{};{}'.format(zeroes, ','.join(map(lambda x: hex(x).replace('0x', ''), deltas)))
    return newData


for line in tf:
    word, data = line.split('|')
    series = list(map(float, data.split(',')))
    line = compress(series)
    if line:
        compressed.write('{}|{}\n'.format(word, line))
    # maxNum = max(series)
    # if maxNum <= 0:
    #     print(word)
    #     continue
    # zeroes = floor(-log10(maxNum))
    # series = (np.round(array(series) * (10**zeroes), 5) * 100000).astype(int)
    # newData = '{};{}'.format(zeroes, ','.join(map(lambda x: hex(x)[2:], series)))
    # compressed.write('{}|{}\n'.format(word, newData))

compressed.close()
tf.close()