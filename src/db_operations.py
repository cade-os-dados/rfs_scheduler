import sqlite3

def execute(db_filename, command):
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute(command)

def commit(db_filename, command, argument, return_id = False):
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute(command, argument)
        conn.commit()
        if return_id:
            return cursor.lastrowid

class schedulerDatabase:

    @staticmethod
    def create_database(db_filename):
        create_db = '''
                CREATE TABLE IF NOT EXISTS executed_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                scheduled_time DATETIME NOT NULL,
                status TEXT NOT NULL
                )
                '''
        execute(db_filename,create_db)
    
    @staticmethod
    def commit_task(db_filename, task_name, scheduled_time, status):
        insert_db = '''
        INSERT INTO executed_tasks (task_name, scheduled_time, status) VALUES (?, ?, ?)
        '''
        commit(db_filename, insert_db, (task_name, scheduled_time, status))
    
    @staticmethod
    def create_process_database(db_filename):
        create_db = '''
                CREATE TABLE IF NOT EXISTS executed_processes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                process_name TEXT NOT NULL,
                free_memory_mb REAL,
                scheduled_time DATETIME NOT NULL,
                finished_time DATETIME,
                status TEXT NOT NULL,
                msg_error TEXT
                )
                '''
        execute(db_filename,create_db)
    
    @staticmethod
    def commit_process(db_filename, process_name, scheduled_time, free_memory_mb):
        insert_db = '''
        INSERT INTO executed_processes (process_name, scheduled_time, free_memory_mb, status) 
        VALUES (?, ?, ?, 'RUNNING')
        '''
        id_commit = commit(db_filename, insert_db, (process_name, scheduled_time, free_memory_mb), return_id=True)
        return id_commit

    @staticmethod
    def update_commit(db_filename, finished_time, status, msg_error, row_id):
        update_db = '''
        UPDATE executed_processes 
        SET finished_time = ?,
            status = ?,
            msg_error = ?
        WHERE id = ?
        '''
        commit(db_filename, update_db, (finished_time, status, msg_error, row_id))