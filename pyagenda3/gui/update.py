from pyagenda3.database.ops import schedulerDatabase

db = schedulerDatabase('scheduler.db')
db.execute("UPDATE executed_processes SET status = 'KILLED' WHERE status IN ('WAITING','RUNNING')")