UPDATE executed_processes 
    SET finished_time = ?,
        status = ?,
        msg_error = ?
    WHERE id = ?