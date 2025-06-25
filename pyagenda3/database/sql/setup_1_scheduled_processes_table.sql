 CREATE TABLE IF NOT EXISTS scheduled_processes (
    process_id INTEGER PRIMARY KEY AUTOINCREMENT,
    process_name TEXT NOT NULL,
    args TEXT NOT NULL,
    cwd TEXT NOT NULL,
    scheduled_time DATETIME NOT NULL,
    interval INT,
    status_id -- 0 ou 1, se está ativo ou inativo
    --future
    /*
        timeout INT NOT NULL,
        priority INT NOT NULL,
        total_time INT, -- tempo gasto com todas as vezes que rodou
        num_runs INT, -- quantidade de vezes que rodou
        mean_time REAL -- tempo médio para rodar
    */
)