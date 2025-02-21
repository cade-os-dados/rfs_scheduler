from os.path import join, dirname
import time, threading

class RelPath:
    def __init__(self, file: str):
        self.main = dirname(file)
    
    def get(self, rel: str):
        return join(self.main, rel) 

relpath = lambda file, x: join(dirname(file),x)



class ThreadLoop:
    def __init__(self):
        self.threads = []
        self.running = True
        self.stoppers = []
       
    def loop(self, fn, delay):
        while self.running:
            fn()
            time.sleep(delay)

    def add(self, fn, delay = -1):
        if delay > 0:
            thread = threading.Thread(target=lambda: self.loop(fn,delay))
        else:
            thread = threading.Thread(target=fn)
        self.threads.append(thread)

    def add_stopper(self, stopper):
        self.stoppers.append(stopper)

    def start(self):
        for t in self.threads:
            t.start()

    def stop(self):
        self.running = False
        for stopper in self.stoppers:
            stopper.running=False
        for t in self.threads:
            t.join()

    def mainloop(self):
        try:
            while any(t.is_alive() for t in self.threads):
                for t in self.threads:
                    t.join(timeout=1)
        except KeyboardInterrupt:
            print("Interrupção do teclado recebida. Encerrando...")
            self.stop()
            print("Encerrado com sucesso")
            return True