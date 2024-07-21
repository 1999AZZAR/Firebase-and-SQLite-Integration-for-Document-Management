import firebase_admin
from firebase_admin import credentials, firestore
import sqlite3
import os

# Initialize the Firebase app
def initialize_firebase():
    try:
        cred = credentials.Certificate('config-firebase.json')
        firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully.")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")

# Get a reference to the Firestore service
def get_firestore_client():
    try:
        return firestore.client()
    except Exception as e:
        print(f"Error getting Firestore client: {e}")
        return None

# Cache all documents from all collections
def cache_all_documents(db, c):
    try:
        collections = db.collections()
        for collection in collections:
            docs = collection.stream()
            for doc in docs:
                c.execute('''
                    INSERT OR REPLACE INTO cache (collection, document_id, data)
                    VALUES (?, ?, ?)
                ''', (collection.id, doc.id, str(doc.to_dict())))
        c.connection.commit()
        print("All documents cached successfully.")
    except Exception as e:
        print(f"Error caching documents: {e}")
def initialize_sqlite_db():
    try:
        conn = sqlite3.connect('local_cache.db')
        with conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS cache (
                    collection TEXT,
                    document_id TEXT,
                    data TEXT,
                    PRIMARY KEY (collection, document_id)
                )
            ''')
            print("SQLite database initialized successfully.")
        return conn
    except sqlite3.Error as e:
        print(f"Error initializing SQLite database: {e}")
        return None

# Create a new document
def create_document(db, c, collection_name, document_id, data):
    try:
        db.collection(collection_name).document(document_id).set(data)
        # Cache the document locally
        c.execute('''
            INSERT OR REPLACE INTO cache (collection, document_id, data)
            VALUES (?, ?, ?)
        ''', (collection_name, document_id, str(data)))
        c.connection.commit()
        print(f'Document {document_id} created in collection {collection_name} and cached locally')
    except Exception as e:
        print(f"Error creating document: {e}")

# Create multiple documents
def create_multiple_documents(db, c, collection_name, documents):
    try:
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
        c.connection.commit()
        print(f'Multiple documents created in collection {collection_name} and cached locally')
    except Exception as e:
        print(f"Error creating multiple documents: {e}")

# Read multiple documents
def read_multiple_documents(db, c, collection_name):
    try:
        # Try to read from the local cache first
        c.execute('SELECT document_id, data FROM cache WHERE collection = ?', (collection_name,))
        cached_docs = c.fetchall()
        if cached_docs:
            for doc_id, data in cached_docs:
                print(f'{doc_id} => {data}')
            return

        # If not in cache, read from Firestore
        docs = db.collection(collection_name).stream()
        document_ids = []
        for idx, doc in enumerate(docs):
            document_ids.append(doc.id)
            print(f"{idx + 1}. {doc.id}")
        if document_ids:
            return document_ids
        else:
            print(f"No documents found in collection {collection_name}")
            return []
    except Exception as e:
        print(f"Error reading multiple documents: {e}")

def read_document(db, c, collection_name, document_id):
    try:
        doc = db.collection(collection_name).document(document_id).get()
        if doc.exists:
            # Cache the document locally
            c.execute('''
                INSERT OR REPLACE INTO cache (collection, document_id, data)
                VALUES (?, ?, ?)
            ''', (collection_name, document_id, str(doc.to_dict())))
            c.connection.commit()
            print(f'Document data: {doc.to_dict()} (cached locally)')
        else:
            print(f'No such document in collection {collection_name}')
    except Exception as e:
        print(f"Error reading document: {e}")

# Update a document
def update_document(db, c, collection_name, document_id, data):
    try:
        db.collection(collection_name).document(document_id).update(data)
        # Update the local cache
        c.execute('''
            INSERT OR REPLACE INTO cache (collection, document_id, data)
            VALUES (?, ?, ?)
        ''', (collection_name, document_id, str(data)))
        c.connection.commit()
        print(f'Document {document_id} updated in collection {collection_name} and cache')
    except Exception as e:
        print(f"Error updating document: {e}")

# Delete a document
def delete_document(db, c, collection_name, document_id):
    try:
        db.collection(collection_name).document(document_id).delete()
        # Remove from the local cache
        c.execute('DELETE FROM cache WHERE collection = ? AND document_id = ?', (collection_name, document_id))
        c.connection.commit()
        print(f'Document {document_id} deleted from collection {collection_name} and cache')
    except Exception as e:
        print(f"Error deleting document: {e}")

def list_collections(db):
    try:
        collections = db.collections()
        collections_list = []
        for idx, collection in enumerate(collections):
            collections_list.append(collection.id)
            print(f"{idx + 1}. {collection.id}")
        return collections_list
    except Exception as e:
        print(f"Error listing collections: {e}")

def list_document_ids(db, collection_name):
    try:
        docs = db.collection(collection_name).stream()
        document_ids = []
        for idx, doc in enumerate(docs):
            document_ids.append(doc.id)
            print(f"{idx + 1}. {doc.id}")
        return document_ids
    except Exception as e:
        print(f"Error listing document IDs: {e}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    print("Select an operation:")
    print("1. Create a document")
    print("2. Create multiple documents")
    print("3. Read a document")
    print("4. Read multiple documents")
    print("5. Update a document")
    print("6. Delete a document")
    print("7. Clear screen")
    print("8. Exit")

def main():
    initialize_firebase()
    db = get_firestore_client()
    conn = initialize_sqlite_db()

    if db is None or conn is None:
        print("Failed to initialize the database. Exiting.")
        return

    c = conn.cursor()
    cache_all_documents(db, c)
    first_run = True
    while True:
        if first_run:
            clear_screen()
            first_run = False
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            collections = list_collections(db)
            collection_idx = int(input("Select collection by number (or 0 to cancel): ")) - 1
            if collection_idx == -1:
                continue
            collection = collections[collection_idx]
            document_ids = read_multiple_documents(db, c, collection)
            if document_ids:
                doc_id_idx = int(input("Select document ID by number (or 0 to cancel): ")) - 1
                if doc_id_idx == -1:
                    continue
                doc_id = document_ids[doc_id_idx]
                read_document(db, c, collection, doc_id)
            doc_id = input("Enter new document ID: ")
            doc_ref = db.collection(collection).document(doc_id)
            if doc_ref.get().exists:
                print(f"Document {doc_id} already exists. Switching to edit mode.")
                data = eval(input("Enter data to update as a dictionary: "))
                update_document(db, c, collection, doc_id, data)
            else:
                data = eval(input("Enter data as a dictionary: "))
                create_document(db, c, collection, doc_id, data)
        elif choice == '2':
            collections = list_collections(db)
            collection_idx = int(input("Select collection by number (or 0 to cancel): ")) - 1
            if collection_idx == -1:
                continue
            collection = collections[collection_idx]
            documents = eval(input("Enter documents as a dictionary: "))
            create_multiple_documents(db, c, collection, documents)
        elif choice == '3':
            collections = list_collections(db)
            collection_idx = int(input("Select collection by number (or 0 to cancel): ")) - 1
            if collection_idx == -1:
                continue
            collection = collections[collection_idx]
            document_ids = list_document_ids(db, collection)
            doc_id_idx = int(input("Select document ID by number (or 0 to cancel): ")) - 1
            if doc_id_idx == -1:
                continue
            doc_id = document_ids[doc_id_idx]
            read_document(db, c, collection, doc_id)
        elif choice == '4':
            collections = list_collections(db)
            collection_idx = int(input("Select collection by number (or 0 to cancel): ")) - 1
            if collection_idx == -1:
                continue
            collection = collections[collection_idx]
            read_multiple_documents(db, c, collection)
        elif choice == '5':
            collections = list_collections(db)
            collection_idx = int(input("Select collection by number (or 0 to cancel): ")) - 1
            if collection_idx == -1:
                continue
            collection = collections[collection_idx]
            document_ids = list_document_ids(db, collection)
            doc_id_idx = int(input("Select document ID by number (or 0 to cancel): ")) - 1
            if doc_id_idx == -1:
                continue
            doc_id = document_ids[doc_id_idx]
            data = eval(input("Enter data to update as a dictionary: "))
            update_document(db, c, collection, doc_id, data)
        elif choice == '6':
            collections = list_collections(db)
            collection_idx = int(input("Select collection by number: ")) - 1
            collection = collections[collection_idx]
            document_ids = list_document_ids(db, collection)
            doc_id_idx = int(input("Select document ID by number (or 0 to cancel): ")) - 1
            if doc_id_idx == -1:
                continue
            doc_id = document_ids[doc_id_idx]
            delete_document(db, c, collection, doc_id)
        elif choice == '7':
            clear_screen()
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
