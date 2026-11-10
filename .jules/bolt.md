## 2024-05-19 - Bulk Firestore Upload Performance Bottleneck
**Learning:** Initializing multiple single `.set()` operations via a loop creates huge network bottlenecks and takes substantially longer. Firestore's batch APIs exist to mitigate this.
**Action:** When performing bulk data uploads to Firestore, always use `db.batch()` with a maximum of 500 operations per batch to prevent network bottlenecks caused by individual `.set()` calls.
