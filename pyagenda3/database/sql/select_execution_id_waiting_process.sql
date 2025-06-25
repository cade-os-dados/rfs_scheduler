SELECT executed_id
FROM executed_processes
WHERE process_id = ? AND status = 'WAITING'