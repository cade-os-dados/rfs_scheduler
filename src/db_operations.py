import sqlite3

def execute(db_filename, command):
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute(command)

def commit(db_filename, command, argument):
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute(command, argument)
        conn.commit()

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