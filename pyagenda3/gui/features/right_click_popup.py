import tkinter as tk

class RightClickPopup:

    def __init__(self, master, labels: list, commands: list, separator_index: int = -1):
        self.master = master
        self.menu = tk.Menu(master, tearoff=0)
        self.master.bind("<Button-3>", self.popup)
        self.add_commands(labels, commands, separator_index)
    
    def add_commands(self, labels: list, commands: list, separator_index: int):
        for i, (label, command) in enumerate(zip(labels, commands)):
            self.menu.add_command(label=label, command=command)
            if i == separator_index:
                self.menu.add_separator()

    def popup(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()
