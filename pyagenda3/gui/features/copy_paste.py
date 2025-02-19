from pyagenda3.gui.features.right_click_popup import RightClickPopup
from tkinter import TclError

def paste(root, widget):
    clipboard = root.clipboard_get()  # Obtém o item copiado da área de transferência do sistema
    try:
        start = widget.index('sel.first')  # Pega o índice do início da seleção
        end = widget.index('sel.last')  # Pega o índice do fim da seleção
        widget.delete(start, end)  # Deleta o texto selecionado
        widget.insert(start, clipboard)  # Insere o item do clipboard no início da seleção
    except TclError:
        widget.insert('end', clipboard)  # Insere o item no final do widget se não houver seleção

def copy(root, widget):
    inp = widget.get() # Get the text inside entry widget
    root.clipboard_clear() # Clear the tkinter clipboard
    root.clipboard_append(inp) # Append to system clipboard

def add_copy_and_paste_right_click(root, widget):
    RightClickPopup(widget, 
        ("Copiar", "Colar", ), 
        (lambda: copy(root, widget), lambda: paste(root, widget),))