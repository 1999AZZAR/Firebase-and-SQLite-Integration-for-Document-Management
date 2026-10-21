import sqlite3
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

def xlsx_to_sqlite(xlsx_file, db_file):
    # Read all sheets from the Excel file
    xls = pd.ExcelFile(xlsx_file)

    # Connect to SQLite database (or create it)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create tables for each sheet
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df.to_sql(sheet_name, conn, if_exists='replace', index=False)

    # Commit and close
    conn.commit()
    conn.close()

def upload_to_firebase(db_file, firebase_cred):
    # Initialize Firebase
    cred = credentials.Certificate(firebase_cred)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]

        # Read data from SQLite
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]

        # ⚡ Bolt: Use batched writes for bulk uploads to Firebase.
        # This significantly improves performance and prevents network bottlenecks
        # by executing up to 500 operations in a single network request.
        batch = db.batch()
        operation_count = 0

        # Upload data to Firebase with incremental document IDs
        for idx, row in enumerate(rows):
            data = dict(zip(columns, row))
            doc_id = f"{table_name}_{idx + 1}"
            doc_ref = db.collection(table_name).document(doc_id)
            batch.set(doc_ref, data)
            operation_count += 1

            # Firestore batches can only contain up to 500 operations
            if operation_count == 500:
                batch.commit()
                batch = db.batch()
                operation_count = 0

        # Commit any remaining operations
        if operation_count > 0:
            batch.commit()


    # Close the connection
    conn.close()

if __name__ == "__main__":
    xlsx_file = 'database_sementara.xlsx'
    db_file = 'output_database.db'
    firebase_cred = '/home/azzar/Downloads/project/firebase/config-firebase.json'

    xlsx_to_sqlite(xlsx_file, db_file)
    upload_to_firebase(db_file, firebase_cred)
