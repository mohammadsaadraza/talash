import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


def pushInFirebase(dictDoc):

    cred = credentials.Certificate('./talash-70578-firebase-adminsdk-jz0oc-e545575ec0.json')
    default_app = firebase_admin.initialize_app(cred,{'databaseURL': 'https://talash-70578.firebaseio.com/'})
    #firebase_admin.initialize_app(cred)
    #db = firestore.client()
    #db.collection("ForwardIndex").document("FI").set(dictDoc)

    root=db.reference()
    ref=root.child('InvertedIndex')
    ref.set(dictDoc)

def pushInFirebaseHead(dictDoc):

    cred = credentials.Certificate('./talash-70578-firebase-adminsdk-jz0oc-e545575ec0.json')
    default_app = firebase_admin.initialize_app(cred,{'databaseURL': 'https://talash-70578.firebaseio.com/'})

    root=db.reference()
    ref=root.child('head')
    ref.push().set(dictDoc)

def pushInFirebaseUrl(dictDoc):

    cred = credentials.Certificate('./talash-70578-firebase-adminsdk-jz0oc-e545575ec0.json')
    default_app = firebase_admin.initialize_app(cred,{'databaseURL': 'https://talash-70578.firebaseio.com/'})

    root=db.reference()
    ref=root.child('url')
    ref.push().set(dictDoc)
