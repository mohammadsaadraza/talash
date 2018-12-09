from Parser import parser
from FilterAndTokenize import filterDoc
from ForwardIndexer import forwardIndexer
import os

def goThroughAllFiles():

    path = "E:\\Wikipedia-Dataset" #Make sure the files are in this directory

    numOfFiles = 0 #Total 109832 files have to be parsed!! Keep Calm xD

    done = False #This is just for testing. Only one page will be indexed. To index all, remove this variable from this file.
    
    #Recursively goes through every folder
    for root, dirs, files in os.walk(path):

        for name in files:
            
            if name.endswith((".html", "htm")):
                
                numOfFiles+= 1
                
                pageTitle, headings, text = parser(root + "\\" + name) #See Parser file
                
                textList = filterDoc(text) #See FilterAndTokenize file
                
                if(pageTitle == None): pageTitle = name[:-5]
                else: pageTitle = pageTitle.text
                
                forwardIndexer(numOfFiles, pageTitle, headings, textList) #See ForwardIndexer file
                
                print(numOfFiles)
                
                done = True 
                
                break #done variable and break are just to make sure that only one doc is indexed. Later these will be removed.
        
        if(done): break

goThroughAllFiles()
