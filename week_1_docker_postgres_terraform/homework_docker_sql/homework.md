# Homework Week 1

## Question 1. 

Understanding Docker images
Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container.

What's the version of pip in the image?

* 25.3 
* 24.3.1
* 24.2.1
* 23.3.1

## Answer (Solution 1): 25.3
Step 1: Run the Python:3.13 image with bash as the entrypoint. <br /> 
``` docker run -it --rm --entrypoint=bash python:3.13 ```<br /> 

Step 2: Run command to find version of the pip<br />
```pip --version```<br />

## Answer (Solution 2): 25.3
Step 1: Create a Dockerfile<br/>

Step 2: Write command in Dockerfile<br/>
```FROM python:3.13```<br/>
```ENTRYPOINT ["bash"]```<br/><br/>
Step 3: From the folder, run the docker build and run.<br/>
```docker build -t name .```<br/>
```docker run -it --rm name``` <br/>

## Question 2. 

Given the docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database? 

```
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

* postgres:5433
* localhost:5432
* db:5433
* postgres:5432
* db:5432 

## Answer: db:5432
In the section of the db in services, we can see the ports is 5433:5432. Postgres listen on the port 5432, 5433 is for the local host. <br/>

## Question 3
For the trips in November 2025, how many trips had a trip_distance of less than or equal to 1 mile? 

## Answer: 8007
```
SELECT COUNT(*) AS short_trips
FROM green_taxi_data
WHERE trip_distance <= 1
  AND green_taxi_data.lpep_pickup_datetime >= '2025-11-01'
  AND green_taxi_data.lpep_pickup_datetime < '2025-12-01';
```


## Question 4
Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles.

## Answer: 2025-11-14
```
SELECT DATE(lpep_pickup_datetime) AS pickup_day,
       MAX(trip_distance) AS longest_trip
FROM green_taxi_data
WHERE trip_distance < 100
GROUP BY pickup_day
ORDER BY longest_trip DESC
LIMIT 1;
```

## Question 5
Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

## Answer: East Harlem North
```
SELECT 
    z."Zone" AS pickup_zone,
    SUM(g."total_amount") AS total_revenue
FROM green_taxi_data g
JOIN taxi_zone_lookup z
    ON g."PULocationID" = z."LocationID"
WHERE g."lpep_pickup_datetime" >= '2025-11-18'
  AND g."lpep_pickup_datetime" < '2025-11-19'
GROUP BY z."Zone"
ORDER BY total_revenue DESC
LIMIT 1;
```

## Question 6
For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip? 

## Answer: Yorkville West
```
SELECT 
    dz."Zone" AS dropoff_zone,
    g."tip_amount"
FROM green_taxi_data g
JOIN taxi_zone_lookup pu
    ON g."PULocationID" = pu."LocationID"
JOIN taxi_zone_lookup dz
    ON g."DOLocationID" = dz."LocationID"
WHERE pu."Zone" = 'East Harlem North'
  AND g."lpep_pickup_datetime" >= '2025-11-01'
  AND g."lpep_pickup_datetime" < '2025-12-01'
ORDER BY g."tip_amount" DESC
LIMIT 1;
```
## Question 7
Which of the following sequences describes the Terraform workflow for: <br/>
1) Downloading plugins and setting up backend, <br/>
2) Generating and executing changes, <br/>
3) Removing all resources?

## Answer: terraform init, terraform apply -auto-approve, terraform destroy
Terraform init - Initialise a working directory containing configuration files and installs <br/>

Terraform apply -auto-approve - Applies changes defined in Terraform configuration <br/>

Terraform destroy - Deletes all resources that Terraform has created from configurations