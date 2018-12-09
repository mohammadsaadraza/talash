from fire import pushInFirebase

def forwardIndexer(docId, docTitle, headings, docList):

    dictDoc = dict()
    
    dictDoc[docId] = [docTitle, headings, docList] #A dictionary ie hash table that stores docids headings and other text.

    pushInFirebase(dictDoc) #This function uploads the data in dictionary to firebase

