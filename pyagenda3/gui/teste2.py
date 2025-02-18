from tkinter import *

def selection_present():
    print(entry.select_present())
    if entry.select_present():
        print(entry.selection_get())

root = Tk()

entry = Entry(root)
entry.pack()

Button(root, text="Check selection", command=selection_present).pack()

root.mainloop()