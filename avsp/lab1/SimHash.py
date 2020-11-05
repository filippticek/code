import hashlib
from sys import stdin

def simHash(text):
    sh = [0] * 128

    for word in text.split(' '):
        hash = hashlib.md5(word.encode('utf-8')).hexdigest()

        hash = bin(int(hash, 16))[2:].zfill(128)
        #print(hash)
        for bit, i in zip(hash, range(128)):
            if int(bit) == 1:
                sh[i] = sh[i] + 1
            else:
                sh[i] = sh[i] - 1

    sh = [1 if shash >= 0 else 0 for shash in sh]
   
    #print(sh)
    return str(hex(binToInt(sh)))[2:]

def binToInt(list):
    return int(''.join(str(e) for e in list), 2)


def hammingDistance(hash1, hash2, minDist):
    hash1 = bin(int(hash1,16))[2:].zfill(128)
    hash2 = bin(int(hash2,16))[2:].zfill(128)

    count = 0

    for bit1, bit2 in zip(hash1, hash2):
        if bit1 != bit2:
            count += 1

        if count > minDist:
            return False

    return True


hashes = []
diff = []    

N = int(stdin.readline().strip())

for i in range(N):
    hashes.append(simHash(stdin.readline().strip()))

Q = int(stdin.readline().strip())

for i in range(Q):
    line = stdin.readline().strip().split(' ')

    I = int(line[0])
    K = int(line[1])

    diffCount = 0

    for j in range(N):

        if j == I:
            pass
        else:
            if hammingDistance(hashes[I], hashes[j], K):
                diffCount += 1 

    print(diffCount)
