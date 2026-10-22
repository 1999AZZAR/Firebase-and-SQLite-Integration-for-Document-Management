## 2024-03-24 - Firestore Bulk Write Bottlenecks
**Learning:** Performing bulk operations on Firestore using individual `.set()` calls creates significant network bottlenecks. Firestore also has a hard limit of 500 operations per batch when using `db.batch()`. Failing to chunk batches exceeding this limit will result in errors.
**Action:** When performing bulk data uploads or creations to Firestore, always use `db.batch()` and ensure that operations are chunked with a maximum of 500 operations per batch to prevent network bottlenecks and batch limit failures.
