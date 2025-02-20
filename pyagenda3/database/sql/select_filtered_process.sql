SELECT 
    args, cwd, process_id, scheduled_time, interval 
FROM 
    scheduled_processes 
WHERE 
    process_id IN ({})