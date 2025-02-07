UPDATE executed_processes 
    SET finished_time = ?,
        status = ?,
        msg_error = ?
    WHERE process_id = ?