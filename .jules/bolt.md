## 2024-05-24 - Firestore Bulk Uploads Network Bottleneck
**Learning:** Using individual `.set()` calls for bulk data uploads to Firestore can cause severe network bottlenecks and slow down the application significantly.
**Action:** Always use `db.batch()` with a maximum of 500 operations per batch when performing bulk data uploads to Firestore to prevent network bottlenecks and improve performance.
