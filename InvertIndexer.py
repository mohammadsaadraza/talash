def invertedIndex(docId, listContainingTextOfDoc, dictionaryForII):

    tempDict = dict()
    
    for token in listContainingTextOfDoc:
    
        if token in dictionaryForII:
            if dictionaryForII[token][-1][0] == docId: 
                dictionaryForII[token][-1][1]+= 1
            else:
                dictionaryForII[token].append([docId, 1])
        else:
            dictionaryForII[token] = [[docId, 1]]
