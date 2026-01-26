# Datatalks Zoomcamp Homework

## Week 1

### Question 3

```sql
SELECT COUNT(*) AS trip_count
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= TIMESTAMP '2025-11-01'
  AND lpep_pickup_datetime <  TIMESTAMP '2025-12-01'
  AND trip_distance <= 1;
```

### Question 4

```sql
SELECT lpep_pickup_datetime
FROM green_taxi_trips
WHERE trip_distance = (select max(trip_distance) from green_taxi_trips where trip_distance <= 100)
```

### Question 5

```sql
SELECT
    tzl."Zone",
    SUM(gtt.total_amount) AS total_revenue
FROM green_taxi_trips gtt
JOIN taxi_zone_lookup tzl
  ON gtt."PULocationID" = tzl."LocationID"
WHERE gtt.lpep_pickup_datetime >= TIMESTAMP '2025-11-18'
  AND gtt.lpep_pickup_datetime <  TIMESTAMP '2025-11-19'
GROUP BY tzl."Zone"
ORDER BY total_revenue DESC
LIMIT 1;
```

### Question 6

todo
