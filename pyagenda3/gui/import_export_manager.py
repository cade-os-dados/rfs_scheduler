import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os, json
from tkinter.messagebox import showinfo, showerror, showwarning

class ImportExportManager:
    info = ('process_name',
        'args',
        'cwd',
        'scheduled_time',
        'interval'
    )

    def __write__(self, j: dict, path: str = 'config.json'):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(j, f, indent=4)

    def __read__(self, path: str = 'config.json'):
        with open(path, "r", encoding="utf-8") as f:
            j = json.load(f)
        return j

    def to_dict(self, data: list):
        j = [dict(zip(self.info, data[i][1:-1])) for i in range(len(data))]
        return j

    def importar(self, app):
        file = filedialog.askopenfilename(parent=app)
        dicio = self.__read__(file)
        # adicionar funcionalidade de selecionar os processos do json

        # verificar se já existe
        query = "SELECT process_name,args,cwd,scheduled_time,interval FROM scheduled_processes"
        processes = app.db.query(query).fetchall()

        for processo in dicio:
            data = tuple(processo.values())
            if data in processes:
                showwarning('Processo já existe!', 'Processo: {} já existe'.format(data[0]))
            else:
                app.db.insert_process(*data)

    def export(self, app):
        query = "SELECT * FROM scheduled_processes"
        processes = app.db.query(query).fetchall()
        directory = filedialog.askdirectory(parent=app)
        app.deiconify()
        app.focus_force()
        if directory:
            path = os.path.join(directory,'config.json')
            try:
                self.__write__(self.to_dict(processes),path)
                showinfo('Sucesso!','Seus processos foram exportados com sucesso!')
            except Exception as e:
                showerror('Erro!', f'Falha ao exportar processos... Detalhes: {e}')