
## 2024-10-28 - Firestore Bulk Upload Bottleneck
**Learning:** When performing bulk data uploads to Firestore, individual `.set()` calls cause significant network bottlenecks.
**Action:** Always use `db.batch()` with a maximum of 500 operations per batch when uploading bulk data to prevent network bottlenecks.
