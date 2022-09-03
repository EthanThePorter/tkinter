import tkinter as tk
from tkinter import ttk

class App(tk.Frame):

    def __init__(self, master):

        tk.Frame.__init__(self, master)

        self.master = master

        entry1 = ttk.Entry(self)
        entry1.pack()

        entry2 = ttk.Entry(self)
        entry2.pack()

        # Code for standard button
        button1 = ttk.Button(self, text="Test", command=lambda: self.yup(0))
        button1.bind('<Return>', self.yup)
        button1.pack(pady=10)

        # Code for Dropdown Menu
        items = ["Alkane-Alcohol", "Alkane-Alcohol",
                 "Alcohol-Water", "Ketone-Alcohol",
                 "Alcohol-Alcohol", "Alcohol-Ester"]

        self.dropdown = Dropdown(self, items)
        self.dropdown.pack(pady=10, padx=10)

    def yup(self, e):
        print("yup")


class Dropdown(tk.Frame):

    def __init__(self, parent, items, width=15, command=None):
        tk.Frame.__init__(self, parent)

        # Initialize OptionMenu
        self.value = tk.StringVar()
        self.value.set(items[0])
        self.options = items
        self.option_menu = ttk.OptionMenu(self,
                                          self.value,
                                          *self.options,
                                          command=command)
        self.option_menu.config(width=width)
        self.option_menu.bind('<Return>', lambda event: self.option_menu_return_handler(self.option_menu))
        self.option_menu.pack()

    @staticmethod
    def option_menu_return_handler(menu: ttk.OptionMenu):
        """
        Function required to handle <Return> event to open OptionMenu Dropdown
        """
        menu.event_generate('<space>', when='tail')
        menu.focus()

    def get(self):
        """
        :return: Returns value of Dropdown OptionMenu
        """
        return self.value.get()


root = tk.Tk()

# Simply set the theme
root.tk.call("source", "assets/azure.tcl")
root.tk.call("set_theme", "light")

app = App(root).pack()

root.mainloop()