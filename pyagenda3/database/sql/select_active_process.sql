SELECT 
    args, cwd, process_id, scheduled_time, interval 
FROM 
    scheduled_processes 
WHERE 
    status_id = 1