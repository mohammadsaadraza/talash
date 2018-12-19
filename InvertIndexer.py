import regex as re

def invertedIndex(docId, headings, title, hitList, dictionaryForII):

    temp = ""
    tempHead = []
    tempTitle = []
    for head in headings:
        temp = re.sub(r'\W+', '', head)
        if temp.isalnum():
            hitList.append([temp, [""]])
            tempHead.append(temp)
    for head in title:
        temp = re.sub(r'\W+', '', head)
        if temp.isalnum():
            hitList.append([temp, [""]])
            tempTitle.append(temp)


    
    for token in hitList:
        
        if token[0] in dictionaryForII:
            if token[0] in tempHead and token[0] in tempTitle:
                dictionaryForII[token[0]].append([docId, True, True, len(token[1]), token[1]])
                continue
            if token[0] in tempHead:
                dictionaryForII[token[0]].append([docId, False, True, len(token[1]), token[1]])
                continue
            if token[0] in tempTitle:
                dictionaryForII[token[0]].append([docId, True, False, len(token[1]), token[1]])
                continue
            dictionaryForII[token[0]].append([docId, False, False, len(token[1]), token[1]])

        else:
            if token[0] in tempHead and token[0] in tempTitle:
                dictionaryForII[token[0]] = [[docId, True, True, len(token[1]), token[1]]]
                continue
            if token[0] in tempHead:
                dictionaryForII[token[0]] = [[docId, False, True, len(token[1]), token[1]]]
                continue
            if token[0] in tempTitle:
                dictionaryForII[token[0]] = [[docId, True, False, len(token[1]), token[1]]]
                continue
            
            dictionaryForII[token[0]] = [[docId, False, False, len(token[1]), token[1]]]
