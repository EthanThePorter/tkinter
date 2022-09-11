import tkinter as tk
from tkinter import ttk


class App(tk.Frame):

    def __init__(self, master):

        tk.Frame.__init__(self, master)

        # Code for standard button
        button1 = ttk.Button(self, text="Test", command=lambda: self.function(0))
        button1.bind('<Return>', self.function)
        button1.pack(pady=10)

        # Code for Dropdown Menu
        items = ["Alkane-Alcohol",
                 "Alcohol-Water", "Ketone-Alcohol",
                 "Alcohol-Alcohol", "Alcohol-Ester"]
        self.dropdown = Dropdown(self, items, 'System Type', width=25)
        self.dropdown.pack(pady=10, padx=10)



        # Entry 2 for testing
        self.entry_test = NumberInput(self, 15, 10, 1000, 'Vapour Pressure (mmHg)', displayBounds=True)
        self.entry_test.pack()

        # Code for Entry - call it NumberInput Class
        self.entry = NumberInput(self, 15, 10, 1000, 'Vapour Pressure (mmHg)', displayBounds=False, command=self.entry_test.update_default)
        self.entry.pack()


        # Code for Filename
        self.filename_input = FilenameInput(self, 'Enter Filename', 'Data')
        self.filename_input.pack()

        self.value = ValueDisplay(self, 45, 'Value Display')
        self.value.pack()

        # Code for Entry - call it NumberInput Class
        self.entry2 = NumberInput(self, 15, 10, 1000, 'Vapour Pressure (mmHg)', displayBounds=False, command=self.entry_test.update_default)
        self.entry2.pack()
        self.entry2.disable()

    def function(self, e):
        """
        Sample function for previewing button.
        :param e: Parameter for .bind() method's events.
        """
        self.dropdown.update_options(['One Item', 'Two', 'Tjree'])


class Dropdown(tk.Frame):

    def __init__(self, parent, items: list, text, width=15, command=None):
        """
        Widget to simplify creating dropdown menus.
        :param parent: Parent Frame.
        :param items: List of items. Does not require the first element to be repeated twice like OptionMenu.
        :param text: Text to display as label.
        :param width: Width of combobox.
        :param command: Command to execute when Dropmenu selection is changed.
        """
        tk.Frame.__init__(self, parent)

        # Process list by having the first element repeat twice.
        # This is because the first element gets deleted by OptionMenu
        items.insert(0, items[0])
        # Initialize title
        if text is not None:
            self.label = ttk.Label(self, text=text)
            self.label.pack()
        # Initialize OptionMenu
        self.value = tk.StringVar(self)
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

    def change_label(self, text):
        self.label.config(text=text)

    def update_options(self, new_options):
        self.option_menu.set_menu(new_options[0], *new_options)


    def get(self):
        return self.value.get()

    def set(self, value):
        self.value.set(value)

    def enable(self):
        self.option_menu.config(state='normal')

    def disable(self):
        self.option_menu.config(state='disabled')

    def background(self, color):
        self.option_menu.config(bg=color)


class NumberInput(tk.Frame):

    def __init__(self, parent, default, minimum, maximum, text, width=30, displayBounds=False, command=None):
        """
        Widget designed for number input and verification. Ensures number are within a range.
        :param parent: Parent Frame
        :param default: Default Number
        :param maximum: Maximum Number
        :param minimum: Minimum Number
        :param text: Label Text
        :param width: Width of Entry Box
        :param displayBounds: Option to display bounds in label or not
        """
        tk.Frame.__init__(self, parent)

        # Initialize command
        self.command = command
        # Initialize numbers for validation
        self.maximum = maximum
        self.minimum = minimum
        self.default = default
        # Initialize variable to track focus
        self.focus = False
        # Initialize variable for displaying bounds and text
        self.text = text
        self.displayBounds = displayBounds
        self.display_bounds_text = tk.StringVar()
        if displayBounds:
            self.display_bounds_text.set(f'{text} ({self.minimum}-{self.maximum})')
        else:
            self.display_bounds_text.set(text)
        # Initialize Label
        self.label = ttk.Label(self, textvariable=self.display_bounds_text)
        self.label.pack()
        # Initialize Entry
        self.entry_value = tk.StringVar(self, str(default))
        self.entry = ttk.Entry(self, textvariable=self.entry_value, width=width)
        self.entry.pack()
        # Initializes binding for command to entry box, if one has been inputted to the class
        if self.command is not None:
            self.entry.bind('<Key>', self.command_handler_delay)
        # Initializes other bindings to entry box
        self.entry.bind('<Key>', self.validate, add='+')
        self.entry.bind('<FocusOut>', self.entry_FocusOut_handler)
        self.entry.bind('<FocusIn>', self.entry_FocusIn_handler)
        # Initialize Error Label
        self.error_text_var = tk.StringVar()
        self.error_text_var.set('')
        self.error_label = ttk.Label(self, textvariable=self.error_text_var)
        self.error_label.config(foreground='red')
        self.error_label.pack()


    def command_handler_delay(self, e):
        """
        Delays command_handler so most recent value is used
        """
        self.after(1, self.command_handler)

    def command_handler(self):
        if self.number_validation():
            self.command(float(self.entry_value.get()))

    def entry_FocusOut_handler(self, e):
        """
        Handles cases for entry going out of focus
        """
        # Sets focus
        self.focus = False
        # Handles various cases for entry value
        try:
            value = float(self.entry_value.get())
            if value == '':
                self.entry_value.set(str(self.default))
            elif value < self.minimum:
                self.entry_value.set(str(self.minimum))
            elif value > self.maximum:
                self.entry_value.set(str(self.maximum))
        except:
            self.entry_value.set(str(self.default))
        # Adjust States
        self.entry.state(['!invalid'])
        self.entry.state(['!focus'])
        self.error_text_var.set('')

    def entry_FocusIn_handler(self, e=0):
        self.focus = True

    def validate(self, e):
        """
        Creates 2ms delay before calling validate function. This ensures all text is properly read.
        """
        return self.after(1, self.number_validation)

    def number_validation(self):
        """
        Validates number to ensure it is within a specified range.
        :return: True or False
        """
        try:
            if self.entry_value.get() == '':
                value = 0
            else:
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
            self.error_text_var.set(f'Invalid Number')
            return False

    def get(self):
        self.update_validate()
        return float(self.entry_value.get())

    def update_label(self, text):
        if self.displayBounds:
            self.display_bounds_text.set(f'{text} ({self.minimum}-{self.maximum})')
        else:
            self.display_bounds_text.set(text)

    def update_default(self, new_default):
        """
        Updates default and sets values
        """
        # Converts to float
        new_default = float(new_default)
        # Check if new default is outside of bounds
        if new_default > self.maximum or new_default < self.minimum:
            raise Exception(f'New Default is outside of currently set bounds\nNew Default:{new_default}\nBounds: {self.minimum}-{self.maximum}')
        # If within bounds
        else:
            self.default = new_default
            self.set(self.default)

    def set(self, value):
        # Check if new default is outside of bounds
        if value > self.maximum or value < self.minimum:
            raise Exception(f'New Value is outside of currently set bounds\nNew Value:{value}\nBounds: {self.minimum}-{self.maximum}')
        else:
            # If within bounds
            self.entry_value.set(str(value))
            self.update_validate()

    def update_bounds(self, new_min, new_max):
        self.maximum = new_max
        self.minimum = new_min
        # Validate Entry Box
        self.update_validate()
        # Update displayed bounds if enabled
        if self.displayBounds:
            self.display_bounds_text.set(f'{self.text} ({self.minimum}-{self.maximum})')

    def update_validate(self):
        """
        Handles cases for updated bounds
        """
        # Handles various cases for entry value
        try:
            value = float(self.entry_value.get())
            if value == '':
                self.entry_value.set(str(self.default))
            elif value < self.minimum:
                self.entry_value.set(str(self.minimum))
            elif value > self.maximum:
                self.entry_value.set(str(self.maximum))
        except:
            self.entry_value.set(str(self.default))
        # Adjust States
        self.entry.state(['!invalid'])
        self.error_text_var.set('')

    def enable(self):
        self.entry.config(state='normal')

    def disable(self):
        self.entry.config(state='disabled')


class ValueDisplay(tk.Frame):

    def __init__(self, parent, value: str | float | int, text: str, width=30):
        """

        :param parent: Parent Frame
        :param value: Value to display in box
        :param text: Text for Label
        :param width: Width of entry box
        """
        tk.Frame.__init__(self, parent)

        # Initialize Label
        self.text = tk.StringVar(self, text)
        self.label = ttk.Label(self, textvariable=self.text)
        self.label.pack()
        # Initialize Entry
        self.entry_value = tk.StringVar(self, str(value))
        self.entry = ttk.Entry(self, textvariable=self.entry_value, width=width, foreground='black', background='black')
        self.entry.config(state='disabled')
        self.entry.pack()

    def update_label(self, text):
        self.text.set(text)

    def set(self, value):
        self.entry_value.set(str(value))



class FilenameInput(tk.Frame):

    def __init__(self, parent, text, default, character_limit=25, width=30):
        """
        Entry box designed specific for filenames. Validates the entered string with the requirements of a filename.
        :param parent: Parent Frame
        :param text: Text to display as label
        :param default: Default filename
        :param character_limit: Character Limit
        :param width: Width of Entry Box
        """
        tk.Frame.__init__(self, parent)

        # Initialize variable to track focus
        self.focus = False
        # Initialize variables
        self.character_limit = character_limit
        self.default = default
        # Initialize Label
        self.label = ttk.Label(self, text=text)
        self.label.pack()
        # Initialize Entry Box
        self.filename = tk.StringVar()
        self.filename.set(default)
        self.fileEntry = ttk.Entry(self, textvariable=self.filename, width=width)
        self.fileEntry.pack()
        self.fileEntry.bind('<Key>', self.validate)
        self.fileEntry.bind('<FocusOut>', self.entry_FocusOut_handler)
        self.fileEntry.bind('<FocusIn>', self.entry_FocusIn_handler)
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
        # Sets focus
        self.focus = False
        # Get Value from Entry and lowercase it
        value = str(self.fileEntry.get())
        value = value.lower()
        valid = self.fileName_validation()
        if not valid:
            self.filename.set(str(self.default))
        # Adjust States
        self.fileEntry.state(['!invalid'])
        self.fileEntry.state(['!focus'])
        self.error_text_var.set('')

    def entry_FocusIn_handler(self, e):
        self.focus = True

    def validate(self, e):
        """
        Creates 2ms delay before calling validate function. This ensures all text is properly read.
        """
        return self.after(2, self.fileName_validation)

    def fileName_validation(self):
        """
        Validates number to ensure it is within a specified range.
        :return: True or False
        """
        try:
            # Get value from Entry and lowercase it
            value = str(self.filename.get())
            value = value.lower()
            # Define list of acceptable characters and check the entry value
            valid_characters = 'abcdefghijklmnopqrstuvwxyz1234567890_-'
            for char in value:
                if valid_characters.__contains__(char) is False:
                    # Set states and return False
                    self.fileEntry.state(['invalid'])
                    self.error_text_var.set('Use only (A-Z), (0-9), (-), (_)')
                    return False
            # Check length
            if len(value) > self.character_limit:
                # Set states and return False
                self.fileEntry.state(['invalid'])
                self.error_text_var.set(f'Exceeds {self.character_limit} Character Limit')
                return False
            elif len(value) == 0:
                self.fileEntry.state(['invalid'])
                self.error_text_var.set('Empty Filename')
                return False
            # If all tests pass, check for focus
            if self.focus:
                self.fileEntry.state(['!invalid'])
                self.error_text_var.set('')
                return True
            else:
                self.fileEntry.state(['!invalid'])
                self.fileEntry.state(['!focus'])
                self.error_text_var.set('')
                return True
        except:
            print('Case 5')
            self.fileEntry.state(['invalid'])
            self.error_text_var.set('Empty Filename')
            return False

    def get(self):
        self.fileName_validation()
        return str(self.filename.get())

    def disable(self):
        self.fileEntry.config(state='disabled')

    def enable(self):
        self.fileEntry.config(state='active')


# Create Root Frame
root = tk.Tk()
root.geometry('300x500+500+500')

# Simply set the theme
root.tk.call("source", "assets/azure.tcl")
root.tk.call("set_theme", "light")

app = App(root).pack()
root.mainloop()