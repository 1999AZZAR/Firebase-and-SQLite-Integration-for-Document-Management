## 2024-05-18 - Firestore Bulk Upload Network Bottleneck
**Learning:** Sequential individual `.set()` calls to Firestore for bulk data uploads cause severe network bottlenecks.
**Action:** Always use `db.batch()` with a maximum of 500 operations per batch when performing bulk data uploads to Firestore to prevent network bottlenecks.
