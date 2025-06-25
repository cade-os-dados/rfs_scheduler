SELECT 
    ep.process_id
FROM executed_processes ep
LEFT JOIN scheduled_processes sp USING(process_id)
WHERE 
    status = 'WAITING' AND sp.status_id = 1