## 2024-05-24 - Firestore Write Bottleneck
**Learning:** Uploading large amounts of data to Firestore using individual `.set()` calls creates significant network overhead and acts as a bottleneck.
**Action:** Always use `db.batch()` to write chunks of documents (up to 500 max per batch as per Firestore limits) when doing bulk uploads.
