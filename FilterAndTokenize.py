from nltk import PorterStemmer
from nltk.corpus import stopwords
import regex

#This function removes unnecessary content from the start and end of the page by finding the common text in all files.

def removeUnnecessaryContent(doc):

    startIndex = doc.find("From the Simple English Wikipedia, the free encyclopedia that anyone can change")
    endIndex = doc.rfind("Views")

    if(startIndex == -1 or endIndex == -1): return doc

    return doc[startIndex+79 : endIndex]


#This function converts all characters in lower case and replaces non alphanumeric characters with space so that they may be splitted later.

def filterDoc(parsedDoc):

    parsedDoc = removeUnnecessaryContent(parsedDoc);

    if(parsedDoc == ""): return ""
    
    parsedDoc = parsedDoc.lower()

    re = regex.compile("[^a-zA-Z\n]")

    filteredDoc = re.sub(" ", parsedDoc)

    filteredDoc = filteredDoc.replace("\n", " ")

    return tokenize(filteredDoc)


#This function makes the list of words by splitting the string using space as delimiter.

def tokenize(filteredDoc):

    tokenizedList = filteredDoc.split(" ")

    tokenizedList = list(filter(None, tokenizedList))

    return removeStopWords(tokenizedList)


#This function removes stop words from the tokenized list of words.

def removeStopWords(docList):

    stopWords = set(stopwords.words("english"))

    return applyPS([i for i in docList if i not in stopWords])


#This function stems the words. For example, washed, washing, wash, etc will all be converted to wash.


def applyPS(tokens):

    finalList = []

    PS = PorterStemmer()

    for term in tokens:
        finalList.append(PS.stem(term))

    return getPos(finalList)

def getPos(aList):

    tempList = []
    
    for word in aList:
        if presence(word, tempList): continue
        tempList.append([word , [i for i, w in enumerate(aList) if w == word]])
                        
    return tempList

def presence(aWord, tempList):
        for subList in tempList:
            if aWord == subList[0] : return True
        return False



