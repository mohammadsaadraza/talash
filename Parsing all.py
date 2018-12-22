from Parser import parser, pageTitleHead, urlIndex
from FilterAndTokenize import filterDoc
from ForwardIndexer import forwardIndexer
from nltk import PorterStemmer
from fire import pushInFirebase, pushInFirebaseHead, pushInFirebaseUrl
import json
import sqlite3
from InvertIndexer import invertedIndex
import sys
import os

def porterStemmer(headingsList, title):

    headings = []
    titles = []

    PS = PorterStemmer()

    for term in headingsList:
        headings.append(PS.stem(term))

    for term in title.split():
        titles.append(PS.stem(term))

    return headings, titles
    
def goThroughAllFiles():

    path = "E:\\Wikipedia-Dataset" #Make sure the files are in this directory

    numOfFiles = 0 #Total 109832 files have to be parsed!! Keep Calm xD

    n = 1

    done = 0 #This is just for testing. 1040 pages will be indexed. To index all, remove this variable from code.
    
    #Recursively goes through every folder
    for root, dirs, files in os.walk(path):

        for name in files:
            
            if name.endswith((".html", "htm")):

                numOfFiles+= 1
                
                pageTitle, headings, text = parser(root + "\\" + name) #See Parser file
                
                textList = filterDoc(text) #See FilterAndTokenize file
                
                if(pageTitle == None): pageTitle = name[:-5]
                else: pageTitle = pageTitle.text

                #-----FORWARD & INVERTED INDEX functions, comment one and uncomment the other to build the index-----------
                #forwardIndexer(numOfFiles, pageTitle, headings, textList, dictionaryForFI) #See ForwardIndexer file

                headings, pageTitle = porterStemmer(headings, pageTitle)                

                invertedIndex(numOfFiles, headings, pageTitle, textList, dictionaryForII)
                
                #-----Heading Storage in Database, used to ease Searcher Component------
                #pageTitleHead(numOfFiles, pageTitle, headings, ditctionaryForHead)

                #-----Linking urls to docIDs------------
                #urlIndex(numOfFiles, root + "\\" + name, ditctionaryForUrl)


                #pageTitleHead(numOfFiles, pageTitle, headings, dictionaryForHead)
                
                #urlIndex(numOfFiles, root + "\\" + name, dictionaryForUrl)

                
                print(numOfFiles)
                #print("Size of dictionary: ", sys.getsizeof(dictionaryForII))
                
                done+=1
                
        
        if(done >= 80000): break

#------Dicts For Corresponding purposes, comment one and uncomment the other as required--------
#dictionaryForFI = dict()
dictionaryForII = dict()
#dictionaryForHead = dict()
#dictionaryForUrl = dict()

#*********Main Parsing Function Call*************
goThroughAllFiles()
#**************************************

#-------Functions to store DICTS in Database-----------
#pushInFirebase(dictionaryForFI)
#pushInFirebase(dictionaryForII)
db = sqlite3.connect("C:\\Users\\HAT\\Desktop\\Parsing\\InvertedIndex.db")
cur = db.cursor()
#cur.execute('''Drop Table InvertedIndex''')
cur.execute('''Create Table InvertedIndex(word string, docId int, isTitle boolean, isHeading boolean, frequency int, Positions string)''')

k = 1

for key in dictionaryForII:
    print(k)
    k+=1

    for aList in dictionaryForII[key]:

        cur.execute('''INSERT INTO InvertedIndex(word, docId, isTitle, isHeading, frequency, Positions) VALUES (?,?,?,?,?,?)''', (key, aList[0], aList[1], aList[2], aList[3], ",".join(str(e) for e in aList[4])))

db.commit()

db.close()
#pushInFirebaseHead(dictionaryForHead)
#pushInFirebaseUrl(dictionaryForUrl)
