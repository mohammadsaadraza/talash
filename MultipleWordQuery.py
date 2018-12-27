import operator

#-------------------This function retrieves the index of a word from sqlite database and returns it-------------------#

def fetchResult(aWord, cur):
    
    cur.execute("SELECT docId, isTitle, isHeading, frequency, Positions FROM InvertedIndex WHERE word=?",(aWord,))
    return cur.fetchall()

#-------------------This function takes the tuples returned from the database and then makes a dictionary in which first element of-------------------#
#-------------------------------the tuple is key and all the others are stored in list that is referred by the key------------------------------------#

def makeDictionary(aList):

    tempDic = dict()

    for tuples in aList:
        tempDic[tuples[0]] = tuples[1:]

    return tempDic

#-------------------This function calculates the distribution of words in a document. Document with less distribution will be prefferred-------------------#

#Distance of every word from every other word is calculated and then the average distance is calculated. Incase of imbalance between the frequencies
#of two words, pageRank will be increased by constant times the amount by which imbalance occurred

def avgDistance(dictionaryByDocId, dictionaryForWordsInSameDoc, docId, numOfWords):

    totalDifference = 0
    sameLengths = 0
    extras = 0

    for a in range(numOfWords):

        positionsList1 = list(str(dictionaryByDocId[dictionaryForWordsInSameDoc[docId][a]][docId][3]).split(","))

        totalForAWord = 0

        for b in range(a+1, numOfWords):

            positionsList2 = list(str(dictionaryByDocId[dictionaryForWordsInSameDoc[docId][b]][docId][3]).split(","))

            tempLength1 = len(positionsList1)
            tempLength2 = len(positionsList2)

            loop = 0
            
            totalForTwoWords = 0

            index1 = 0
            index2 = 0

            while index1 < tempLength1 and index2 < tempLength2:

                a = int(positionsList1[index1])
                b = int(positionsList2[index2])
                
                if not (index2 != tempLength2 - 1 and abs(a - b) >= abs(a - int(positionsList2[index2 + 1]))):
                    totalForTwoWords += abs(a - b)
                    loop += 1
                    sameLengths += 1
                    index1 += 1

                index2 += 1

            extras += (tempLength1-index1) + (tempLength2-index2)

            totalForAWord += totalForTwoWords/loop

        totalDifference += totalForAWord

    return totalDifference/sameLengths, extras


#-------------------This function makes a dictionary that will contain doc ids which will refer to a list containing the words that-------------------#
#-------------------------------------------------------occurred in that particular document----------------------------------------------------------#

          
def checkWordsInSameDoc(dictionaryForWordsInSameDoc, word, fetchedIndexForAword):

    for i in range(len(fetchedIndexForAword)):
        if fetchedIndexForAword[i][0] not in dictionaryForWordsInSameDoc:
            dictionaryForWordsInSameDoc[fetchedIndexForAword[i][0]] = [word]
        else:
            dictionaryForWordsInSameDoc[fetchedIndexForAword[i][0]].append(word)


#-------------------This function removes those documents from the dictionary that contain only word from the query. This is because-------------------#
#-------------------------------pageRank for single occurrences are calculated in the same way as for single word queries------------------------------#


def removeSingleOccurences(dictionaryForWordsInSameDoc):

    keysToBeRemoved = list()

    for docId in dictionaryForWordsInSameDoc:
        if len(dictionaryForWordsInSameDoc[docId]) == 1: keysToBeRemoved.append(docId)

    for docId in keysToBeRemoved:
        del dictionaryForWordsInSameDoc[docId]


#-------------------This function returns true if any of the word appearing in a document is a heading or a tile and false otherwise. -------------------#


def isHeadingOrTitle(dictionaryByDocId, dictionaryForWordsInSameDoc, docId,  numOfWords):

    for i in range(numOfWords):
        if dictionaryByDocId[dictionaryForWordsInSameDoc[docId][i]][docId][3] == "": return True
    
    return False

#-------------------This function calculates pageRank for multiple Word Queries-------------------#

def pageRankForMultipleWordQuery(listOfWords, cur, dictionaryForUrl):

    fetchedIndex = dict()
    dictionaryByDocId = dict()
    dictionaryForWordsInSameDoc = dict()
    pageRankDictionary = dict()

    for word in listOfWords:
        fetchedIndex[word] = fetchResult(word, cur)
        checkWordsInSameDoc(dictionaryForWordsInSameDoc, word, fetchedIndex[word])
        dictionaryByDocId[word] = makeDictionary(fetchedIndex[word])


    #--------------------FOR CALCULATING PAGE RANK BASED ON THE FREQUENCY AND OTHER STUFF--------------------#


    for docId in dictionaryForWordsInSameDoc:
        pageRankDictionary[docId] = 0
        for word in dictionaryForWordsInSameDoc[docId]:
            if dictionaryByDocId[word][docId][0]: pageRankDictionary[docId] += 10
            if dictionaryByDocId[word][docId][1]: pageRankDictionary[docId] += 2.5
            pageRankDictionary[docId] += 0.5*dictionaryByDocId[word][docId][2]
            
    removeSingleOccurences(dictionaryForWordsInSameDoc)
            
    for docId in dictionaryForWordsInSameDoc:

        lengthOfList = len(dictionaryForWordsInSameDoc[docId])

        if isHeadingOrTitle(dictionaryByDocId, dictionaryForWordsInSameDoc, docId, lengthOfList) : continue

        difference, extra = avgDistance(dictionaryByDocId, dictionaryForWordsInSameDoc, docId, lengthOfList)
 
        pageRankDictionary[docId] += (15/difference) + (extra*0.5)

    
    return pageRankDictionary
