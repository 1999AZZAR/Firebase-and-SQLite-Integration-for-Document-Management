import firebase_admin
from firebase_admin import credentials, firestore

# Initialize the Firebase app
cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Get a reference to the Firestore service
db = firestore.client()

# Create a new document
def create_document(collection_name, document_id, data):
    db.collection(collection_name).document(document_id).set(data)
    print(f'Document {document_id} created in collection {collection_name}')

# Create multiple documents
def create_multiple_documents(collection_name, documents):
    batch = db.batch()
    for doc_id, data in documents.items():
        doc_ref = db.collection(collection_name).document(doc_id)
        batch.set(doc_ref, data)
    batch.commit()
    print(f'Multiple documents created in collection {collection_name}')

# Read multiple documents
def read_multiple_documents(collection_name):
    docs = db.collection(collection_name).stream()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
def read_document(collection_name, document_id):
    doc = db.collection(collection_name).document(document_id).get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
    else:
        print(f'No such document in collection {collection_name}')

# Update a document
def update_document(collection_name, document_id, data):
    db.collection(collection_name).document(document_id).update(data)
    print(f'Document {document_id} updated in collection {collection_name}')

# Delete a document
def delete_document(collection_name, document_id):
    db.collection(collection_name).document(document_id).delete()
    print(f'Document {document_id} deleted from collection {collection_name}')

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
