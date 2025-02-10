UPDATE scheduled_processes 
SET
    process_name = ?,
    args = ?,
    cwd = ?,
    scheduled_time = ?,
    interval = ?,
    status_id = ?
WHERE process_id = ?