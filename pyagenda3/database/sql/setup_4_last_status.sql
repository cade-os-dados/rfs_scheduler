 CREATE TABLE IF NOT EXISTS last_status (
    process_id INTEGER NOT NULL,
    last_status TEXT,
    FOREIGN KEY(process_id) REFERENCES scheduled_processes(process_id)
)