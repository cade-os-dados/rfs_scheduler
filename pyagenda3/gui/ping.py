import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from pyagenda3.services.ping import PingClient
from pyagenda3.gui.centralize import toplevel_centralize

def combobox_defocus(combobox: ttk.Combobox) -> None:
    def defocus(event):
        event.widget.master.focus_set()

    combobox.bind("<FocusIn>",defocus)

def list_ping_server(self):
    q = self.db.handler.get('select_ping_servers.sql')
    return self.db.query(q)

def teste_conexao(self):

    # new_window = tk.Toplevel(self)
    new_window = toplevel_centralize(self, 300, 150)
    new_window.title("Teste de conexão")

    # Criando a barra de progresso indeterminada
    tk.Label(new_window, text='Testando conexão...').pack(side=tk.TOP, pady=10)

    progress_bar = ttk.Progressbar(new_window, mode='indeterminate',length=400)
    progress_bar.pack(padx=10, pady=10)
    progress_bar.start(10)

    self.t = 1
    def pingar():
        print(f'Tentativa...{self.t}')
        self.t+=1
        if ping.rcv2(server):
            messagebox.showinfo('Conexão Estabelecida', f'O servidor {server} está disponível!')
            new_window.destroy()
        else:
            new_window.after(500, pingar)
    def destruir():
        messagebox.showerror('Erro', 'Não foi possível estabelecer conexão!')
        new_window.destroy()

    ping = PingClient('scheduler.db')
    # server = self.servers[0].cget('text')
    server = self.chosen_server.get()
    ping.ping(server)
    new_window.after(500,pingar)
    new_window.after(10000, destruir)
    new_window.focus_force()
    
def show_servers(self):
    self.frame3 = tk.Frame(self.mainframe)
    self.frame4 = tk.Frame(self.mainframe)
    self.frame3.grid(row=2,column=0)
    self.frame4.grid(row=3,column=0)
    tk.Label(self.frame3, text='Servidores',font=self.mainfont).pack()



    
    self.chosen_server = tk.StringVar() 
    self.servers = ttk.Combobox(self.frame3, width = 27, 
                                textvariable = self.chosen_server,
                                state='readonly')
    self.servers['values'] = self.list_ping_server().fetchall()
    if len(self.servers['values']):
        self.servers.pack(pady=10)
        combobox_defocus(self.servers)
        tk.Button(self.frame4, text='verificar conexão', command=self.teste_conexao, width=20).pack(side=tk.BOTTOM)
    else:
        tk.Label(self.frame4, text='Nenhum servidor ativo encontrado').pack(pady=10)
  
    # self.servers = []
    # for server in self.list_ping_server():
    #     check = tk.Checkbutton(self.frame3, text=server)
    #     check.pack(side=tk.TOP)
    #     self.servers.append(check)
    #     print(self.servers)
