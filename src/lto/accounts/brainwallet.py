import os
from lto import crypto
from lto.word_list import wordList

def random_seed():
    word_count = len(wordList)
    words = []
    for i in range(5):
        r = crypto.bytes2str(os.urandom(4))
        x = (ord(r[3])) + (ord(r[2]) << 8) + (ord(r[1]) << 16) + (ord(r[0]) << 24)
        w1 = x % word_count
        w2 = ((int(x / word_count) >> 0) + w1) % word_count
        w3 = ((int((int(x / word_count) >> 0) / word_count) >> 0) + w2) % word_count
        words.append(wordList[w1])
        words.append(wordList[w2])
        words.append(wordList[w3])
    return ' '.join(words)
