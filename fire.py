import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

<<<<<<< HEAD
def pushInFirebase(dictDoc):

    cred = credentials.Certificate('./talash-70578-firebase-adminsdk-jz0oc-e545575ec0.json')
    default_app = firebase_admin.initialize_app(cred,{'databaseURL': 'https://talash-70578.firebaseio.com/'})

    root=db.reference()
    ref=root.child('users')
    ref.set(dictDoc)
=======
cred = credentials.Certificate('./talash-70578-firebase-adminsdk-jz0oc-e545575ec0.json')
default_app = firebase_admin.initialize_app(cred,{'databaseURL': 'https://talash-70578.firebaseio.com/'})

root=db.reference()
ref=root.child('users').get()
print (ref)
>>>>>>> 029ab3f3d905d6e68f4c96ffef646e3e4e9c85ec
