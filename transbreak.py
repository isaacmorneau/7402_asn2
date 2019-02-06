#!/usr/bin/env python3
import sys, string, itertools, math
from multiprocessing import Pool
"""
author: Isaac Morneau
date: Feb 01, 2019
content:
    encrypt_message - takes in a key and message returning the ciphertext
    decrypt_message - takes in a key and message returning the plaintext
    transbreak - takes in a ciphertext and dictionary and brute forces the key
"""

def encrypt_message(key, message):
    ciphertext = [''] * key
    for col in range(key):
        pointer = col
        while pointer < len(message):
            ciphertext[col] += message[pointer]
            pointer += key
    return ''.join (ciphertext)


def decrypt_message(key, message):
    cols = math.ceil(len(message) / key)
    rows = key
    extra = (cols * rows) - len(message)
    plaintext = [''] * cols
    row = col = 0
    for m in message:
        plaintext[col] += m
        col += 1
        if (col == cols) or (col == cols - 1 and row >= rows - extra):
            col = 0
            row += 1
    return ''.join(plaintext)

def trykey(key):
    #score the key by counting all matching words over 5 characters long
    return sum(1 for word in decrypt_message(key, cipher).split(None, wordcount) if len(word) > 4 and len(word) < maxlen and word in words)

def transbreak(cipherfile, dictfile):
    global cipher
    global words
    global wordcount
    global maxlen

    cipher = open(cipherfile).read()
    words = open(dictfile).read().split()
    maxlen = max(len(word) for word in words)
    print("4 < word length < {}".format(maxlen))
    #if we have a lot of cipher text dont bother checking every word
    if len(cipher) > 1000:
        wordcount = int(len(cipher)/100)
        print("checking {} words per decrypt".format(wordcount))
    else:
        wordcount = -1
    try:
        listing = Pool().imap(trykey, range(1,len(cipher)))
        best = 0
        best_index = -1
        for index, score in enumerate(listing):
            if score > best:
                best = score
                best_index = index
                print("[new best] keylen: {} score: {}".format(index+1, score))
            if index and index % 100 == 0:
                print("{:.01f}% {}/{}".format(index/len(cipher)*100, index, len(cipher)))
    except KeyboardInterrupt:
        pass
    return best_index+1, best


if __name__ == "__main__":
    if len(sys.argv) == 5:
        if sys.argv[1] == "encrypt":
            with open(sys.argv[4], "w+") as o:
                ciphertxt = encrypt_message(int(sys.argv[2]), open(sys.argv[3], "r").read())
                o.write(ciphertxt)
                print(ciphertxt)
        if sys.argv[1] == "decrypt":
            with open(sys.argv[4], "w+") as o:
                plaintxt = decrypt_message(int(sys.argv[2]), open(sys.argv[3], "r").read())
                o.write(plaintxt)
                print(plaintxt)
    elif len(sys.argv) == 4:
        if sys.argv[1] == "break":
            index, best = transbreak(sys.argv[2], sys.argv[3])
            if index == -1:
                print("all cipher lengths equally terrible")
            else:
                print("[best overall] keylen: {} score: {}".format(index, best))
    else:
        print("usage ./transbreak.py encrypt <key> /path/to/input /path/to/output")
        print("usage ./transbreak.py decrypt <key> /path/to/input /path/to/output")
        print("usage ./transbreak.py break /path/to/ciphertext /path/to/dictionary")
        print("    to generate a dictionary the following can be used:")
        print("        aspell dump master | grep -v \"'\" -E '.{5,}' > dict")
        sys.exit(1)
