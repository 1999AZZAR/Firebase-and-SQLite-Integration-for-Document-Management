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

# Read a document
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

    # Read
    read_document(collection, doc_id)

    # Update
    update_document(collection, doc_id, {'age': 31})

    # Read again to see the update
    read_document(collection, doc_id)

    # Delete
    delete_document(collection, doc_id)
