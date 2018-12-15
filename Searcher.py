import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def initialize():
    cred = credentials.Certificate('./talash-70578-firebase-adminsdk-jz0oc-e545575ec0.json')
    default_app = firebase_admin.initialize_app(cred,{'databaseURL': 'https://talash-70578.firebaseio.com/'})

def search(token):
    root=db.reference()
    ref=root.child('users').child(token)

    if (ref.get() != None):
        print(ref.get())
    else:
        print('doesnt exist')

token=input('enter the token')
initialize()
search(token)
