SELECT COUNT(*)
FROM executed_processes
WHERE process_id = ?
    AND status IN ('WAITING', 'RUNNING')