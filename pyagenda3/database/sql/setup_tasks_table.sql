CREATE TABLE IF NOT EXISTS executed_tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    scheduled_time DATETIME NOT NULL,
    status TEXT NOT NULL
)