## 2023-10-24 - Batch Operations for Firebase Uploads
**Learning:** Performing individual `.set()` operations during bulk data uploads to Firestore causes severe network bottlenecks.
**Action:** Always use `db.batch()` with a maximum of 500 operations per batch when uploading bulk data to Firebase to optimize network usage and improve upload speed.
