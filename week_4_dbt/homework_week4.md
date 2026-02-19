# Data Engineering Zoomcamp - Week 4 Homework
## dbt Analytics Engineering

---

## Question 1: dbt Lineage and Execution

**Scenario:**
Given a dbt project with the following structure:
```
models/
├── staging/
│   ├── stg_green_tripdata.sql
│   └── stg_yellow_tripdata.sql
└── intermediate/
    └── int_trips_unioned.sql (depends on stg_green_tripdata & stg_yellow_tripdata)
```

**Question:** If you run `dbt run --select int_trips_unioned`, what models will be built?

**Options:**
- stg_green_tripdata, stg_yellow_tripdata, and int_trips_unioned (upstream dependencies)
- Any model with upstream and downstream dependencies to int_trips_unioned
- **int_trips_unioned only** ✅
- int_trips_unioned, int_trips, and fct_trips (downstream dependencies)

### Solution

**Answer: `int_trips_unioned` only**

The `dbt run --select` command is very specific in what it runs:

| Selector Pattern | What Gets Built |
|-----------------|-----------------|
| `model_name` | Just that model |
| `+model_name` | Upstream dependencies + that model |
| `model_name+` | That model + downstream dependencies |
| `+model_name+` | Everything in the chain |

Without the `+` prefix or suffix, dbt only builds the explicitly selected model.

---

## Question 2: dbt Tests

**Scenario:**
You've configured a generic test like this in your `schema.yml`:

```yaml
columns:
  - name: payment_type
    data_tests:
      - accepted_values:
          arguments:
            values: [1, 2, 3, 4, 5]
            quote: false
```

Your model `fct_trips` has been running successfully for months. A new value `6` now appears in the source data.

**Question:** What happens when you run `dbt test --select fct_trips`?

**Options:**
- dbt will skip the test because the model didn't change
- **dbt will fail the test, returning a non-zero exit code** ✅
- dbt will pass the test with a warning about the new value
- dbt will update the configuration to include the new value

### Solution

**Answer: dbt will fail the test, returning a non-zero exit code**

The `accepted_values` test checks that the `payment_type` column only contains values `[1, 2, 3, 4, 5]`.

When value `6` appears in the data:
1. ✅ dbt runs the test
2. ✅ The test finds rows with `payment_type = 6`
3. ✅ These rows violate the accepted values constraint
4. ✅ The test **fails** and returns a non-zero exit code (typically exit code 1)

The test is checking the *data*, not the model definition, so it always runs regardless of whether the model code changed.

---

## Question 3: Counting Records in fct_monthly_zone_revenue

**Question:** After running your dbt project, query the `fct_monthly_zone_revenue` model. What is the count of records?

**Options:**
- 12,998
- 14,120
- **12,184** ✅
- 15,421

### Solution

```sql
SELECT COUNT(*) 
FROM `zoomcamp-dbt-102030.nytaxi.fct_monthly_zone_revenue`;
```

**Answer: 12,184**

---

## Question 4: Best Performing Zone for Green Taxis (2020)

**Question:** Using the `fct_monthly_zone_revenue` table, find the pickup zone with the highest total revenue (`revenue_monthly_total_amount`) for Green taxi trips in 2020.

**Options:**
- **East Harlem North** ✅
- Morningside Heights
- East Harlem South
- Washington Heights South

### Solution

```sql
SELECT 
    pickup_zone,
    SUM(revenue_monthly_total_amount) AS total_revenue
FROM {{ ref('fct_monthly_zone_revenue') }}
WHERE 
    service_type = 'Green'
    AND EXTRACT(YEAR FROM revenue_month) = 2020
GROUP BY pickup_zone
ORDER BY total_revenue DESC
LIMIT 1;
```

**Answer: East Harlem North**

---

## Question 5: Green Taxi Trip Counts (October 2019)

**Question:** Using the `fct_monthly_zone_revenue` table, what is the total number of trips (`total_monthly_trips`) for Green taxis in October 2019?

**Options:**
- 500,234
- 350,891
- 384,624
- **385,624** ✅

### Solution

```sql
SELECT 
    SUM(total_monthly_trips) AS total_trips
FROM {{ ref('fct_monthly_zone_revenue') }}
WHERE 
    service_type = 'Green'
    AND revenue_month = '2019-10-01';
```

**Answer: 385,624**

---

## Question 6: Build a Staging Model for FHV Data

**Requirements:**
1. Load the FHV trip data for 2019 into your data warehouse
2. Create a staging model `stg_fhv_tripdata` with these requirements:
   - Filter out records where `dispatching_base_num` IS NULL
   - Rename fields to match your project's naming conventions (e.g., `PUlocationID` → `pickup_location_id`)

**Question:** What is the count of records in `stg_fhv_tripdata`?

**Options:**
- **42,084,899** ✅
- 43,244,693
- 22,998,722
- 44,112,187

### Solution

**Step 1: Create the staging model** (`models/staging/stg_fhv_tripdata.sql`)

```sql
{{ config(materialized='view') }}

SELECT
    -- identifiers
    dispatching_base_num,
    CAST(PUlocationID AS INT64) AS pickup_location_id,
    CAST(DOlocationID AS INT64) AS dropoff_location_id,
    
    -- timestamps
    CAST(pickup_datetime AS TIMESTAMP) AS pickup_datetime,
    CAST(dropOff_datetime AS TIMESTAMP) AS dropoff_datetime,
    
    -- trip info
    CAST(SR_Flag AS INT64) AS sr_flag,
    Affiliated_base_number AS affiliated_base_number

FROM {{ source('raw', 'fhv_tripdata') }}
WHERE dispatching_base_num IS NOT NULL
```

**Step 2: Count the records**

```sql
SELECT COUNT(*) AS num_of_records
FROM `zoomcamp-dbt-102030.nytaxi.stg_fhv_tripdata`;
```

**Answer: 42,084,899**

---

## Summary

This homework demonstrates key dbt concepts:
- ✅ Model selection and dependency management
- ✅ Data testing and validation
- ✅ Aggregation and analytical queries
- ✅ Staging model creation and data filtering
- ✅ Working with different taxi trip data sources (Green, Yellow, FHV)

---

## Tools Used

- **dbt Core 1.11.5** - Data transformation
- **BigQuery** - Data warehouse
- **Google Cloud Storage** - Raw data storage
- **Python** - Data ingestion scripts

---

## Project Structure

```
week_4_dbt/
├── models/
│   ├── staging/
│   │   ├── stg_green_tripdata.sql
│   │   ├── stg_yellow_tripdata.sql
│   │   ├── stg_fhv_tripdata.sql
│   │   └── sources.yml
│   ├── intermediate/
│   │   ├── int_trips_unioned.sql
│   │   └── int_trips.sql
│   └── marts/
│       ├── core/
│       │   ├── fct_trips.sql
│       │   └── dim_zones.sql
│       └── reporting/
│           └── fct_monthly_zone_revenue.sql
├── seeds/
│   ├── taxi_zone_lookup.csv
│   └── payment_type_lookup.csv
└── dbt_project.yml
```