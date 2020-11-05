from sys import stdin

numBaskets = int(stdin.readline().strip())

s = float(stdin.readline().strip())

threshold = s * numBaskets

numBuckets = int(stdin.readline().strip())

itemsCount = {}
baskets = []

for _ in range(numBaskets):
    basket = [int(i) for i in stdin.readline().strip().split(' ')]
    baskets.append(basket)
    for item in basket:
        if item in itemsCount:
            itemsCount[item] += 1
        else:
            itemsCount[item] = 1

buckets = [0] * numBuckets
numItems = len(itemsCount)
allPairs = {}

for basket in baskets:
    pairs = []
    for i in range(len(basket)):
        if  itemsCount[basket[i]] >= threshold:
            
            for j in range(i+1, len(basket)):
                if itemsCount[basket[j]] >= threshold:
                    pairs.append((basket[i],basket[j]))


    for (i1, i2) in pairs:
        k = (i1 * numItems + i2) % numBuckets
        buckets[k] += 1

        if (i1, i2) not in allPairs:
            allPairs[(i1,i2)] = 0
        
print(len(allPairs))

numOfPairs = 0

for basket in baskets:
    pairs = []
    for i in range(len(basket)):
        if  itemsCount[basket[i]] >= threshold:
            
            for j in range(i+1, len(basket)):
                if itemsCount[basket[j]] >= threshold:
                    pairs.append((basket[i],basket[j]))

   
    for (i1, i2) in pairs:
        k = (i1 * numItems + i2) % numBuckets

        if buckets[k] >= threshold:
            if allPairs[(i1,i2)] == 1:
                numOfPairs += 1
                
            allPairs[(i1, i2)] += 1

print(numOfPairs)

for w in sorted(allPairs, key=allPairs.get, reverse=True):
    if allPairs[w] != 0:
        print(allPairs[w])