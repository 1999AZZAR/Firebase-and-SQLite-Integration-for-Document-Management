# Firebase CRUD Operations in Python

This repository contains Python scripts to perform CRUD (Create, Read, Update, Delete) operations on a Firebase Firestore database using the `firebase-admin` SDK, as well as to convert Excel files to SQLite databases and upload SQLite data to Firebase.

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

2. Install the required Python packages listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

3. Place your Firebase Admin SDK service account key JSON file in the project directory. You will be prompted to enter the path to this file when running the scripts.
    ```python
    cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
    ```

## Usage

The `firebase_crud.py` script provides a menu-driven interface to perform various operations on a Firestore collection, including CRUD operations, clearing the screen, nuking the Firebase database, converting Excel files to SQLite databases, and uploading SQLite data to Firebase.

### Menu Options

1. Create a document
2. Create multiple documents
3. Read a document
4. Read multiple documents
5. Update a document
6. Delete a document
7. Clear screen
8. Nuke Firebase Database
9. Convert Excel to SQLite
10. Upload SQLite to Firebase
11. Exit


## License

This project is licensed under the MIT License.
### Additional Scripts

- `basic_crud.py`: Contains basic CRUD operations and a main function to demonstrate these operations.
- `firebase_cleanup.py`: Contains functions to clean up the Firebase database.
- `xlsx_to_sqlite_firebase.py`: Contains functions to convert Excel files to SQLite databases and upload SQLite data to Firebase.
## License

This project is licensed under the MIT License.
