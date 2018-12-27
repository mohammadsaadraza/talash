from SingleWordQuery import pageRankForSingleWordQuery
from MultipleWordQuery import pageRankForMultipleWordQuery
from storeURLs import goThroughAllFiles
from nltk.corpus import stopwords
from nltk import PorterStemmer
import tkinter
import regex 
import webbrowser
import sqlite3
import operator
import time

#-------------------This function returns true if a query has only one word, and false other wise-------------------#

def isSingleWordQuery(query):
    if len(query) == 1 : return True
    return False

#-------------------This function returns true if a query has more than one word and false other wise-------------------#

def isMultipleWordsQuery(query):
    if len(query) > 1: return True
    return False

#-------------------This function takes a dictionary containing ranks of documents and displays the urls corrosponding to that doc id as hyperlinks--------------#

def returnUrls(rankedDictionary):
    sortedByValue =  sorted(rankedDictionary, key=rankedDictionary.get, reverse=True)
    items = 0

    root = tkinter.Tk()  
    for key in sortedByValue:
        if "User_talk~" in dictionaryForUrl[key] or "Category~" in dictionaryForUrl[key] or "Talk~"     in dictionaryForUrl[key] or "User~" in dictionaryForUrl[key] or "Wikipedia~" in dictionaryForUrl[key] or "Image~"    in dictionaryForUrl[key] or "Template~" in dictionaryForUrl[key] : continue
        link = tkinter.Label(root, text=dictionaryForUrl[key], fg="blue", cursor="hand2")
        link.pack()
        link.bind("<Button-1>", callback)
        items += 1
        if items == 20: break



#-------------------This function is for the hyperlink to open the browser on click--------------------------------------#
def callback(event):
    webbrowser.open_new(event.widget.cget("text"))

    
    
#-------------------This is the main GUI window for the search engine----------------------------------------------------#
def createWindow():


    #---------------Button to retrieve data from field and search the words----------------------------------------------#
    
    def callButton():
        a = e1.get()
        a = re.sub(" ", a)
        a = a.replace("\n"," ")
        a = a.split(" ")
        print(a)
        e1.delete(0, 'end')
        searchQuery(a)

    #---------------Function for searching the words in our database and retreiving a ranked list of docs according to our PageRank----------------------------#

    def searchQuery(query):
        start = time.time()

        query = [word for word in query if word not in stopWords]

        for i in range(len(query)):
            query[i] = PS.stem(query[i])

        query = list(filter(None, query))

        print("Your Query:", query)

        try:

            rankedDictionary = dict()

            if isSingleWordQuery(query) : rankedDictionary = pageRankForSingleWordQuery(query, cur, dictionaryForUrl)
            elif isMultipleWordsQuery(query) : rankedDictionary = pageRankForMultipleWordQuery(query, cur, dictionaryForUrl)
            else : print("Please Enter Something Else!")
            
            returnUrls(rankedDictionary)

        except:
            print("No Result Found!")

        print("Time taken to answer the query:", time.time()-start)
        

    #-------------------Main Code-------------------#    
    PS = PorterStemmer()
    stopWords = set(stopwords.words("english"))


    db = sqlite3.connect("InvertedIndex.db") #Connecting to sqlite
    cur = db.cursor()
    
    window = tkinter.Tk() #Creating window
    window.title('TALAASH')
    
    w = tkinter.Canvas(window, height=406, width=650) #Using canvas to draw images
    w.pack()

    background = tkinter.PhotoImage(file = "back.png")
    w.create_image(335, 220, image = background) #Blitting images


    e1 = tkinter.Entry(window, width = 32) #Creating entry field
    e1_window = w.create_window(235, 305, anchor='nw', window=e1)
    
    photo1 = tkinter.PhotoImage(file = 'button.png')
    b1 = tkinter.Button(window, height = 29, width = 129, image = photo1, command = callButton) #Creating search button
    b1_window = w.create_window(265, 350, anchor='nw', window = b1)


    window.mainloop()
    

#-------------------Main file where we create the index of all URLs and call the GUI create function-------------------#


dictionaryForUrl = goThroughAllFiles() #See tempUrl file
re = regex.compile("[^a-zA-z0-9\n]")
createWindow()



