# Data Engineering Zoomcamp - Week 3 Homework
## BigQuery and Data Warehousing

---

## Q1: What is count of records for the 2024 Yellow Taxi Data?

**Options:**
- 65,623
- 840,402
- **20,332,093** ✅
- 85,431,289

### Solution:

**Step 1: Create the Dataset**
1. Fill in Dataset ID
2. Keep Data location: Sydney
3. Click "Create dataset"

**Step 2: Create External Table**
1. Click the 3 dots next to the dataset name
2. Click "Create table"
3. Configure the table:
   - Source: Google Cloud Storage
   - File path: `dezoomcamp_hw3_2026_dk/yellow_tripdata_*.parquet`
   - File format: Parquet
   - Destination table name: `yellow_taxi_external`
   - Table type: External table
   - Schema: Auto detect

**Step 3: SQL Query**
```sql
SELECT COUNT(*) 
FROM `dk-datawarehouse-zoomcamp.yellow_taxi_dataset.yellow_taxi_external`;
```

**Answer: 20,332,093**

---

## Q2: Estimated Data Read - External vs Materialized Table

**Question:** Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

**Options:**
- **18.82 MB for the External Table and 47.60 MB for the Materialized Table** ✅
- 0 MB for the External Table and 155.12 MB for the Materialized Table
- 2.14 GB for the External Table and 0MB for the Materialized Table
- 0 MB for the External Table and 0MB for the Materialized Table

### Solution:

**Query for Native/Materialized Table:**
```sql
SELECT COUNT(DISTINCT PULocationID)  
FROM `dk-datawarehouse-zoomcamp.yellow_taxi_dataset.yellow_taxi_native`;
```

**Query for External Table:**
```sql
SELECT COUNT(DISTINCT PULocationID)  
FROM `dk-datawarehouse-zoomcamp.yellow_taxi_dataset.yellow_taxi_external`;
```

Check the **Job Information** tab → **Bytes processed** for each query.

**Answer: 18.82 MB for the External Table and 47.60 MB for the Materialized Table**

---

## Q3: Columnar Database Byte Differences

**Question:** Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?

**Options:**
- **BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.** ✅
- BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, doubling the estimated bytes processed.
- BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.
- When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed

### Solution:

**Query 1: Single Column**
```sql
SELECT PULocationID
FROM `dk-datawarehouse-zoomcamp.yellow_taxi_dataset.yellow_taxi_native`;
```

**Query 2: Two Columns**
```sql
SELECT PULocationID, DOLocationID
FROM `dk-datawarehouse-zoomcamp.yellow_taxi_dataset.yellow_taxi_native`;
```

### Explanation:
BigQuery stores data in a columnar format, meaning:
- Each column is stored separately
- BigQuery only reads the requested columns from storage
- Query 1 reads only `PULocationID` → processes ~X bytes
- Query 2 reads both `PULocationID` AND `DOLocationID` → processes ~2X bytes

**Answer: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.**

---

## Q4: Records with Zero Fare Amount

**Question:** How many records have a fare_amount of 0?

**Options:**
- 128,210
- 546,578
- 20,188,016
- **8,333** ✅

### Solution:

```sql
SELECT COUNT(*) 
FROM `dk-datawarehouse-zoomcamp.yellow_taxi_dataset.yellow_taxi_native`
WHERE fare_amount = 0;
```

**Answer: 8,333**

---

## Q5: Optimized Table Strategy - Partitioning and Clustering

**Question:** What is the best strategy to make an optimized table in BigQuery if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID?

**Options:**
- **Partition by tpep_dropoff_datetime and Cluster on VendorID** ✅
- Cluster on by tpep_dropoff_datetime and Cluster on VendorID
- Cluster on tpep_dropoff_datetime Partition by VendorID
- Partition by tpep_dropoff_datetime and Partition by VendorID

### Solution:

**Create the optimized table:**
```sql
CREATE OR REPLACE TABLE `dk-datawarehouse-zoomcamp.yellow_taxi_dataset.yellow_taxi_optimized`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `dk-datawarehouse-zoomcamp.yellow_taxi_dataset.yellow_taxi_native`;
```

### Reasoning:
- Can only have **ONE partition column** in BigQuery
- Clustering both columns doesn't make sense - wastes resources
- More efficient to **partition** based on date/time (for filtering)
- Then **cluster** by VendorID (for sorting/ordering)
- Partition columns must be DATE, TIMESTAMP, or INTEGER ranges (VendorID doesn't qualify)

**Answer: Partition by tpep_dropoff_datetime and Cluster on VendorID**

---

## Q6: Partitioned vs Non-Partitioned Table Performance

**Question:** Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive). Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?

**Options:**
- 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
- **310.24 MB for non-partitioned table and 26.84 MB for the partitioned table** ✅
- 5.87 MB for non-partitioned table and 0 MB for the partitioned table
- 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table

### Solution:

**Query 1: Non-Partitioned Table**
```sql
SELECT DISTINCT VendorID
FROM `dk-datawarehouse-zoomcamp.yellow_taxi_dataset.yellow_taxi_native`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```

**Query 2: Partitioned Table**
```sql
SELECT DISTINCT VendorID
FROM `dk-datawarehouse-zoomcamp.yellow_taxi_dataset.yellow_taxi_optimized`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```

Check **Job Information → Bytes processed** for both queries.

### Key Insight:
- **Non-partitioned table**: Must scan the ENTIRE table → ~310 MB
- **Partitioned table**: Only scans partitions for March 1-15 → ~27 MB
- This demonstrates the massive benefit of partitioning (12x less data scanned!)

**Answer: 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table**

---

## Q7: External Table Data Storage Location

**Question:** Where is the data stored in the External Table you created?

**Options:**
- Big Query
- Container Registry
- **GCP Bucket** ✅
- Big Table

### Solution:

**External Table:**
- Data stays in GCS buckets (Cloud Storage)
- BigQuery just points to it and queries it on-demand
- Only metadata (table schema, pointer to GCS) is stored in BigQuery

**Native/Materialized Table:**
- Data is copied into BigQuery's internal storage
- Stored in BigQuery's proprietary columnar format

**Answer: GCP Bucket**

---

## Q8: Clustering Best Practice

**Question:** It is best practice in BigQuery to always cluster your data:

**Options:**
- True
- **False** ✅

### Solution:

**When NOT to cluster:**
- Table is very small (<1GB)
- Columns have very high cardinality (millions of unique values)
- You query all data without filters
- Ad-hoc queries with no consistent filter patterns

**When TO cluster:**
- Table is large (>1GB)
- You frequently filter/sort/group by specific columns
- Query patterns are consistent and predictable

**Answer: False**

---

## Q9: COUNT(*) Bytes Processed

**Question:** Write a `SELECT count(*)` query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

### Solution:

```sql
SELECT COUNT(*) 
FROM `dk-datawarehouse-zoomcamp.yellow_taxi_dataset.yellow_taxi_native`;
```

**Check Job Information → Bytes processed**

### Explanation:

BigQuery stores **metadata** about tables, including:
- Total row count
- Column statistics
- Table size
- Min/max values

When you run `COUNT(*)` (without a WHERE clause):
- BigQuery **doesn't scan any actual data**
- It reads the row count directly from the **table metadata**
- Returns the answer instantly
- **Bytes processed: 0 B**
- No cost (BigQuery doesn't charge for metadata queries)

**Answer: 0 Bytes**

---

## Summary

This homework demonstrates key BigQuery concepts:
1. External vs Native tables
2. Columnar storage and query optimization
3. Partitioning and clustering strategies
4. Query performance analysis
5. Metadata-based query optimization
