import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from pyagenda3.gui.centralize import spawn_on_mouse

DELAY_ATUALIZACAO = 1000 # ms

HIST_QUERY = """
    SELECT scheduled_time, strftime('%s', finished_time) - strftime('%s',scheduled_time) AS duration, status, msg_error
    FROM executed_processes 
    WHERE process_id = ? 
    ORDER BY scheduled_time DESC
    LIMIT ?
"""

PROCESS_NAME = "SELECT process_name FROM scheduled_processes WHERE process_id = ?"

class Historico:    
    def __init__(self,
        scheduled_time: str,
        duration: str,
        status: str,
        msg_error: str
    ):
        if status == "COMPLETED":
            status = "✅"
        elif status == "FAILED":
            status = "❌"
        elif status == "WAITING":
            status = "🕓" # 🕓 ⏳
        elif status == "RUNNING":
            status = "⭮" # ⏭️ ↺ ⭯ ⇄ ↻ ⭮ 💫 ↺↻⟲⟳⭯⭮↺↻⥀⥁↶↷⮌⮍⮎⮏⤻⤸⤾⤿⤺⤼⤽⤹🗘⮔⤶⤷⃕↻
        if type(msg_error) == str:
            msg_error = msg_error[:200]
        self.values = (scheduled_time[:19], duration, status, msg_error)

def atualizar_limite_treeview_historico(master, tree, process_id):
    # Salvar a seleção atual com base em um valor único (por exemplo, a primeira coluna)
    selected_values = [tree.item(item)["values"][0] for item in tree.selection()]

    last_processes = master.db.query(HIST_QUERY, (process_id, master.limit_hist.get(), ))
    # Deletar tudo
    for item in tree.get_children():
        tree.delete(item)
    # Inserir tudo e mapear valores únicos para novos IDs
    value_to_id = {}
    for tupla in last_processes:
        hist = Historico(*tupla)
        item_id = tree.insert("", "end", values=hist.values)
        value_to_id[hist.values[0]] = item_id  # Mapeia o valor único para o novo ID

    # Restaurar a seleção com base nos valores únicos mapeados
    for value in selected_values:
        if value in value_to_id:
            tree.selection_add(value_to_id[value])

def refresh_historico(master, tree, process_id):
    atualizar_limite_treeview_historico(master, tree, process_id)
    tree.after(DELAY_ATUALIZACAO, lambda: refresh_historico(master, tree, process_id))

def abrir_historico(self):
    process_id = self.get_process_id()

    top = tk.Toplevel(self)
    spawn_on_mouse(self, top, (800,360))
    top.title('Histórico')
    top.focus_force()

    frame = tk.Frame(top)
    frame.pack()

    process_nm = self.db.query(PROCESS_NAME, (process_id,)).fetchone()[0]
    frame_child0 = tk.Frame(frame); frame_child0.pack(side=tk.TOP, pady=10)
    ttk.Label(frame_child0, text='Histórico do Processo: {}'.format(process_nm), font=self.mainfont).pack()

    frame_child1 = tk.Frame(frame); frame_child2 = tk.Frame(frame)
    frame_child1.pack(side=tk.TOP, pady=10); frame_child2.pack(side=tk.TOP, pady=10)

    ttk.Label(frame_child2,text='Limitar linhas: ').pack(side=tk.LEFT)
    spin = ttk.Spinbox(frame_child2, from_=5,to=100, justify='center', width=10, textvariable=self.limit_hist)
    spin.pack(side=tk.LEFT)
    ttk.Button(
        frame_child2, text='aplicar',
        command=lambda: atualizar_limite_treeview_historico(self, tree, process_id)
    ).pack(side=tk.LEFT, padx=10)
    
    cols = [f'col{i}' for i in range(1,5)]
    tree = ttk.Treeview(frame_child1, columns=cols, show="headings", style="Treeview")
    for col, name in zip(cols, ["scheduled_time", "duration", "status", "msg_error"]):
        tree.heading(col, text=name, anchor="center")
        tree.column(col,anchor='center')

    scrollbar_y = ttk.Scrollbar(frame_child1, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.pack(side=tk.RIGHT,fill=tk.Y)

    atualizar_limite_treeview_historico(self, tree, process_id)
    tree.pack(side=tk.LEFT)
    tree.after(DELAY_ATUALIZACAO, lambda: refresh_historico(self,tree,process_id))
