import tkinter as tk
from tkinter import ttk

def update_treeview(tree):
    # Exemplos de dados: (Processo, Status)
    processes = [
        ("Processo 1", "Ativo"),
        ("Processo 2", "Inativo"),
        ("Processo 3", "Ativo"),
        ("Processo 4", "Inativo"),
    ]

    for process, status in processes:
        if status == "Inativo":
            tree.insert("", "end", values=(process, status), tags=("inactive",))
        else:
            tree.insert("", "end", values=(process, status))

def on_select(event):
    for item in tree.selection():
        status = tree.item(item, "values")[1]
        if status == "Inativo":
            tree.tag_configure("selected_inactive", background="#FFC0CB", foreground="black")
            tree.item(item, tags=("selected_inactive",))
        else:
            tree.tag_configure("selected_active", background="#90EE90", foreground="black")
            tree.item(item, tags=("selected_active",))

def apply_custom_style():
    # Customizando o estilo de seleção
    style = ttk.Style()
    style.map("Treeview", 
              foreground=[('selected', 'white')],
              background=[('selected', '#FF69B4')])  # Cor rosa choque para seleção

root = tk.Tk()
root.title("Treeview de Processos")

tree = ttk.Treeview(root, columns=("process", "status"), show="headings")
tree.heading("process", text="Processo")
tree.heading("status", text="Status")

# Definindo estilo para processos inativos
style = ttk.Style()
style.configure("Treeview.Inactive", background="#FFC0CB")  # Cor rosa claro para inativos
tree.tag_configure("inactive", background="#FFC0CB")

apply_custom_style()

# Ligando o evento de seleção
tree.bind("<<TreeviewSelect>>", on_select)

tree.pack(fill=tk.BOTH, expand=True)

update_treeview(tree)

root.mainloop()
