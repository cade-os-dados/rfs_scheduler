 CREATE TABLE IF NOT EXISTS ping_server (
    server_ip TEXT NOT NULL,
    server_nickname TEXT,
    free_memory_mb REAL,
    last_ping DATETIME,
    ping_status TEXT NOT NULL
)