import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pyagenda3.database.ops import schedulerDatabase
from datetime import datetime

DEBUG = True

def validar_data(data_str):
    formato ="%d/%m/%Y" # Formato de data :dia/mês/ano
    try:
        data_valida=datetime.strptime(data_str,formato)
        return True
    except ValueError:
        return False
    
def validar_inteiro(entrada):
    try:
        numero = int(entrada)
        return True
    except ValueError:
        messagebox.showerror("Entrada inválida", "Por favor, digite um número inteiro no campo intervalo.")
        return False

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Processos")
        self.geometry("680x400")
        self.db = schedulerDatabase('scheduler.db')
        self.atualiza_processos()

        self.frame1 = tk.Frame(self)
        self.frame1.pack(side=tk.LEFT, anchor='ne')
        self.frame2 = tk.Frame(self)
        self.frame2.pack()
        self.make_treeview(self.frame2)
 
        self.button_new = tk.Button(self.frame1, text='Novo', pady=10, padx=10, width=20)
        self.button_new.pack(side=tk.TOP)
        self.button_new.bind('<Button-1>', self.new_form)
        self.button_delete = tk.Button(self.frame1, text='Delete', pady=10, padx=10, width=20, command=self.delete_process)
        self.button_delete.pack(side=tk.TOP)

    def atualiza_processos(self):
        self.processes = self.db.query('SELECT * FROM scheduled_processes')

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
        entry = tk.Entry(master)
        label.grid(row=grid_row,column=0)
        entry.grid(row=grid_row,column=1)
        return entry

    def valida(self):
        # Testando a função
        if not validar_data(self.dt.get()):
            messagebox.showerror("Entrada inválida", "Por favor, digite uma data no formato DIA/MES/ANO no campo de data.")
        else:
            validar_inteiro(self.i.get())
            dt_ = datetime.strptime(self.dt.get(),"%d/%m/%Y")
            self.db.insert_process(self.nome.get(), self.argumento.get(), self.caminho.get(), dt_, int(self.i.get()))
            messagebox.showinfo('Sucesso!', 'Seu processo foi salvo com sucesso!')
            if not messagebox.askyesno("Continuar?", "Deseja inserir mais processos?"):
                self.atualiza_processos()
                self.mpopup.destroy()
                self.update_treeview()

    def new_form(self, event):
        self.mpopup = tk.Toplevel(self)
        self.mpopup.transient(self)
        self.mpopup.title("New Window")
        self.mpopup_frame1 = tk.Frame(self.mpopup, pady=5)
        self.mpopup_frame2 = tk.Frame(self.mpopup, pady=5)
        self.mpopup_frame1.pack()
        self.mpopup_frame2.pack()
    
        # sets the geometry of toplevel
        self.mpopup.geometry("300x180")
    
        # A Label widget to show in toplevel
        self.nome = self.label_entry(self.mpopup_frame1, 'Nome', 0)
        self.argumento = self.label_entry(self.mpopup_frame1, 'Argumento', 1)
        self.caminho = self.label_entry(self.mpopup_frame1, 'Caminho', 2)
        self.dt = self.label_entry(self.mpopup_frame1, 'Date', 3)
        self.i = self.label_entry(self.mpopup_frame1, 'Interval', 4)
        ok = tk.Button(self.mpopup_frame2, text='OK',command=self.valida,width=10)
        ok.pack()

    def pop_up(self, event):
        self.popup_window = tk.Toplevel(self)
        self.popup_window.title("New Window")
    
        # sets the geometry of toplevel
        self.popup_window.geometry("200x200")
    
        # A Label widget to show in toplevel
        tk.Label(self.popup_window, 
        text ="This is a new window").pack()

    def on_treeview_select(self, event):
        selected_item = self.arvore.selection()
        item_text = self.arvore.item(selected_item, 'values')
        print(f"Linha selecionada: {item_text}, item: {selected_item}")

    def update_treeview(self):
        # Remover todos os itens existentes
        for item in self.arvore.get_children():
            self.arvore.delete(item)
        
        # Inserir novos itens
        for i, linha in enumerate(self.processes):
            self.arvore.insert("", "end", values=linha)
    
    def make_treeview(self, master):
        cols = [f'col{i}' for i in range(1,6)]
        self.arvore = ttk.Treeview(master, columns=cols, show="headings")
        for col, name in zip(cols, ["id", "nome", "arg", "data", "intervalo (em segundos)"]):
            self.arvore.heading(col, text=name)
        
        # Cria a Scrollbar horizontal
        scrollbar_x = ttk.Scrollbar(master, orient="horizontal", command=self.arvore.xview)
        self.arvore.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Insere os dados nas colunas
        for i, linha in enumerate(self.processes):
            self.arvore.insert("", "end", values=linha)
    
        self.arvore.pack(expand=True)
        self.arvore.bind('<<TreeviewSelect>>', self.on_treeview_select)
        self.arvore.bind('<Double-1>', self.pop_up)

if __name__ == '__main__':
    root = App()
    root.mainloop()