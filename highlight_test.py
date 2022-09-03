import tkinter as tk
from tkinter import ttk


class App(tk.Frame):

    def __init__(self, master):

        tk.Frame.__init__(self, master)

        self.master = master


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

        # Code for Entry - call it NumberInput Class
        # Variables
        text = 'This is a Thing'
        error_text = 'Bacon'
        pady = 10
        maximum = 10
        minimum = 1
        # Initialize max and min for validation
        self.maximum = maximum
        self.minimum = minimum
        # Initialize variable to track focus
        self.focus = False
        # Initialize Label
        self.label = ttk.Label(self, text=text)
        self.label.pack(pady=(pady, 0))
        # Initialize Entry
        self.entry_value = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.entry_value)
        self.entry.pack(padx=10)
        self.entry.bind('<Key>', self.validate)
        self.entry.bind('<FocusOut>', self.entry_FocusOut_handler)
        self.entry.bind('<FocusIn>', self.entry_FocusIn_handler)
        # Initialize Error Label
        self.error_text_var = tk.StringVar()
        self.error_text_var.set(error_text)
        self.error_label = ttk.Label(self, textvariable=self.error_text_var)
        self.error_label.config(foreground='red')
        self.error_label.pack(pady=(0, pady))

    def entry_FocusOut_handler(self, e):
        self.focus = False

    def entry_FocusIn_handler(self, e):
        self.focus = True

    def validate(self, e):
        """
        Creates 2ms delay before calling validate function. This ensures all text is properly read.
        """
        self.after(2, self.number_validation)

    def number_validation(self):
        """
        Validates number to ensure it is within a specified range.
        :return: True or False
        """
        value = int(self.entry_value.get())

        if value >= self.maximum or value <= self.minimum:
            self.entry.state(['invalid'])
            return False
        elif self.focus:
            self.entry.state(['!invalid'])
            return True
        else:
            self.entry.state(['!invalid'])
            self.entry.state(['!focus'])
            return True

    def valid(self):







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

root.geometry('200x200+500+500')

# Simply set the theme
root.tk.call("source", "assets/azure.tcl")
root.tk.call("set_theme", "light")

app = App(root).pack()



root.mainloop()