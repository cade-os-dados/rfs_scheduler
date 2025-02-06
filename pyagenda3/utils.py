from os.path import join, dirname

class RelPath:
    def __init__(self, file: str):
        self.main = dirname(file)
    
    def get(self, rel: str):
        return join(self.main, rel) 

relpath = lambda file, x: join(dirname(file),x)