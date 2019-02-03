#!/usr/bin/env python3

import sys, string

def key_to_col(keystr):
    keypos = 1
    keycol = [0 for i in range(len(keystr))]
    for v in string.ascii_lowercase:
        for k,s in enumerate(keystr):
            if s == v:
                keycol[k] = keypos
                keypos += 1
    keycol = [s[1] for s in sorted((k, i) for i,k in enumerate(keycol))]
    return keycol, keystr

def encrypt(keycol, plain, cipher):
    index = 0
    rows = [[]]
    with open(plain, "r") as p, open(cipher, "w+") as c:
        for line in p:
            for char in line:
                rows[-1].append(char)
                index += 1
                if index == len(keycol):
                    rows.append([])
                    index = 0
        if len(rows[-1]) == 0:
            del rows[-1]
        else:
            for i in range(len(rows[-1]), len(keycol)):
                rows[-1].append(' ')
        print(rows)
        for row in rows:
            for k in keycol:
                c.write(row[k])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage ./transbreak.py encrypt <key> /path/to/plaintext /path/to/ciphertext")
        print("usage ./transbreak.py decrypt <key> /path/to/plaintext /path/to/ciphertext")
        print("usage ./transbreak.py break /path/to/ciphertext")
    if sys.argv[1] == "encrypt":
        keycol, key = key_to_col(sys.argv[2])
        print("using key:", keycol)
        encrypt(keycol, sys.argv[3], sys.argv[4])
    if sys.argv[1] == "decrypt":
        key_to_col(sys.argv[2])
