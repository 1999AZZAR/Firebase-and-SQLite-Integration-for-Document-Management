## 2024-05-18 - Batch Firestore Writes
**Learning:** Performing bulk data uploads to Firestore using individual `.set()` calls causes severe network bottlenecks.
**Action:** Always use `db.batch()` with a maximum of 500 operations per batch when uploading multiple documents to Firestore.
