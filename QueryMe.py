from SingleWordQuery import pageRankForSingleWordQuery
from MultipleWordQuery import pageRankForMultipleWordQuery
from tempUrl import goThroughAllFiles
from nltk.corpus import stopwords
from nltk import PorterStemmer
import sqlite3
import operator
import time

#-------------------This function returns true if a query has only one word, and false other wise-------------------#

def isSingleWordQuery(query):
    if len(query) == 1 : return True
    return False

#-------------------This function returns true if a query has more than one word and false other wise-------------------#

def isMultipleWordsQuery(query):
    if len(query) > 1: return True
    return False

#-------------------This function takes a dictionary containing ranks of documents and displays the urls corrosponding to that doc id-------------------#

def displayUrls(rankedDictionary):

    sortedByValue =  sorted(rankedDictionary, key=rankedDictionary.get, reverse=True)
    items = 0

    print("\n\n\nCorrosponding urls: \n\n\n")

    for key in sortedByValue:
        if "User_talk~" in dictionaryForUrl[key] or "Category~" in dictionaryForUrl[key] or "Wikipedia~" in dictionaryForUrl[key] or "Image~" in dictionaryForUrl[key] : continue
        print(key, "\t", dictionaryForUrl[key], "\t")
        items += 1
        if items == 20: break


#-------------------Main Code-------------------#


PS = PorterStemmer()
stopWords = set(stopwords.words("english"))

dictionaryForUrl = goThroughAllFiles() #See tempUrl file

db = sqlite3.connect("InvertedIndex.db") #Connecting to sqlite
cur = db.cursor()

while True:

    query = input("Enter a query: ").split(" ")

    start = time.time()

    query = [word for word in query if word not in stopWords]

    for i in range(len(query)):
        query[i] = PS.stem(query[i])

    print("Your Query:", query)

    rankedDictionary = dict()

    if isSingleWordQuery(query) : rankedDictionary = pageRankForSingleWordQuery(query, cur, dictionaryForUrl)
    elif isMultipleWordsQuery(query) : rankedDictionary = pageRankForMultipleWordQuery(query, cur, dictionaryForUrl)
    else : print("You didn't enter anything!")
    
    displayUrls(rankedDictionary)

    print("Time taken to answer the query:", time.time()-start)




