import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from pyagenda3.gui.features.centralize import spawn_on_mouse
from pyagenda3.gui.features.treeview_refresh import TreeViewRefresher
from pyagenda3.gui.features.hider import TreeviewHider

DELAY_ATUALIZACAO_HISTORICO = 900 # ms

HIST_QUERY = """
    SELECT scheduled_time, strftime('%s', finished_time) - strftime('%s',scheduled_time) AS duration, status, msg_error
    FROM executed_processes 
    WHERE process_id = ? 
    ORDER BY scheduled_time ASC
    -- LIMIT ?
"""

PROCESS_NAME = "SELECT process_name FROM scheduled_processes WHERE process_id = ?"

def status_to_emoji(status):
    if status == "COMPLETED":
        status = "✅"
    elif status == "FAILED":
        status = "❌"
    elif status == "WAITING":
        status = "🕓" # 🕓 ⏳
    elif status == "RUNNING":
        status = "⭮" # ⏭️ ↺ ⭯ ⇄ ↻ ⭮ 💫 ↺↻⟲⟳⭯⭮↺↻⥀⥁↶↷⮌⮍⮎⮏⤻⤸⤾⤿⤺⤼⤽⤹🗘⮔⤶⤷⃕↻
    else:
        status = ""
    return status

class Historico:    
    def __init__(self,
        scheduled_time: str,
        duration: str,
        status: str,
        msg_error: str
    ):
        status = status_to_emoji(status)
        if type(msg_error) == str:
            msg_error = msg_error[:200]
        self.values = (scheduled_time[:19], duration, status, msg_error)

def dados_historico(master, process_id):
    #last_processes = master.db.query(HIST_QUERY, (process_id, master.limit_hist.get(), ))
    last_processes = master.db.query(HIST_QUERY, (process_id, ))
    new_values = []
    for tupla in last_processes:
        hist = Historico(*tupla)
        new_values.append(hist.values)
    return new_values

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
    
    cols = [f'col{i}' for i in range(1,5)]
    tree = ttk.Treeview(frame_child1, columns=cols, show="headings", style="Treeview")
    for col, name in zip(cols, ["scheduled_time", "duration", "status", "msg_error"]):
        tree.heading(col, text=name, anchor="center")
        tree.column(col,anchor='center')

    scrollbar_y = ttk.Scrollbar(frame_child1, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.pack(side=tk.RIGHT,fill=tk.Y)

    tree.pack(side=tk.LEFT)
    hider = TreeviewHider(tree, self.limit_hist)
   
    ttk.Button(
        frame_child2, text='aplicar',
        command=lambda: hider.hide_rows()
    ).pack(side=tk.LEFT, padx=10)

    refresh = TreeViewRefresher(tree, 300, False)
    refresh.run(lambda: dados_historico(self, process_id))
    hider.hide_rows()

class HistoricoGeral:

    def __init__(self, app):
        self.app = app

    def update(self):
        data = self.app.db.query("""
            SELECT ep.executed_id,
                sp.process_name,
                CONCAT(CAST(CAST(ep.free_memory_mb AS INTEGER) As VARCHAR), ' MB'),
                ep.scheduled_time,
                Cast ((
                    JulianDay(ep.finished_time) - JulianDay(ep.scheduled_time)
                ) * 24 * 60 * 60 As Integer) AS execution_time,
                ep.status,
                ep.msg_error
            FROM executed_processes ep
            LEFT JOIN scheduled_processes sp ON ep.process_id = sp.process_id
        """).fetchall()

        data = [*map(lambda x: list(x),data)]

        for i in range(len(data)):
            data[i][-2] = status_to_emoji(data[i][-2])
            if data[i][-1] is not None and len(data[i][-1]) > 0:
                data[i][-1] = data[i][-1][:20]+'...'
        return data

    def on_treeview_select(self, event):
        selected_item = self.tree.selection()
        item_text = self.tree.item(selected_item, 'values')
        try:
            id = item_text[0]
            msg = self.app.db.query('SELECT msg_error FROM executed_processes WHERE executed_id = ?', (id,)).fetchone()
            if msg:
                msg = msg[0]
                if msg == None:
                    msg=''
            if msg != '':
                new_window = tk.Toplevel(self.app)
                new_window.title('Mensagem de Erro')
                spawn_on_mouse(self.app,new_window, (800,360))
                txt = tk.Text(new_window)
                txt.pack(fill='both',expand=True)
                txt.insert(tk.END,msg)
                new_window.focus()

                bloquear_edicao = lambda event: "break"
                txt.bind("<Key>", bloquear_edicao)
                txt.bind("<Button-2>", bloquear_edicao)  # botão do meio
                txt.bind("<Button-3>", bloquear_edicao)  # botão direito (em alguns sistemas)

                # Permite seleção e cópia
                txt.config(cursor="xterm")  # mantém o cursor de texto

        except Exception as e:
            print(e)

    def run(self,top):
        frame = tk.Frame(top)
        frame.pack()

        frame_child1 = tk.Frame(frame); frame_child2 = tk.Frame(frame)
        frame_child1.pack(side=tk.TOP, pady=10); frame_child2.pack(side=tk.TOP, pady=10)

        ttk.Label(frame_child2,text='Limitar linhas: ').pack(side=tk.LEFT)
        spin = ttk.Spinbox(frame_child2, from_=5,to=100, justify='center', width=10, textvariable=self.app.limit_hist)
        spin.pack(side=tk.LEFT)
        
        cols = [f'col{i}' for i in range(1,8)]
        tree = ttk.Treeview(frame_child1, columns=cols, show="headings", style="Treeview")
        for col, name in zip(cols, [
            "executed_id","process_name","free_memory_mb",
            "scheduled_time","execution_time","status","msg_error"
        ]):
            tree.heading(col, text=name, anchor="center")
            tree.column(col,anchor='center',width=int(1280/7))

        scrollbar_y = ttk.Scrollbar(frame_child1, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=tk.RIGHT,fill=tk.Y)

        tree.pack(side=tk.LEFT)
        hider = TreeviewHider(tree, self.app.limit_hist)
    
        ttk.Button(
            frame_child2, text='aplicar',
            command=lambda: hider.hide_rows()
        ).pack(side=tk.LEFT, padx=10)

        refresh = TreeViewRefresher(tree, 300, False)
        refresh.run(lambda: self.update())
        hider.hide_rows()
        self.tree = tree
        # self.tree.bind('<<TreeviewSelect>>', self.on_treeview_select)
        self.tree.bind('<Double-1>', self.on_treeview_select)
