import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from pyagenda3.gui.centralize import spawn_on_mouse

class Historico:    
    def __init__(self,
        scheduled_time: str,
        duration: str,
        status: str,
        msg_error: str
    ):
        if status == 'COMPLETED':
            status = "✅"
        else:
            status = "❌"
        self.values = (scheduled_time[:19], duration, status, msg_error[:200])


def abrir_historico(self, process_name):
    query = """
        SELECT scheduled_time, strftime('%s', finished_time) - strftime('%s',scheduled_time) AS duration, status, msg_error
        FROM executed_processes 
        WHERE process_name = ? 
        ORDER BY scheduled_time DESC
    """
    last_processes = self.db.query(query, (process_name, ))
    top = tk.Toplevel(self)
    spawn_on_mouse(self, top, (800,600))
    top.title('Histórico')
    top.focus_force()

    frame = tk.Frame(top)
    frame.pack()
    
    cols = [f'col{i}' for i in range(1,5)]
    tree = ttk.Treeview(frame, columns=cols, show="headings", style="Treeview")
    for col, name in zip(cols, ["scheduled_time", "duration", "status", "msg_error"]):
        tree.heading(col, text=name, anchor="center")
        tree.column(col,anchor='center')

    
    scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.pack(side=tk.RIGHT,fill=tk.Y)

    for tupla in last_processes:
        hist = Historico(*tupla)
        tree.insert("","end", values=hist.values)
    tree.pack(side=tk.LEFT)
