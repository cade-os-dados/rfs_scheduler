import tkinter as tk
 
# w -> largura
# h -> altura
# x -> posicao horizontal
# y -> posicao vertical
def centralize_dimensions(w,h,x,y, w_, h_):
    y_ = (2*x+h)/2
    x_ = (2*y+w)/2
    return int(x_ - w_/2), int(y_ - h_/2)

def toplevel_centralize(master, width, height, deiconify=True):
    mpopup = tk.Toplevel(master)
    mpopup.withdraw()
    master.update()
    w = master.winfo_width()
    h = master.winfo_height()
    x = master.winfo_x()
    y = master.winfo_y()
    x_, y_ = centralize_dimensions(w,h,x,y, width, height)
    mpopup.title("Desafio")
    mpopup.geometry(f"{width}x{height}+{x_}+{y_}")
    if deiconify:
        mpopup.deiconify()
    return mpopup

# apenas para fins de visualização
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1280x720")
    root.title("Janela com Sidebar")
    
    botao = tk.Button(root, width=20, text='Clique aqui', command=lambda: toplevel_centralize(root,300,180))
    botao.pack()
    
    root.mainloop()
 