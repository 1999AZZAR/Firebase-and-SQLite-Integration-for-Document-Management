## 2023-10-24 - Bulk Firestore Uploads Optimization
**Learning:** Found individual `.set()` calls being used for bulk data uploads to Firestore in `upload_to_firebase`. This creates a network bottleneck. Using `db.batch()` allows up to 500 operations per network request, significantly improving upload performance.
**Action:** When performing bulk data uploads to Firestore, always use `db.batch()` with a maximum of 500 operations per batch instead of individual `.set()` calls.
