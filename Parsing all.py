from Parser import parser
from FilterAndTokenize import filterDoc
from ForwardIndexer import forwardIndexer
from fire import pushInFirebase
from InvertIndexer import invertedIndex
import sys
import os


    

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
                
                #forwardIndexer(numOfFiles, pageTitle, headings, textList, dictionaryForFI) #See ForwardIndexer file

                invertedIndex(numOfFiles, textList, dictionaryForII)
                
                print(numOfFiles)
                print("Size of dictionary: ", sys.getsizeof(dictionaryForII))
                
                done+=1
                
        
        if(done >= 1000): break

#dictionaryForFI = dict()
dictionaryForII = dict()


goThroughAllFiles()

#pushInFirebase(dictionaryForFI)

pushInFirebase(dictionaryForII)
