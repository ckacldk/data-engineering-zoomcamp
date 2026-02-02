# Homework Solutions

## Q1 Solution

**Question:** Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e. the output file yellow_tripdata_2020-12.csv of the extract task)?

**Options:**
* 128.3 MiB
* 134.5 MiB
* 364.7 MiB
* 692.6 MiB

**Steps to Solve:**

1. Utilize the `08_gcp_taxi` workflow and execute for month 12 of 2020 with the yellow option
2. Once done, the Metric shows the size: `134,481,400 bytes`
3. Convert bytes to MiB: `134,481,400 bytes ÷ 1,048,576 = 128.251 MiB`

**Answer:** 128.3 MiB
<img width="1270" height="630" alt="A kestra" src="https://github.com/user-attachments/assets/c09a6d3c-b8ed-41db-80fa-c7d3e75183a6" />

---

## Q2 Solution

**Question:** What is the rendered value of the variable file when the inputs taxi is set to green, year is set to 2020, and month is set to 04 during execution?

**Options:**
* `{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv`
* `green_tripdata_2020-04.csv`
* `green_tripdata_04_2020.csv`
* `green_tripdata_2020.csv`

**Explanation:**

The Kestra file uses the following variable definition:
```yaml
variables:
  file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"
```

When rendered with the given inputs:
- `taxi = green`
- `year = 2020`
- `month = 04`

**Answer:** `green_tripdata_2020-04.csv`

---

## Q3 Solution

**Question:** How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?

**Options:**
* 13,537,299
* 24,648,499
* 18,324,219
* 29,430,127

**BigQuery Solution:**
```sql
SELECT SUM(row_count) as total_rows
FROM `kestra-sandbox102030.zoomcamp.__TABLES__`
WHERE table_id LIKE 'yellow_tripdata_2020%'
  AND table_id NOT LIKE '%_ext'
```

**Answer:** 24,648,499

---

## Q4 Solution

**Question:** How many rows are there for the Green Taxi data for all CSV files in the year 2020?

**Options:**
* 5,327,301
* 936,199
* 1,734,051
* 1,342,034

**BigQuery Solution:**
```sql
SELECT SUM(row_count) as total_rows
FROM `kestra-sandbox102030.zoomcamp.__TABLES__`
WHERE table_id LIKE 'green_tripdata_2020%'
  AND table_id NOT LIKE '%_ext'
```

**Answer:** 1,734,051

---

## Q5 Solution

**Question:** How many rows are there for the Yellow Taxi data for the March 2021 CSV file?

**Options:**
* 1,428,092
* 706,911
* 1,925,152
* 2,561,031

**Steps to Solve:**

1. Need to include "2021" in the year values to enable execution for 2021 data
2. Update the workflow configuration:
```yaml
- id: year
  type: SELECT
  displayName: Select year
  values: ["2019", "2020", "2021"]
  defaults: "2021"
  allowCustomValue: true
```

3. Execute the workflow for Yellow Taxi, March 2021

**Answer:** 1,925,152

<img width="672" height="637" alt="go kestra-sandbox102030  Datasets  200mcamp  Tables  yellow _tripdata_2021_03" src="https://github.com/user-attachments/assets/af89bfc5-4736-4ae3-b851-ee5a71f9277c" />


---

## Q6 Solution

**Question:** How would you configure the timezone to New York in a Schedule trigger?

**Options:**
* Add a timezone property set to EST in the Schedule trigger configuration
* Add a timezone property set to America/New_York in the Schedule trigger configuration
* Add a timezone property set to UTC-5 in the Schedule trigger configuration
* Add a location property set to New_York in the Schedule trigger configuration

**Explanation:**

Kestra uses `Etc/UTC` timezone by default. To configure a different timezone:
<img width="570" height="175" alt="timezone $" src="https://github.com/user-attachments/assets/1167752f-bb01-4692-ab74-bc168cf3dbf4" />

1. Kestra documentation references the IANA timezone database
2. According to the [IANA Time Zone Database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones), New York uses the identifier: `America/New_York`
3. This timezone identifier should be used in the Schedule trigger configuration

**Answer:** Add a timezone property set to America/New_York in the Schedule trigger configuration.
