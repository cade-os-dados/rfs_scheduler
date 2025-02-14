import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from pyagenda3.database.ops import schedulerDatabase
from datetime import datetime
from pyagenda3.utils import relpath
from pyagenda3.gui.centralize import toplevel_centralize, centralize_dimensions, spawn_on_mouse
from historico import abrir_historico
from tkcalendar import DateEntry

from ping import *

DEBUG = True
MINUTO = 60; HORA = 60*MINUTO; DIA = 24*HORA; SEMANA = 7*DIA;
OPCOES_INTERVALO = ['12 horas', '1 dia', '1 semana']

def validar_data(data_str):
    formato ="%d/%m/%Y" # Formato de data :dia/mês/ano
    try:
        data_valida=datetime.strptime(data_str,formato)
        return True
    except ValueError:
        return False

def secs_to_string(dado):
    try:
        dado = int(dado)
    except:
        pass
    if dado == 12*HORA:
        return '12 horas'
    if dado == DIA:
        return '1 dia'
    if dado == SEMANA:
        return '1 semana'
    else:
        return dado

def validar_intervalo(entrada):
    if entrada == '12 horas':
        entrada = 12*HORA
    elif entrada == '1 dia':
        entrada = DIA
    else:
        entrada = SEMANA
    try:
        numero = int(entrada)
        return numero
    except ValueError:
        messagebox.showerror("Entrada inválida", "Por favor, digite um número inteiro no campo intervalo.")
        return False

def get_sizes(root):
    root.update()
    return root.winfo_width(), root.winfo_height() 

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Processos")
        # geometria
        w,h = self.winfo_screenwidth(), self.winfo_screenheight()
        w_, h_ = 1280, 720
        pos = centralize_dimensions(w,h,0,0,w_,h_)
        self.geometry(f"{w_}x{h_}+{pos[0]}+{pos[1]}")
        # fonte
        self.mainfont = font.Font(family='Helvetica',size=14, weight='bold')
        self.db = schedulerDatabase('scheduler.db')
        self.atualiza_processos()
                
        self.taskbar_icon()
        self.mainframe = tk.Frame(self)
        self.mainframe.pack()

        self.frame2_title = tk.Frame(self.mainframe)
        self.frame2_title.grid(row=0,column=0)
        tk.Label(self.frame2_title, text='Listagem de Processos', font=self.mainfont,pady=20).pack()

        self.frame2 = tk.Frame(self.mainframe)
        self.frame2.grid(row=1,column=0)
        self.make_treeview(self.frame2)

        self.show_servers()
        self.spawn_rcmenu()

        # limitação de exibição do histórico
        self.limit_hist = tk.StringVar(self)
        self.limit_hist.set("20")

    def taskbar_icon(self):
        import ctypes
        # Change the taskbar icon
        myappid = 'your_company_name.your_product_name.subproduct.version'  # Choose a unique ID
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        photo = tk.PhotoImage(file = relpath(__file__, 'assets/calendario2.png'))
        self.wm_iconphoto(True, photo)

    def atualiza_processos(self):
        self.processes = self.db.query('SELECT * FROM scheduled_processes')

    def edit_process(self):
        def set_text(widget, text):
            widget.delete(0,tk.END)
            widget.insert(0,text)
            return 
        def fmt_dtstr(dt_str: str, format='%d/%m/%Y'):
            return f"{dt_str[8:10]}/{dt_str[5:7]}/{dt_str[0:4]}"

        dados = self.on_treeview_select(None)
        self.edit_id = dados[0]

        self.edit = tk.Toplevel(self)
        self.edit.transient(self)
        self.edit.title("Editar")
        spawn_on_mouse(self, self.edit, (300,160))
        self.edit_frame1 = tk.Frame(self.edit, pady=5)
        self.edit_frame2 = tk.Frame(self.edit, pady=5)
        self.edit_frame1.pack()
        self.edit_frame2.pack()
    
        self.nome = self.label_entry(self.edit_frame1, 'Nome', 0); set_text(self.nome, dados[1])
        self.argumento = self.label_entry(self.edit_frame1, 'Argumento', 1); set_text(self.argumento, dados[2])
        self.caminho = self.label_entry(self.edit_frame1, 'Caminho', 2); set_text(self.caminho, dados[3])
        # date entry
        tk.Label(self.edit_frame1, text='Data: ',width=10, anchor='w').grid(row=3,column=0)
        self.dt=tk.StringVar(self)
        DateEntry(self.edit_frame1,selectmode='day',textvariable=self.dt,locale='pt_br',width=22).grid(row=3,column=1)
        self.dt.set(fmt_dtstr(dados[4]))
        # interval
        tk.Label(self.edit_frame1, text='Intervalo: ',width=10, anchor='w').grid(row=4,column=0)
        self.i = ttk.Combobox(self.edit_frame1,values=OPCOES_INTERVALO, width=22)
        self.i.grid(row=4,column=1); # set_text(self.i, secs_to_string(dados[5]))
        new_data = secs_to_string(dados[5])
        print(new_data)
        self.i.set(new_data)
        
       
        # self.i = self.label_entry(self.edit_frame1, 'Interval', 4); set_text(self.i, dados[5])
        ok = tk.Button(self.edit_frame2, text='OK',command=self.edit_db,width=10)
        ok.pack()
        self.edit.focus_force()

    def edit_db(self):
        # Testando a função
        if not validar_data(self.dt.get()):
            messagebox.showerror("Entrada inválida", "Por favor, digite uma data no formato DIA/MES/ANO no campo de data.")
        else:
            intervalo = validar_intervalo(self.i.get())
            dt_ = datetime.strptime(self.dt.get(),"%d/%m/%Y")
            novos_dados = self.nome.get(), self.argumento.get(), self.caminho.get(), dt_, intervalo
            self.db.edit_process(self.edit_id, *novos_dados)
            self.atualiza_processos()
            self.edit.destroy()
            self.update_treeview()

    def delete_process(self):
        selected = self.arvore.selection()
        if selected:
            item_text = self.arvore.item(selected, 'values')
            confirm = messagebox.askyesno("Confirmação", f"Tem certeza de que deseja excluir o processo: {item_text[1]}?")
            if confirm:
                self.arvore.delete(selected)
                if not DEBUG:
                    self.db.delete_process(item_text[0])
        else:
            messagebox.showwarning("Aviso", "Selecione um processo para deletar")

    def label_entry(self, master, name: str, grid_row: int):
        labelText=tk.StringVar()
        labelText.set(name)
        label = tk.Label(master, textvariable=labelText, width=10, anchor='w')
        entry = tk.Entry(master, width=25)
        label.grid(row=grid_row,column=0)
        entry.grid(row=grid_row,column=1)
        return entry

    def valida(self):
        # Testando a função
        if not validar_data(self.dt_new.get()):
            messagebox.showerror("Entrada inválida", "Por favor, digite uma data no formato DIA/MES/ANO no campo de data.")
        else:
            intervalo = validar_intervalo(self.i.get())
            dt_ = datetime.strptime(self.dt_new.get(),"%d/%m/%Y")
            self.db.insert_process(self.nome.get(), self.argumento.get(), self.caminho.get(), dt_, intervalo)
            messagebox.showinfo('Sucesso!', 'Seu processo foi salvo com sucesso!')
            if not messagebox.askyesno("Continuar?", "Deseja inserir mais processos?"):
                self.atualiza_processos()
                self.mpopup.destroy()
                self.update_treeview()

    def new_form(self):
        self.mpopup = tk.Toplevel(self)
        self.mpopup.transient(self)
        self.mpopup.title("New Window")
        self.mpopup_frame1 = tk.Frame(self.mpopup, pady=5)
        self.mpopup_frame2 = tk.Frame(self.mpopup, pady=5)
        self.mpopup_frame1.pack()
        self.mpopup_frame2.pack()

        # sets the geometry of toplevel
        spawn_on_mouse(self, self.mpopup, dim = (300,180))
    
        # A Label widget to show in toplevel
        self.nome = self.label_entry(self.mpopup_frame1, 'Nome', 0)
        self.argumento = self.label_entry(self.mpopup_frame1, 'Argumento', 1)
        self.caminho = self.label_entry(self.mpopup_frame1, 'Caminho', 2)
        tk.Label(self.mpopup_frame1, text='Data: ',width=10, anchor='w').grid(row=3,column=0)
        self.dt_new=tk.StringVar()
        entry = DateEntry(self.mpopup_frame1,selectmode='day',textvariable=self.dt_new,locale='pt_br',width=22)
        entry.grid(row=3,column=1); entry.delete(0,"end")
        # self.i = self.label_entry(self.mpopup_frame1, 'Interval', 4)
        tk.Label(self.mpopup_frame1, text='Intervalo: ',width=10, anchor='w').grid(row=4,column=0)
        self.i = ttk.Combobox(self.mpopup_frame1,values=OPCOES_INTERVALO, width=22)
        self.i.grid(row=4,column=1)
        # self.i = self.label_entry(self.mpopup_frame1, 'Interval', 4)
        ok = tk.Button(self.mpopup_frame2, text='OK',command=self.valida,width=10)
        ok.pack()

    def pop_up(self, event):
        self.popup_window = tk.Toplevel(self)
        self.popup_window.title("New Window")
    
        # sets the geometry of toplevel
        self.popup_window.geometry("200x200")
    
        # A Label widget to show in toplevel
        tk.Label(self.popup_window, text ="This is a new window").pack()

    def rodar(self):
        process_id = self.get_process_id()
        if not self.db.waiting_or_running_process(process_id):
            self.db.commit_process(process_id, datetime.now(), 'WAITING')

    def get_process_id(self):
        return int(self.on_treeview_select(None)[0])

    def spawn_rcmenu(self):
        'right click menu'
        self.rcmenu = tk.Menu(self.arvore, tearoff=0)
        self.rcmenu.add_command(label="Editar", command=self.edit_process)
        self.rcmenu.add_command(label="Novo", command=self.new_form)
        self.rcmenu.add_command(label="Rodar", command=self.rodar)
        self.rcmenu.add_command(label="Histórico", command=self.abrir_historico)
        self.rcmenu.add_separator()
        self.rcmenu.add_command(label="Excluir", command=self.delete_process)

    def popup_rcmenu(self, event):
        try:
            self.rcmenu.tk_popup(event.x_root, event.y_root)
        finally:
            self.rcmenu.grab_release()

    def on_treeview_select(self, event):
        selected_item = self.arvore.selection()
        item_text = self.arvore.item(selected_item, 'values')
        print(f"Linha selecionada: {item_text}, item: {selected_item}")
        return item_text

    def update_treeview(self):
        # Remover todos os itens existentes
        for item in self.arvore.get_children():
            self.arvore.delete(item)
        
        # Inserir novos itens
        for i, linha in enumerate(self.processes):
            self.arvore.insert("", "end", values=linha)
    
    def make_treeview(self, master):
        cols = [f'col{i}' for i in range(1,7)]
        self.arvore = ttk.Treeview(master, columns=cols, show="headings")
        for col, name in zip(cols, ["id", "Nome", "Argumentos", "Caminho", "Data/Hora Agendamento", "Intervalo de Execuções (seg.)"]):
            self.arvore.heading(col, text=name,anchor='center')
            self.arvore.column(col, anchor='center')
        
        # Cria a Scrollbar horizontal
        scrollbar_x = ttk.Scrollbar(master, orient="horizontal", command=self.arvore.xview)
        self.arvore.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Insere os dados nas colunas
        for i, linha in enumerate(self.processes):
            self.arvore.insert("", "end", values=linha)
    
        self.arvore.pack(expand=True, fill=tk.Y)
        self.arvore.bind('<<TreeviewSelect>>', self.on_treeview_select)
        self.arvore.bind('<Double-1>', self.pop_up)
        self.arvore.bind('<Button-3>', self.popup_rcmenu)

        display = cols[1:]
        self.arvore["displaycolumns"] = display

App.list_ping_server = list_ping_server
App.show_servers = show_servers
App.teste_conexao = teste_conexao
App.abrir_historico = abrir_historico

if __name__ == '__main__':
    root = App()
    root.mainloop()