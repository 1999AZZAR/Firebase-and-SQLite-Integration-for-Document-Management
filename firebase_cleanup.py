import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase(firebase_cred):
    # Initialize Firebase
    cred = credentials.Certificate(firebase_cred)
    firebase_admin.initialize_app(cred)
    return firestore.client()

def delete_collection(db, collection_name, batch_size):
    collection_ref = db.collection(collection_name)
    docs = collection_ref.limit(batch_size).stream()
    
    deleted = 0
    for doc in docs:
        doc.reference.delete()
        deleted += 1

    if deleted >= batch_size:
        return delete_collection(db, collection_name, batch_size)

def cleanup_firebase(firebase_cred):
    db = initialize_firebase(firebase_cred)
    
    # Get all collections
    collections = db.collections()
    
    for collection in collections:
        delete_collection(db, collection.id, 100)

if __name__ == "__main__":
    firebase_cred = '/home/azzar/Downloads/project/firebase/config-firebase.json'
    cleanup_firebase(firebase_cred)
