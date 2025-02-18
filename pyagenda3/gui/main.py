import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from pyagenda3.database.ops import schedulerDatabase
from datetime import datetime
from pyagenda3.utils import relpath
from pyagenda3.gui.centralize import centralize_dimensions
from historico import abrir_historico, status_to_emoji
import re
from forms import NewEditProcessForm
from ping import *

DELAY_ATUALIZACAO = 500 # ms
DEBUG = False; PRINT = False;
MINUTO = 60; HORA = 60*MINUTO; DIA = 24*HORA; SEMANA = 7*DIA;
OPCOES_INTERVALO = ['12 horas', '1 dia', '1 semana']
REGEX = re.compile(r"(\d+)\s+segundos?")

def apply_custom_style(active: bool):
    # Customizando o estilo de seleção
    style = ttk.Style()
    if active:
        foreground, background = 'white', "#3399FF"
    else:
        foreground, background = 'white', "red"
    
    style.map("Treeview", 
            foreground=[('selected', foreground)],
            background=[('selected', background)])  # Cor rosa choque para seleção

def update_row_color(treeview, item_id, color):
    treeview.tag_configure(color, background=color)
    treeview.item(item_id, tags=(color,))

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
    return '1 segundo'  if dado == 1 else f'{dado} segundos'
            
def validar_intervalo(entrada):
    if entrada == '12 horas':
        return 12*HORA
    if entrada == '1 dia':
        return DIA
    if entrada == '1 semana':
        return SEMANA   
    try:
        return int(entrada)
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
        self.db.setup_last_status()
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
        self.spawn_activate_menu()

        # limitação de exibição do histórico
        self.limit_hist = tk.StringVar(self)
        self.limit_hist.set("20")

        self.refresh()

    def taskbar_icon(self):
        import ctypes
        # Change the taskbar icon
        myappid = 'your_company_name.your_product_name.subproduct.version'  # Choose a unique ID
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        photo = tk.PhotoImage(file = relpath(__file__, 'assets/calendario2.png'))
        self.wm_iconphoto(True, photo)

    def atualiza_processos(self):
        q2 = """
            SELECT 
                sp.process_id, process_name, args, cwd, 
                sp.scheduled_time, interval, last_status status, status_id
            FROM scheduled_processes sp
            LEFT JOIN last_status ON sp.process_id = last_status.process_id
        """

        self.processes = self.db.query(q2).fetchall()
        self.processes = list(map(lambda x: list(x), self.processes))
        for linha in self.processes:
            linha[-2] = status_to_emoji(linha[-2])
            linha[-3] = secs_to_string(linha[-3])
        # print(self.processes)

    def inativos(self):
        for i, row in enumerate(self.processes):
            if int(row[-1]) == 0:
                update_row_color(self.arvore, self.arvore.get_children()[i], "#FFC0CB")

    def edit_process(self):
        def set_text(widget, text):
            widget.delete(0,tk.END)
            widget.insert(0,text)
            return 
        def fmt_dtstr(dt_str: str, format='%d/%m/%Y'):
            return f"{dt_str[8:10]}/{dt_str[5:7]}/{dt_str[0:4]}"
        def tratar_intervalo(intervalo):
            find = REGEX.findall(intervalo)
            if find is not None and len(find) == 1:
                intervalo = find[0]
            return intervalo
            
        def edit_db(widget, event):
            if not validar_data(widget.dt.get()):
                messagebox.showerror("Entrada inválida", "Por favor, digite uma data no formato DIA/MES/ANO no campo de data.")
            else:
                intervalo = validar_intervalo(widget.i.get())
                dt_ = datetime.strptime(widget.dt.get(),"%d/%m/%Y")
                novos_dados = widget.nome.get(), widget.argumento.get(), widget.caminho.get(), dt_, intervalo
                self.db.edit_process(self.edit_id, *novos_dados)
                self.atualiza_processos()
                widget.form.destroy()
                self.update_treeview()

        dados = self.on_treeview_select(None)
        self.edit_id = dados[0]

        edit = NewEditProcessForm(self, 'Editar', lambda e: edit_db(edit, e))

        set_text(edit.nome, dados[1]); set_text(edit.argumento, dados[2]); set_text(edit.caminho, dados[3])
        edit.dt.set(fmt_dtstr(dados[4]))
        edit.i.set(tratar_intervalo(dados[5]))

    def new_form(self):
        def valida(widget, event):
            if not validar_data(widget.dt.get()):
                messagebox.showerror("Entrada inválida", "Por favor, digite uma data no formato DIA/MES/ANO no campo de data.")
            else:
                intervalo = validar_intervalo(widget.i.get())
                dt_ = datetime.strptime(widget.dt.get(),"%d/%m/%Y")
                self.db.insert_process(widget.nome.get(), widget.argumento.get(), widget.caminho.get(), dt_, intervalo)
                messagebox.showinfo('Sucesso!', 'Seu processo foi salvo com sucesso!')
                if not messagebox.askyesno("Continuar?", "Deseja inserir mais processos?"):
                    self.atualiza_processos()
                    widget.form.destroy()
                    self.update_treeview()

        new = NewEditProcessForm(self, 'Novo Processo', lambda e: valida(new, e))

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
        self.rcmenu.add_command(label="Desativar", command=self.desativar)
        self.rcmenu.add_separator()
        self.rcmenu.add_command(label="Excluir", command=self.delete_process)

    def ativar(self):
        q = self.db.handler.get('update_process_status_id.sql')
        print(q)
        self.db.commit(q, (1, self.get_process_id(),))

    def desativar(self):
        q = self.db.handler.get('update_process_status_id.sql')
        print(q)
        self.db.commit(q, (0, self.get_process_id(),))

    def get_process_status(self):
        return int(self.on_treeview_select(None)[-1])

    def spawn_activate_menu(self):
        self.acmenu = tk.Menu(self.arvore, tearoff=0)
        self.acmenu.add_command(label="Editar", command=self.edit_process)
        self.acmenu.add_command(label="Novo", command=self.new_form)
        self.acmenu.add_command(label="Rodar", command=self.rodar)
        self.acmenu.add_command(label="Histórico", command=self.abrir_historico)
        self.acmenu.add_command(label="Ativar", command=self.ativar)
        self.acmenu.add_separator()
        self.acmenu.add_command(label="Excluir", command=self.delete_process)

    def popup_rcmenu(self, event):
        if self.get_process_status():
            try:
                self.rcmenu.tk_popup(event.x_root, event.y_root)
            finally:
                self.rcmenu.grab_release()
        else:
            try:
                self.acmenu.tk_popup(event.x_root, event.y_root)
            finally:
                self.acmenu.grab_release()

    def on_treeview_select(self, event):
        selected_item = self.arvore.selection()
        item_text = self.arvore.item(selected_item, 'values')
        if PRINT:
            print(f"Linha selecionada: {item_text}, item: {selected_item}")
        try:
            apply_custom_style(bool(int(item_text[-1])))
        except:
            pass
        return item_text

    def update_treeview(self):
        # Remover todos os itens existentes
        for item in self.arvore.get_children():
            self.arvore.delete(item)
        
        # Inserir novos itens
        for linha in self.processes:
            self.arvore.insert("", "end", values=linha)

    def atualiza_treeview(self):
        self.atualiza_processos()
        # Salvar a seleção atual com base em um valor único (por exemplo, a primeira coluna)
        selected_values = [self.arvore.item(item)["values"][0] for item in self.arvore.selection()]

        # Deletar tudo
        for item in self.arvore.get_children():
            self.arvore.delete(item)
        value_to_id = {}
        for tupla in self.processes:
            item_id = self.arvore.insert("", "end", values=tupla)
            value_to_id[tupla[0]] = item_id  # Mapeia o valor único para o novo ID

        ignore = False
        # Restaurar a seleção com base nos valores únicos mapeados
        for value in selected_values:
            if value in value_to_id:
                if not ignore:
                    focar = value_to_id[value]
                    ignore = True
                self.arvore.selection_add(value_to_id[value])
        if ignore:
            self.arvore.focus(focar)
        self.inativos()

    def refresh(self):
        self.atualiza_treeview()
        self.arvore.after(DELAY_ATUALIZACAO, self.refresh)

    def make_treeview(self, master):
        cols = [f'col{i}' for i in range(1,8)]
        self.arvore = ttk.Treeview(master, columns=cols, show="headings")
        for col, name in zip(cols, ["id", "Nome", "Argumentos", "Caminho", "Data/Hora Agendamento", "Intervalo de Execuções", "Últimos Status"]):
            self.arvore.heading(col, text=name,anchor='center')
            self.arvore.column(col, anchor='center')
        
        # Cria a Scrollbar horizontal
        scrollbar_x = ttk.Scrollbar(master, orient="horizontal", command=self.arvore.xview)
        self.arvore.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Insere os dados nas colunas
        for linha in self.processes:
            self.arvore.insert("", "end", values=linha)
    
        self.arvore.pack(expand=True, fill=tk.Y)
        self.arvore.bind('<<TreeviewSelect>>', self.on_treeview_select)
        self.arvore.bind('<Button-3>', self.popup_rcmenu)

        display = cols[1:]
        self.arvore["displaycolumns"] = display
        self.inativos()

App.list_ping_server = list_ping_server
App.show_servers = show_servers
App.teste_conexao = teste_conexao
App.abrir_historico = abrir_historico

if __name__ == '__main__':
    root = App()
    root.mainloop()