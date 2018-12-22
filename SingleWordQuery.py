import operator


#-------------------This function retrieves the index of a word from sqlite database and returns it-------------------#

def fetchResult(aWord, cur):
    
    cur.execute("SELECT docId, isTitle, isHeading, frequency FROM InvertedIndex WHERE word=?",(aWord,))
    return cur.fetchall()

#-------------------This function calculates pageRank for a single word query-------------------#

def pageRankForSingleWordQuery(word, cur, dictionaryForUrl):

    allHitLists = fetchResult(word[0], cur)

    ranks = dict() #Dictionary that will contain doc ids and their respective ranks

    for hitList in allHitLists:

        ranks[hitList[0]] = 0
        if hitList[1] : ranks[hitList[0]] += 5
        if hitList[2] : ranks[hitList[0]] += 2.5
        ranks[hitList[0]] += hitList[3]*0.5

    return ranks






