# Firebase CRUD Operations in Python

This repository contains a Python script to perform CRUD (Create, Read, Update, Delete) operations on a Firebase Firestore database using the `firebase-admin` SDK.

## Prerequisites

- Python 3.x
- Firebase project with Firestore enabled
- Firebase Admin SDK service account key

## Setup

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required Python packages:
    ```bash
    pip install firebase-admin
    ```

3. Place your Firebase Admin SDK service account key JSON file in the project directory and update the path in `firebase_crud.py`:
    ```python
    cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
    ```

## Usage

The `firebase_crud.py` script provides functions to create, read, update, and delete documents in a Firestore collection.

### Functions

- `create_document(collection_name, document_id, data)`: Creates a new document in the specified collection.
- `create_multiple_documents(collection_name, documents)`: Creates multiple documents in the specified collection.
- `read_document(collection_name, document_id)`: Reads a single document from the specified collection.
- `read_multiple_documents(collection_name)`: Reads all documents from the specified collection.
- `update_document(collection_name, document_id, data)`: Updates an existing document in the specified collection.
- `delete_document(collection_name, document_id)`: Deletes a document from the specified collection.

### Example Usage

The script includes an example usage section that demonstrates how to use the functions:

```python
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
```

## License

This project is licensed under the MIT License.
