import socket, threading
from time import sleep
from pyagenda3.database.ops import schedulerDatabase
from pyagenda3.database.handler import SQLFileHandler
from pyagenda3.utils import relpath

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

class PingService:

    def __init__(self, db_filename: str, interval: int = 5):
        self.handler = SQLFileHandler(relpath(__file__,'../database/sql'))
        self.db = schedulerDatabase(db_filename)
        self.ip = get_ip()
        self.thread = threading.Thread(target=self.run)
        self.interval = interval
        self.setup()
        
    def setup(self):
        server = self.db.query('SELECT COUNT(*) FROM ping_server WHERE server_ip = ?', (self.ip,)).fetchone()
        if server[0] == 0:
            self.db.commit(self.handler.get('insert_ping_server.sql'), (self.ip, 'VM', self.db.check_memory_mb(),))
        else:
            self.db.commit(self.handler.get('update_ping_server.sql'), ('ACTIVE', self.db.check_memory_mb(), self.ip,))

    def check_ping(self):
        consulta = 'SELECT ping_status FROM ping_server WHERE server_ip = ?'
        ping = self.db.query(consulta, (self.ip,)).fetchone()
        if ping is not None and ping[0] == 'WAITING':
            self.db.commit(self.handler.get('update_ping_server.sql'), ('ACTIVE', self.db.check_memory_mb(), self.ip, ))

    def run(self):
        while True:
            print('Cheking...')
            self.check_ping()
            sleep(self.interval)


class PingClient:

    def __init__(self, db: str, max_wait_in_seconds: int = 5):
        self.db = schedulerDatabase(db)
        self.handler = SQLFileHandler(relpath(__file__,'../database/sql'))
        self.max_wait_in_seconds = max_wait_in_seconds
        
    def ping(self, server_ip):
        self.db.commit(self.handler.get('update_ping_server.sql'), ('WAITING', None, server_ip,))

    def rcv(self, server_ip):
        c = 0
        consulta = 'SELECT ping_status FROM ping_server WHERE server_ip = ?'
        ping = self.db.query(consulta, (server_ip,)).fetchone()
        while not ping[0] == 'ACTIVE':
            c+=1
            ping = self.db.query(consulta, (server_ip,)).fetchone()
            sleep(1)
            if c >= self.max_wait_in_seconds:
                return False
        return True
    
    def rcv2(self,server_ip):
        consulta = 'SELECT ping_status FROM ping_server WHERE server_ip = ?'
        ping = self.db.query(consulta, (server_ip,)).fetchone()
        return ping[0] == 'ACTIVE'
        