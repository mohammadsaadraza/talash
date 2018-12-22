from nltk import PorterStemmer
from tempUrl import goThroughAllFiles
import sqlite3
import operator
import time

def fetchResult(aWord):
    
    cur.execute("SELECT docId, isTitle, isHeading, frequency, Positions FROM InvertedIndex WHERE word=?",(aWord,))
    return cur.fetchall()

def makeDictionary(aList):

    tempDic = dict()

    for tuples in aList:
        tempDic[tuples[0]] = tuples[1:]

    return tempDic

def avgDistance(positionsList1, positionsList2):

    loop = 0

    positionsList1 = list(str(positionsList1).split(","))
    positionsList2 = list(str(positionsList2).split(","))

    if len(positionsList1) >= len(positionsList2): loop = len(positionsList2)
    else : loop = len(positionsList1)

    total = 0

    #print("POSITIONS LIST 1:",positionsList1,"POSITIONS LIST 2:",positionsList2)
    
    for i in range(loop):
        total += abs(int(positionsList1[i]) - int(positionsList2[i]))

    if loop == len(positionsList1) : return total/loop, len(positionsList2)-loop
    if loop == len(positionsList2) : return total/loop, len(positionsList1)-loop
    
    
def checkWordsInSameDoc(dictionaryForWordsInSameDoc, word, fetchedIndexForAword):

    for i in range(len(fetchedIndexForAword)):
        if fetchedIndexForAword[i][0] not in dictionaryForWordsInSameDoc:
            dictionaryForWordsInSameDoc[fetchedIndexForAword[i][0]] = [word]
        else:
            dictionaryForWordsInSameDoc[fetchedIndexForAword[i][0]].append(word)


def removeSingleOccurences(dictionaryForWordsInSameDoc):

    keysToBeRemoved = list()

    for docId in dictionaryForWordsInSameDoc:
        if len(dictionaryForWordsInSameDoc[docId]) == 1: keysToBeRemoved.append(docId)

    for docId in keysToBeRemoved:
        del dictionaryForWordsInSameDoc[docId]

def displayURLS(pageRankDictionary):

    sortedByValue =  sorted(pageRankDictionary, key=pageRankDictionary.get, reverse=True)

    print("\n\n\nCorrosponding urls: \n\n\n")

    for key in sortedByValue:
        print(key, "\t", dictionaryForUrl[key], "\t", pageRankDictionary[key])


def pageRankForMultipleWordQuery(listOfWords):

    print("SEARCHING: ", listOfWords)

    fetchedIndex = dict()
    dictionaryByDocId = dict()
    dictionaryForWordsInSameDoc = dict()
    pageRankDictionary = dict()

    for word in listOfWords:
        fetchedIndex[word] = fetchResult(word)
        #print("TESTING FETCHED INDEX    ", fetchedIndex[word])
        checkWordsInSameDoc(dictionaryForWordsInSameDoc, word, fetchedIndex[word])
        dictionaryByDocId[word] = makeDictionary(fetchedIndex[word])


    #--------------------FOR CALCULATING PAGE RANK BASED ON THE FREQUENCY AND OTHER STUFF--------------------#


    for docId in dictionaryForWordsInSameDoc:
        pageRankDictionary[docId] = 0
        for word in dictionaryForWordsInSameDoc[docId]:
            if dictionaryByDocId[word][docId][0]: pageRankDictionary[docId] += 3000
            if dictionaryByDocId[word][docId][1]: pageRankDictionary[docId] += 2000
            pageRankDictionary[docId] += 20*dictionaryByDocId[word][docId][2]
            
    removeSingleOccurences(dictionaryForWordsInSameDoc)

    #print("Fetched Index:", fetchedIndex)
    #print("Dictionary By Doc id:", dictionaryByDocId)
    #print("Dictionary For Words in same Doc:", dictionaryForWordsInSameDoc)
    #print("Page Rank:", pageRankDictionary)
            
    for docId in dictionaryForWordsInSameDoc:

        #print(dictionaryByDocId[dictionaryForWordsInSameDoc[docId][0]][docId])
        #print(dictionaryForWordsInSameDoc[docId])
        #print(dictionaryByDocId[dictionaryForWordsInSameDoc[docId][1]])

        if(dictionaryByDocId[dictionaryForWordsInSameDoc[docId][0]][docId][3] == "" or dictionaryByDocId[dictionaryForWordsInSameDoc[docId][1]][docId][3] == "") : continue

        difference, extra = avgDistance(dictionaryByDocId[dictionaryForWordsInSameDoc[docId][0]][docId][3], dictionaryByDocId[dictionaryForWordsInSameDoc[docId][1]][docId][3])
        #print("Avg difference between words =",difference)
        #print("10000/difference =",10000/difference) 
        pageRankDictionary[docId] += (10000/difference) + (extra*0.5)

    #print("Final Page Rank: ", pageRankDictionary)
    displayURLS(pageRankDictionary)



dictionaryForUrl = goThroughAllFiles()

PS = PorterStemmer()

db = sqlite3.connect("InvertedIndex.db")
cur = db.cursor()

while True:

    query = input("Enter a 2 word query seperated by space: ")

    start = time.time()
    
    query = query.split(" ")
    query = [PS.stem(query[0]), PS.stem(query[1])]
    pageRankForMultipleWordQuery(query)

    print("\n\nTime taken to answer the query =", time.time()-start)
    

