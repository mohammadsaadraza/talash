import time
import os

#This function is used by other files! xD

def goThroughAllFiles():

    start = time.time()

    dictionaryForUrl = dict()

    path = "E:\\Wikipedia-Dataset" #Make sure the files are in this directory

    numOfFiles = 0 #Total 109832 files have to be parsed!! Keep Calm xD

    n = 1

    done = 0 #This is just for testing. 1040 pages will be indexed. To index all, remove this variable from code.
    
    #Recursively goes through every folder
    for root, dirs, files in os.walk(path):

        for name in files:
            
            if name.endswith((".html", "htm")):

                numOfFiles+= 1

                #-----Linking urls to docIDs------------
                dictionaryForUrl[numOfFiles] =  root + "\\" + name
                
                done+=1
                
        
        if(done >= 80000): break

    print("Time taken to store urls: ", (time.time()-start))
    return dictionaryForUrl

    

