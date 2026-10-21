## 2024-05-18 - Use Batched Writes for Firebase Bulk Uploads
**Learning:** When performing bulk data uploads to Firestore, issuing individual `document.set()` calls creates severe network bottlenecks and significantly degrades performance because each request requires its own network round trip.
**Action:** Always use `db.batch()` to combine up to 500 operations into a single network request. Keep a counter and commit/create a new batch whenever the 500-operation limit is reached, and don't forget to commit any remaining operations at the end.
