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

        # Code for standard combobox
        sys_type_select = tk.StringVar()
        sys_type_select.set("Alkane-Alcohol")
        sys_type_options = ["Alkane-Alcohol", "Alkane-Alcohol", "Alcohol-Water", "Ketone-Alcohol", "Alcohol-Alcohol",
                            "Alcohol-Ester"]
        self.option_menu = ttk.OptionMenu(self, sys_type_select, *sys_type_options,)
        self.option_menu.pack(pady=10)

        # FUNCTION TO Cycle
        self.option_menu.bind('<Return>', lambda event: self.option_menu_return_handler(self.option_menu))
        self.option_menu.bind('<Return>', self.option_menu.focus())


    def yup(self, e):
        print("yup")

    @staticmethod
    def option_menu_return_handler(menu: ttk.OptionMenu):
        """Function required to handle <Return> event to open OptionMenu Dropdown"""
        menu.event_generate('<Button-1>', when='tail')
        menu.event_generate('<ButtonRelease>', when='tail')
        menu.focus()





    # ...

root = tk.Tk()

# Simply set the theme
root.tk.call("source", "assets/azure.tcl")
root.tk.call("set_theme", "light")

app = App(root).pack()

root.mainloop()