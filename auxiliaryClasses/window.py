import tkinter as tk

from courseThemes.integration import Integration
from courseThemes.equation import Equation
from courseThemes.polinom import Polinom
from auxiliaryClasses.menu import Menu
from auxiliaryClasses.baseWindow import BaseWindow

class Window(BaseWindow):
    def __init__(self, parent, title, width=500, height=400):
        super().__init__()
    
    def create_new_window(self, window_name):
        self.parent.destroy()
        root = tk.Tk()
        app_class = self.windows_dict[window_name][0]
        title = self.windows_dict[window_name][1]
        app = app_class(root, title)
        root.mainloop()
