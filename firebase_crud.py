import firebase_admin
from firebase_admin import credentials, firestore
import sqlite3

# Initialize the Firebase app
cred = credentials.Certificate('config-firebase.json')
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

def list_collections():
    collections = db.collections()
    collections_list = []
    for idx, collection in enumerate(collections):
        collections_list.append(collection.id)
        print(f"{idx + 1}. {collection.id}")
    return collections_list

def list_document_ids(collection_name):
    docs = db.collection(collection_name).stream()
    document_ids = []
    for idx, doc in enumerate(docs):
        document_ids.append(doc.id)
        print(f"{idx + 1}. {doc.id}")
    return document_ids

def display_menu():
    print("Select an operation:")
    print("1. Create a document")
    print("2. Create multiple documents")
    print("3. Read a document")
    print("4. Read multiple documents")
    print("5. Update a document")
    print("6. Delete a document")
    print("7. Exit")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            collections = list_collections()
            collection_idx = int(input("Select collection by number: ")) - 1
            collection = collections[collection_idx]
            document_ids = list_document_ids(collection)
            doc_id_idx = int(input("Select document ID by number: ")) - 1
            doc_id = document_ids[doc_id_idx]
            data = eval(input("Enter data as a dictionary: "))
            create_document(collection, doc_id, data)
        elif choice == '2':
            collections = list_collections()
            collection_idx = int(input("Select collection by number: ")) - 1
            collection = collections[collection_idx]
            documents = eval(input("Enter documents as a dictionary: "))
            create_multiple_documents(collection, documents)
        elif choice == '3':
            collections = list_collections()
            collection_idx = int(input("Select collection by number: ")) - 1
            collection = collections[collection_idx]
            document_ids = list_document_ids(collection)
            doc_id_idx = int(input("Select document ID by number: ")) - 1
            doc_id = document_ids[doc_id_idx]
            read_document(collection, doc_id)
        elif choice == '4':
            collection = input("Enter collection name: ")
            read_multiple_documents(collection)
        elif choice == '5':
            collection = input("Enter collection name: ")
            doc_id = input("Enter document ID: ")
            data = eval(input("Enter data to update as a dictionary: "))
            update_document(collection, doc_id, data)
        elif choice == '6':
            collection = input("Enter collection name: ")
            doc_id = input("Enter document ID: ")
            delete_document(collection, doc_id)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
