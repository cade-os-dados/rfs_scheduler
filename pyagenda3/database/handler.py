import os
from glob import glob

class SQLFileHandler:

    'Facilita a integração com pasta de arquivos .sql'

    def __init__(self, dir_path: str):
        self.dir = dir_path
    
    def __join__(self, filename):
        return os.path.join(self.dir, filename)

    def open(self, file):
        with open(file,'r') as f:
            data = f.read()
        return data

    def get(self, sql_filename: str, in_: int = -1):
        file = self.__join__(sql_filename)
        opened_file = self.open(file) if os.path.exists(file) else None
        return opened_file if not in_ >= 0 else opened_file.format(','.join('?' for _ in range(in_)))
    
    def list_all(self, pattern='*.sql'):
        return glob(os.path.join(self.dir, pattern))
    
    def open_all(self, pattern='*.sql'):
        return [self.open(f) for f in self.list_all(pattern)]