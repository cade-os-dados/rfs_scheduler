SELECT 
    server_ip 
FROM
    ping_server 
WHERE 
    ping_status = 'ACTIVE'