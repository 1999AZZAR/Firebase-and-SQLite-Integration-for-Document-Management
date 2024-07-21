import firebase_admin
from firebase_admin import credentials, firestore
import sqlite3
import os


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

# Read a single document
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

def main():
    initialize_firebase()
    db = get_firestore_client()
    conn = initialize_sqlite_db()

    if db is None or conn is None:
        print("Failed to initialize the database. Exiting.")
        return

    c = conn.cursor()

    collection = 'users'
    doc_id = 'user1'
    data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'stat': 0
    }

    # Create
    create_document(db, c, collection, doc_id, data)

    # Create multiple documents
    multiple_data = {
        'user2': {'name': 'Jane Doe', 'email': 'jane.doe@example.com', 'stat': 1},
        'user3': {'name': 'Jim Beam', 'email': 'jim.beam@example.com', 'stat': 0}
    }
    create_multiple_documents(db, c, collection, multiple_data)

    # Read multiple documents
    read_multiple_documents(db, c, collection)

    # Read single document
    read_document(db, c, collection, doc_id)

    # Update
    update_document(db, c, collection, doc_id, {'stat': 1})

    # Read again to see the update
    read_document(db, c, collection, doc_id)

    # Delete
    delete_document(db, c, collection, doc_id)

if __name__ == "__main__":
    main()
