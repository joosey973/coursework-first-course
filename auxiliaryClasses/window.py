import tkinter as tk

from courseThemes.integration import Integration
from courseThemes.equation import Equation
from courseThemes.polinom import Polinom
from auxiliaryClasses.menu import Menu


class Window(tk.Frame):
    def __init__(self, parent, title, width=500, height=400):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.width = width
        self.height = height
        self.title = title
        self.windows_dict = {'Интегралы': [Integration, 'Численное интегрирование (Интегралы)'],
                              'Меню': [Menu, 'Курсовая работа - Меню'],
                              'Уравнения': [Equation, 'Решение НУ'],
                              'Полиномы': [Polinom, 'Решение полинома']}
        self.pack(fill=tk.BOTH, expand=True)
        self.initUI()

    def centrize_window(self):
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x, y = (sw - self.width) // 2, (sh - self.height) // 2
        self.parent.geometry(f'{self.width}x{self.height}+{x}+{y}')
        self.parent.resizable(False, False)
    
    def create_new_window(self, window_name):
        self.parent.destroy()
        root = tk.Tk()
        app_class = self.windows_dict[window_name][0]
        title = self.windows_dict[window_name][1]
        app = app_class(root, title)
        root.mainloop()
    
    def check_is_number(self, number):
        try:
            float(number)
            return True
        except ValueError:
            return False

    def initUI(self):
        print(self.title, True)
        self.parent.title(self.title)
        self.centrize_window()