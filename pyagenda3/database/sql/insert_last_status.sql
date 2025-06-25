INSERT INTO last_status(process_id, last_status)
SELECT process_id, status as last_status
FROM (SELECT process_id, status, scheduled_time,
    ROW_NUMBER() OVER (PARTITION BY process_id ORDER BY scheduled_time DESC) as rn
FROM executed_processes) subquery
WHERE rn = 1