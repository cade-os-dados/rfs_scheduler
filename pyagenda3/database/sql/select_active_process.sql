SELECT 
    process_name, args, scheduled_time, interval 
FROM 
    scheduled_processes 
WHERE 
    status_id = 1