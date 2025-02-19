import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry
from pyagenda3.gui.features.centralize import spawn_on_mouse
from pyagenda3.gui.features.hover import CreateToolTip
from pyagenda3.gui.features.copy_paste import add_copy_and_paste_right_click

OPCOES_INTERVALO = ['12 horas', '1 dia', '1 semana']

class NewEditProcessForm:

    def __init__(self, master, title: str, ok_button_function, dims: tuple = (300, 160)):
        self.master = master
        self.form = tk.Toplevel(master); 
        self.form.transient()
        self.form.title(title)
        spawn_on_mouse(master, self.form, dims)
        self.frame1 = tk.Frame(self.form, pady=5)
        self.frame2 = tk.Frame(self.form, pady=5)
        self.frame1.pack(); self.frame2.pack()
        self.create_entries(); self.date_entry(); self.interval_entry()
        self.add_popups_caminho()
        ok = tk.Button(self.frame2, text='OK',width=10)
        ok.pack()
        ok.bind('<Button-1>', ok_button_function)
        ok.bind('<Return>', ok_button_function)
        self.form.focus_force()

    def create_entries(self):
        self.nome = self.label_entry(self.frame1, 'Nome', 0)
        self.argumento = self.label_entry(self.frame1, 'Argumento', 1)
        self.caminho = self.label_entry(self.frame1, 'Caminho', 2)
        add_copy_and_paste_right_click(self.master, self.argumento)
        add_copy_and_paste_right_click(self.master, self.caminho)
        
    def add_popups_caminho(self):
        self.caminho.bind("<Double-1>", self.browse_directory)
        self.argumento.bind("<Tab>", self.browse_directory)
        CreateToolTip(self.caminho, "Clique duas vezes para abrir a seleção de arquivos")

    def browse_directory(self, event):
        directory = filedialog.askdirectory(parent=self.form)
        self.form.deiconify()
        self.form.focus_force()
        if directory:
            self.caminho.delete(0, tk.END)
            self.caminho.insert(0, directory)
        
    def date_entry(self):
        tk.Label(self.frame1, text='Data: ',width=10, anchor='w').grid(row=3,column=0)
        self.dt = tk.StringVar(self.form)
        DateEntry(self.frame1, selectmode='day',textvariable=self.dt, locale='pt_br', width=22).grid(row=3,column=1)

    def interval_entry(self):
        tk.Label(self.frame1, text='Intervalo: ',width=10, anchor='w').grid(row=4,column=0)
        self.i = ttk.Combobox(self.frame1,values=OPCOES_INTERVALO, width=22)
        self.i.grid(row=4,column=1)

    def label_entry(self, master, name: str, grid_row: int):
        labelText=tk.StringVar()
        labelText.set(name)
        label = tk.Label(master, textvariable=labelText, width=10, anchor='w')
        entry = tk.Entry(master, width=25)
        label.grid(row=grid_row,column=0)
        entry.grid(row=grid_row,column=1)
        return entry
