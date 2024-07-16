# Firebase CRUD Operations in Python

This repository contains a Python script to perform CRUD (Create, Read, Update, Delete) operations on a Firebase Firestore database using the `firebase-admin` SDK.

## Prerequisites

- Python 3.x
- Firebase project with Firestore enabled
- Firebase Admin SDK service account key

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/1999AZZAR/Firebase-and-SQLite-Integration-for-Document-Management.git
    cd Firebase-and-SQLite-Integration-for-Document-Management
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


## License

This project is licensed under the MIT License.
