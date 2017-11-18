import sys
from itertools import combinations
import pandas

file_name = sys.argv[1]  # taking file_name in argv array which is passed via command line arguments
min_conf = float(sys.argv[3])  # taking min_conf in argv array which is passed via command line arguments
rules = {}
apriori = {}
freqset = {}


# generate the iterations of apriori
def apriorigenerate(apriori, l, transactions):
    apriori1 = {}
    for cols in combinations(apriori, l):
        count1 = 0
        for j in range(len(transactions)):
            if set(cols).issubset(transactions[j]):
                count1 += 1
            apriori1[cols] = count1
    return apriori1


# generate association rules related to the apriori subsets
def associationrules(freqset, apriori4):
    confidence = 0
    print('Producing rules from the subsets of the dictionary:')
    for key in apriori4:
        loop1 = 1
        while (loop1 <= len(freqset)):
            for cols in combinations(list(key), loop1):
                t = str(cols).split()
                if len(t) <= 1:
                    for char in [',', '\'', '(', ')']:
                        cols = str(cols).replace(char, '')
                if cols in freqset:
                    confidence = freqset[key] / freqset[cols]
                if confidence != 1:
                    if (confidence >= min_conf):
                        key1=str(key).split(",")
                        for x in range(len(key1)):
                            for char in [',', '\'', '(', ')', ' ']:
                                key1[x] = str(key1[x]).replace(char,'')
                        if cols in key1:
                            key1.remove(cols)
                        cols1 = str(cols)+' -> '+str(key1[0])
                        rules[cols1] = confidence
            loop1 += 1

def main():
    min_support = float(sys.argv[2])  # taking min_suppport in argv array which is passed via command line arguments
    
    # read the file and store it in the transactions array
    transactions = []
    with open(file_name) as f:
        for line in f:
            transactions.append(line.split())

    # finding the minimum support of each element in the transactions array
    for i in range(0, len(transactions)):
        for j in range(0, len(transactions[i])):
            if transactions[i][j] not in apriori:
                apriori[transactions[i][j]] = 1
            else:
                apriori[transactions[i][j]] += 1

    # calculating the minimum support and removing the key-value pairs that have support less than minimum support
    min_support *= len(transactions)
    print()
    print('Performing apriori for the dataset with minimum support as ' + str(min_support) + ' and confidence ' + str(
        min_conf))
    for key, val in apriori.copy().items():
        if val < min_support:
            del apriori[key]

    # iteration 1 result
    freqset = apriori
    print("-------- Iteration 1 --------")
    df = pandas.DataFrame([[number, support] for number, support in apriori.items()], columns=['Number', 'Support'])
    print(df)
    if df.empty:
        print('There are no elements with support that meets the requirements')
        sys.exit()
    print()

    # looping the apriori process to produce subsets of length 2,3.. and so on until the iteration array returns empty
    l = 2
    apriori2 = []
    final = []
    final = apriori
    while apriori:
        apriori2 = apriorigenerate(apriori, l, transactions)
        for key, val in apriori2.copy().items():
            if val < min_support:
                del apriori2[key]
        freqset.update(apriori2)
        print('-------- Iteration ' + str(l) + '--------')
        df = pandas.DataFrame([[number, support] for number, support in apriori2.items()], columns=['Number', 'Support'])
        print(df)
        print()

        # if the iteration set is empty then we have generated all possible subsets for the given minimum support
        l = l + 1
        if not apriori2:
            print('Iteration set is empty so we get our final apriori item set from iteration ' + str(l - 2) + '\n')
            break
        else:
            final = apriori2

    print('Generation of association rules from the following dictionary:')
    print(final)
    print()

    # generating rules based on the subsets obtained from apriori
    associationrules(freqset, final)
    df2 = pandas.DataFrame([[item, val] for item, val in rules.items()], columns=['Item', 'Confidence'])
    print(df2)
    if df2.empty:
        print('There are no association rules with confidence: ' + str(min_conf))

if __name__=="__main__":
    main()