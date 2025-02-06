import os
from glob import glob

class SQLFileHandler:

    def __init__(self, dir_path: str):
        self.dir = dir_path
    
    def __join__(self, filename):
        return os.path.join(self.dir, filename)

    def open(self, file):
        with open(file,'r') as f:
            data = f.read()
        return data

    def get(self, sql_filename: str):
        file = self.__join__(sql_filename)
        return self.open(file) if os.path.exists(file) else None
    
    def list_all(self):
        return glob(os.path.join(self.dir, '*.sql'))
    
    def open_all(self):
        return [self.open(f) for f in self.list_all()]