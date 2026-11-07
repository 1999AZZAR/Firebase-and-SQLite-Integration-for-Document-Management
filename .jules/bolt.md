## 2024-05-18 - Firestore Bulk Upload Bottleneck
**Learning:** Found that uploading data row-by-row using individual `document().set()` calls causes a significant network bottleneck and increases upload time proportionally to the number of records.
**Action:** Always use `db.batch()` with chunks (max 500 operations per Firestore limits) when performing bulk data uploads to reduce network round trips and improve performance.
