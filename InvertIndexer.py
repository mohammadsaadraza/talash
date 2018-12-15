def invertedIndex(docId, hitList, dictionaryForII):
    
    for token in hitList:
        
        if token[0] in dictionaryForII:
            dictionaryForII[token[0]].append({docId : token[1]})
        else:
            dictionaryForII[token[0]] = [{docId : token[1]}]
