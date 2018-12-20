import sqlite3
from tempUrl import goThroughAllFiles
from nltk import PorterStemmer
import operator
import time

def fetchResult(aWord):
    
    cur.execute("SELECT * FROM InvertedIndex WHERE word=?",(aWord,))
    return cur.fetchall()

def pageRankForSingleWordQuery(allHitLists):

    tempDict = dict()

    print("Fetched:", allHitLists)

    for hitList in allHitLists:

        tempDict[hitList[1]] = 0
        if hitList[2] : tempDict[hitList[1]] += 5
        if hitList[3] : tempDict[hitList[1]] += 2.5
        tempDict[hitList[1]] += hitList[4]*0.5

    print("Calculated Page Rank:", tempDict)

    sortedByValue =  sorted(tempDict, key=tempDict.get, reverse=True)

    print("\n\n\nCorrosponding urls: \n\n\n")

    for key in sortedByValue:
        print(key, "\t", dictionaryForUrl[key])


dictionaryForUrl = goThroughAllFiles()

PS = PorterStemmer()

db = sqlite3.connect("InvertedIndex.db")
cur = db.cursor()

while True:
    
    token = input("Enter a word: ")
    start = time.time()

    queryWord = PS.stem(token)

    pageRankForSingleWordQuery(fetchResult(queryWord))

    print("Time taken to answer the query:", time.time()-start)




