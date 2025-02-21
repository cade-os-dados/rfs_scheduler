SELECT 
    sp.args, sp.cwd, ep.process_id, ep.scheduled_time, 0
FROM executed_processes ep
LEFT JOIN scheduled_processes sp USING(process_id)
WHERE 
    status = 'WAITING' AND sp.status_id = 1 AND process_id IN ({})