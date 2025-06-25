UPDATE ping_server
SET 
    last_ping = strftime('%Y-%m-%d %H:%M:%S', datetime('now','localtime'))
    ping_status = 'WAITING'
WHERE server_ip = ?