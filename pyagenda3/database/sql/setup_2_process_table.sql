 CREATE TABLE IF NOT EXISTS executed_processes (
    executed_id INTEGER PRIMARY KEY AUTOINCREMENT,
    process_id INTEGER NOT NULL,
    free_memory_mb REAL,
    scheduled_time DATETIME NOT NULL,
    finished_time DATETIME,
    status TEXT NOT NULL,
    msg_error TEXT,
    FOREIGN KEY(process_id) REFERENCES scheduled_processes(process_id)
)