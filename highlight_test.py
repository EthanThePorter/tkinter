import tkinter as tk
from tkinter import ttk


class App(tk.Frame):

    def __init__(self, master):

        tk.Frame.__init__(self, master)

        self.master = master


        # Code for standard button
        button1 = ttk.Button(self, text="Test", command=lambda: self.function(0))
        button1.bind('<Return>', self.function)
        button1.pack(pady=10)


        # Code for Dropdown Menu
        items = ["Alkane-Alcohol", "Alkane-Alcohol",
                 "Alcohol-Water", "Ketone-Alcohol",
                 "Alcohol-Alcohol", "Alcohol-Ester"]
        self.dropdown = Dropdown(self, items)
        self.dropdown.pack(pady=10, padx=10)


        # Code for Entry - call it NumberInput Class
        self.entry = NumberInput(self, 5, 10, 1, 'Vapour Pressure (mmHg) (1-10)')
        self.entry.pack()


    def function(self, e):
        print(self.entry.get())


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


class NumberInput(tk.Frame):

    def __init__(self, parent, default, maximum, minimum, text, width=30):
        tk.Frame.__init__(self, parent)

        # Initialize numbers for validation
        self.maximum = maximum
        self.minimum = minimum
        self.default = default
        # Initialize variable to track focus
        self.focus = False
        # Initialize Label
        self.label = ttk.Label(self, text=text)
        self.label.pack()
        # Initialize Entry
        self.entry_value = tk.StringVar(self, str(default))
        self.entry = ttk.Entry(self, textvariable=self.entry_value, width=width)
        self.entry.pack()
        self.entry.bind('<Key>', self.validate)
        self.entry.bind('<FocusOut>', self.entry_FocusOut_handler)
        self.entry.bind('<FocusIn>', self.entry_FocusIn_handler)
        # Initialize Error Label
        self.error_text_var = tk.StringVar()
        self.error_text_var.set('')
        self.error_label = ttk.Label(self, textvariable=self.error_text_var)
        self.error_label.config(foreground='red')
        self.error_label.pack()

    def entry_FocusOut_handler(self, e):
        """
        Handles cases for entry going out of focus
        """
        print('Focus Out')
        # Sets focus
        self.focus = False
        # Handles various cases for entry value
        try:
            value = float(self.entry_value.get())
            if value == '':
                self.entry_value.set(str(self.minimum))
            elif value < self.minimum:
                self.entry_value.set(str(self.minimum))
            elif value > self.maximum:
                self.entry_value.set(str(self.maximum))
        except:
            self.entry_value.set(str(self.default))

    def entry_FocusIn_handler(self, e):
        self.focus = True

    def validate(self, e):
        """
        Creates 2ms delay before calling validate function. This ensures all text is properly read.
        """
        return self.after(2, self.number_validation)

    def number_validation(self):
        """
        Validates number to ensure it is within a specified range.
        :return: True or False
        """
        try:
            value = float(self.entry_value.get())
            if value > self.maximum or value < self.minimum:
                self.entry.state(['invalid'])
                self.error_text_var.set(f'Range: {self.minimum}-{self.maximum}')
                return False
            elif self.focus:
                self.entry.state(['!invalid'])
                self.error_text_var.set('')
                return True
            else:
                self.entry.state(['!invalid'])
                self.entry.state(['!focus'])
                self.error_text_var.set('')
                return True
        except:
            self.entry.state(['invalid'])
            self.error_text_var.set('Invalid Number')
            return False

    def get(self):
        return float(self.entry_value.get())


root = tk.Tk()

root.geometry('300x300+500+500')

# Simply set the theme
root.tk.call("source", "assets/azure.tcl")
root.tk.call("set_theme", "light")

app = App(root).pack()



root.mainloop()