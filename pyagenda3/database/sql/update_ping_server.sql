UPDATE ping_server 
SET 
    ping_status = 'ACTIVE', 
    last_ping = strftime('%Y-%m-%d %H:%M:%S', datetime('now', 'localtime')),
    free_memory_mb = ?
WHERE server_ip = ?