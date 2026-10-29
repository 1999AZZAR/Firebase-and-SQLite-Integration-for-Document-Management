## 2024-05-19 - Bulk Firestore Operations Bottleneck
**Learning:** Individual .set() calls during bulk uploads create severe network bottlenecks. Firestore supports batching up to 500 operations.
**Action:** Always use db.batch() with a limit of 500 operations per batch for bulk uploads to Firestore.
