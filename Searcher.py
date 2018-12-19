import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from nltk import PorterStemmer
from nltk.corpus import stopwords

def initialize():
    cred = credentials.Certificate('./talash-70578-firebase-adminsdk-jz0oc-e545575ec0.json')
    default_app = firebase_admin.initialize_app(cred,{'databaseURL': 'https://talash-70578.firebaseio.com/'})

def search(token):
    root=db.reference()
    ref=root.child('InvertedIndex').child(token)

    if (ref.get() != None):
        print(ref.get())
    else:
        print('doesnt exist')

def prepare_query(text_for_query):
    token_list=text_for_query.split(' ')

    stopWords = set(stopwords.words("english"))

    for i in token_list:
        if i in stopWords:
            token_list.remove(i)

    finalList=[]

    PS=PorterStemmer()

    for term in token_list:
        finalList.append(PS.stem(term))
    
    return finalList
#-----------------------------------------------------------    
query_text=input('enter the token')
print(prepare_query(query_text.lower()))



#initialize()
#search(token)
