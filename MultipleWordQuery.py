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

def avgDistance(dictionaryByDocId, dictionaryForWordsInSameDoc, docId, numOfWords):

    totalDifference = 0
    sameLengths = 0
    extras = 0

    #print("Number of Words in query: ", numOfWords)

    for a in range(numOfWords):

        positionsList1 = list(str(dictionaryByDocId[dictionaryForWordsInSameDoc[docId][a]][docId][3]).split(","))

        totalForAWord = 0

        for b in range(a+1, numOfWords):

            positionsList2 = list(str(dictionaryByDocId[dictionaryForWordsInSameDoc[docId][b]][docId][3]).split(","))

            tempLength1 = len(positionsList1)
            tempLength2 = len(positionsList2)

            #print("Positions LIST 1 length: ", tempLength1)
            #print("Positions LIST 2 length: ", tempLength2)

            loop = 0

            if tempLength1 >= tempLength2: loop = tempLength2
            else : loop = tempLength1

            #print("Loop =", loop)
            #print("SameLengths =", sameLengths)

            sameLengths = sameLengths+loop

            #print("After adding SameLengths =", sameLengths)
            #print("After adding loop =", loop)

            
            totalForTwoWords = 0

            #print("POSITIONS LIST 1:",positionsList1,"POSITIONS LIST 2:",positionsList2)
            
            for i in range(loop):
                totalForTwoWords += abs(int(positionsList1[i]) - int(positionsList2[i]))

            if loop == tempLength1 : extras += tempLength2-loop
            elif loop == tempLength2 : extras += tempLength1-loop

            if loop != 0 : totalForAWord += totalForTwoWords/loop

        totalDifference += totalForAWord

    return totalDifference/sameLengths, extras

    #if loop == len(positionsList1) : return total/loop, len(positionsList2)-loop
    #if loop == len(positionsList2) : return total/loop, len(positionsList1)-loop
                
                 
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
    items = 0

    print("\n\n\nCorrosponding urls: \n\n\n")

    for key in sortedByValue:
        print(key, "\t", dictionaryForUrl[key], "\t", pageRankDictionary[key])
        items += 1
        if items == 20: break


def isHeadingOrTitle(dictionaryByDocId, dictionaryForWordsInSameDoc, docId,  numOfWords):

    for i in range(numOfWords):
        if dictionaryByDocId[dictionaryForWordsInSameDoc[docId][i]][docId][3] == "": return True
    
    return False

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
            if dictionaryByDocId[word][docId][0]: pageRankDictionary[docId] += 10000
            if dictionaryByDocId[word][docId][1]: pageRankDictionary[docId] += 5000
            pageRankDictionary[docId] += 50*dictionaryByDocId[word][docId][2]
            
    removeSingleOccurences(dictionaryForWordsInSameDoc)

    #print("Fetched Index:", fetchedIndex)
    #print("Dictionary By Doc id:", dictionaryByDocId)
    #print("Dictionary For Words in same Doc:", dictionaryForWordsInSameDoc)
    #print("Page Rank:", pageRankDictionary)
            
    for docId in dictionaryForWordsInSameDoc:

        lengthOfList = len(dictionaryForWordsInSameDoc[docId])

        #print(dictionaryByDocId[dictionaryForWordsInSameDoc[docId][0]][docId])
        #print(dictionaryForWordsInSameDoc[docId])
        #print(dictionaryByDocId[dictionaryForWordsInSameDoc[docId][1]])

        if isHeadingOrTitle(dictionaryByDocId, dictionaryForWordsInSameDoc, docId, lengthOfList) : continue

        difference, extra = avgDistance(dictionaryByDocId, dictionaryForWordsInSameDoc, docId, lengthOfList)
        #difference, extra = avgDistance(dictionaryByDocId[dictionaryForWordsInSameDoc[docId][0]][docId][3], dictionaryByDocId[dictionaryForWordsInSameDoc[docId][1]][docId][3])
        #print("Avg difference between words =",difference)
        #print("10000/difference =",10000/difference) 
        pageRankDictionary[docId] += (5000/difference) + (extra*0.5)

    #print("Final Page Rank: ", pageRankDictionary)
    displayURLS(pageRankDictionary)



dictionaryForUrl = goThroughAllFiles()

PS = PorterStemmer()

db = sqlite3.connect("InvertedIndex.db")
cur = db.cursor()

while True:

    query = input("Enter a multi word query seperated by space: ")

    start = time.time()
    
    query = query.split(" ")

    stemmedQuery = list()

    for token in query:
        stemmedQuery.append(PS.stem(token))
        
    pageRankForMultipleWordQuery(stemmedQuery)

    print("\n\nTime taken to answer the query =", time.time()-start)
    

