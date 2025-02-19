import tkinter as tk
from tkinter import ttk

class TreeviewHider:
    def __init__(self, tree: ttk.Treeview, nrows_var: tk.StringVar):
        self.tree = tree
        self.nrows_var = nrows_var
        self.detached_items = []
        self.last_nrows = -1
        self.total_insertions = 0

    def hide_rows(self):
        nrows = int(self.nrows_var.get())
        if nrows > self.last_nrows and self.last_nrows != -1:
            self.unhide()
        self.last_nrows = nrows
        for i, item_id in enumerate(self.tree.get_children()):
            if i+1 > nrows:
                self.tree.detach(item_id)
                self.detached_items.append(item_id)

    def unhide(self):
        n_children = len(self.tree.get_children())
        for i, item_id in enumerate(self.detached_items):
            self.tree.reattach(item_id,'',i+n_children)
        self.detached_items.clear()