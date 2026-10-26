
## 2024-05-14 - Firestore Bulk Upload Bottlenecks
**Learning:** Performing multiple individual `.set()` calls for bulk document creation in Firestore causes significant network overhead and potential rate-limiting, leading to bottlenecks. Firestore supports `db.batch()` which can handle up to 500 operations in a single network request.
**Action:** When performing bulk data uploads or creations (e.g., iterating through rows or dicts), always use `db.batch()` and chunk the operations to a maximum of 500 per batch.
