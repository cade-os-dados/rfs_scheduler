 CREATE TABLE IF NOT EXISTS executed_processes (
    process_id INTEGER PRIMARY KEY AUTOINCREMENT,
    process_name TEXT NOT NULL,
    free_memory_mb REAL,
    scheduled_time DATETIME NOT NULL,
    finished_time DATETIME,
    status TEXT NOT NULL,
    msg_error TEXT
)