## 2024-10-24 - Firestore Sequential Writes Bottleneck
**Learning:** Sequential writes to Firestore (`db.collection(...).document(...).set(...)` or `.delete()`) create a new network request for each operation, causing major performance bottlenecks during bulk operations like uploading large SQLite databases.
**Action:** Always use Firestore's `db.batch()` to group up to 500 writes or deletes into a single network request.
