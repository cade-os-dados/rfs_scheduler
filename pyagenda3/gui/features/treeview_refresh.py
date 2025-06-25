from tkinter import ttk

class TreeViewRefresher:

    def __init__(self, tree: ttk.Treeview, delay: int, insert_on_end: bool = True, debug=False):
        self.tree = tree
        self.delay = delay
        self.debug = debug
        self.ids = set()
        self.id_to_item = {}
        self.setup()
        self.insert_on_end = insert_on_end

    def insertion_position(self):
        return "end" if self.insert_on_end else 0

    def setup(self):
        for item in self.tree.get_children():
            id = int(self.tree.item(item)["values"][0])
            self.ids.add(id)
            self.id_to_item[id] = item

    def refresh(self, data_generator):
        new_data =  data_generator()
        for tupla in new_data:
            if tupla[0] not in self.ids:
                self.ids.add(tupla[0])
                item_id = self.tree.insert("", self.insertion_position(), values = tupla)
                self.id_to_item[tupla[0]] = item_id
            else:
                item = self.id_to_item[tupla[0]]
                values = self.tree.item(item)["values"]
                if not tupla == values:
                    self.tree.item(item, values=tupla)

    def run(self, data_generator):
        if self.debug:
            print(self.id_to_item.items())
        self.refresh(data_generator)
        self.tree.after(self.delay, lambda: self.run(data_generator))