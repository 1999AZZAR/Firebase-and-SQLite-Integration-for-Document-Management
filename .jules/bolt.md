## 2024-05-24 - Firestore Bulk Upload Bottleneck
**Learning:** Uploading bulk data to Firestore using individual `.set()` calls creates severe network bottlenecks and slows down the application significantly.
**Action:** When performing bulk data uploads to Firestore, always use `db.batch()` with a maximum of 500 operations per batch to prevent network bottlenecks.
