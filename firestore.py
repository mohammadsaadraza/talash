import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

start = time.time()

cred = credentials.Certificate('./talash-70578-firebase-adminsdk-jz0oc-e545575ec0.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

#doc_ref = db.collection(u'users').document(u'alovelace')
#doc_ref.set({"Ali" : 19, "Taimoor" : 19})



users_ref = db.collection(u'users').document(u'alovelace')
docs = users_ref.get()

print(docs.to_dict())
print(time.time()-start)
