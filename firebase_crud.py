import firebase_admin
from firebase_admin import credentials, firestore
import sqlite3

# Initialize the Firebase app
firebaseConfig = {
    "apiKey": "AIzaSyC9JhuNTi0lEGi5SJrz2mwvp0xALCR409g",
    "authDomain": "washapp-test-app.firebaseapp.com",
    "databaseURL": "https://washapp-test-app-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "washapp-test-app",
    "storageBucket": "washapp-test-app.appspot.com",
    "messagingSenderId": "711370391927",
    "appId": "1:711370391927:web:234315043b5f86c08e6172"
}

cred = credentials.Certificate(firebaseConfig)
firebase_admin.initialize_app(cred)

# Get a reference to the Firestore service
db = firestore.client()

# Initialize the SQLite database
conn = sqlite3.connect('local_cache.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS cache (
        collection TEXT,
        document_id TEXT,
        data TEXT,
        PRIMARY KEY (collection, document_id)
    )
''')
conn.commit()

# Create a new document
def create_document(collection_name, document_id, data):
    db.collection(collection_name).document(document_id).set(data)
    # Cache the document locally
    c.execute('''
        INSERT OR REPLACE INTO cache (collection, document_id, data)
        VALUES (?, ?, ?)
    ''', (collection_name, document_id, str(data)))
    conn.commit()
    print(f'Document {document_id} created in collection {collection_name} and cached locally')

# Create multiple documents
def create_multiple_documents(collection_name, documents):
    batch = db.batch()
    for doc_id, data in documents.items():
        doc_ref = db.collection(collection_name).document(doc_id)
        batch.set(doc_ref, data)
    batch.commit()
    # Cache the documents locally
    for doc_id, data in documents.items():
        c.execute('''
            INSERT OR REPLACE INTO cache (collection, document_id, data)
            VALUES (?, ?, ?)
        ''', (collection_name, doc_id, str(data)))
    conn.commit()
    print(f'Multiple documents created in collection {collection_name} and cached locally')

# Read multiple documents
def read_multiple_documents(collection_name):
    docs = db.collection(collection_name).stream()
    # Try to read from the local cache first
    c.execute('SELECT document_id, data FROM cache WHERE collection = ?', (collection_name,))
    cached_docs = c.fetchall()
    if cached_docs:
        for doc_id, data in cached_docs:
            print(f'{doc_id} => {data}')
        return

    # If not in cache, read from Firestore
    docs = db.collection(collection_name).stream()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
def read_document(collection_name, document_id):
    doc = db.collection(collection_name).document(document_id).get()
    if doc.exists:
        # Cache the document locally
        c.execute('''
            INSERT OR REPLACE INTO cache (collection, document_id, data)
            VALUES (?, ?, ?)
        ''', (collection_name, document_id, str(doc.to_dict())))
        conn.commit()
        print(f'Document data: {doc.to_dict()} (cached locally)')
    else:
        print(f'No such document in collection {collection_name}')

# Update a document
def update_document(collection_name, document_id, data):
    db.collection(collection_name).document(document_id).update(data)
    # Update the local cache
    c.execute('''
        INSERT OR REPLACE INTO cache (collection, document_id, data)
        VALUES (?, ?, ?)
    ''', (collection_name, document_id, str(data)))
    conn.commit()
    print(f'Document {document_id} updated in collection {collection_name} and cache')

# Delete a document
def delete_document(collection_name, document_id):
    db.collection(collection_name).document(document_id).delete()
    # Remove from the local cache
    c.execute('DELETE FROM cache WHERE collection = ? AND document_id = ?', (collection_name, document_id))
    conn.commit()
    print(f'Document {document_id} deleted from collection {collection_name} and cache')

# Example usage
if __name__ == "__main__":
    collection = 'users'
    doc_id = 'user1'
    data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'age': 30
    }

    # Create
    create_document(collection, doc_id, data)

    # Create multiple documents
    multiple_data = {
        'user2': {'name': 'Jane Doe', 'email': 'jane.doe@example.com', 'age': 25},
        'user3': {'name': 'Jim Beam', 'email': 'jim.beam@example.com', 'age': 35}
    }
    create_multiple_documents(collection, multiple_data)

    # Read multiple documents
    read_multiple_documents(collection)

    # Read single document
    read_document(collection, doc_id)

    # Update
    update_document(collection, doc_id, {'age': 31})

    # Read again to see the update
    read_document(collection, doc_id)

    # Delete
    delete_document(collection, doc_id)
