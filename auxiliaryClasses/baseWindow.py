import tkinter as tk


class BaseWindow(tk.Frame):
    def __init__(self, parent, title, width=500, height=400):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.width = width
        self.height = height
        self.title = title
        self.pack(fill=tk.BOTH, expand=True)
        self.initUI()

    def create_new_window(self, window_name):
        from courseThemes.integration import Integration
        from courseThemes.equation import Equation
        from courseThemes.polinom import Polinom
        from courseThemes.mnk import MNK
        from auxiliaryClasses.menu import Menu
        
        window_classes = {
            'Интегралы': Integration,
            'Уравнения': Equation,
            'Полиномы': Polinom,
            'МНК': MNK,
            'Меню': Menu,
        }
        
        window_titles = {
            'Интегралы': 'Численное интегрирование (Интегралы)',
            'Уравнения': 'Решение НУ',
            'Полиномы': 'Решение полинома',
            'МНК': 'Аппроксимация МНК',
            'Меню': 'Курсовая работа - Меню',
        }
        
        self.parent.destroy()
        root = tk.Tk()
        app_class = window_classes.get(window_name)
        title = window_titles.get(window_name, window_name)
        
        if app_class:
            app = app_class(root, title)
            root.mainloop()

    def centrize_window(self):
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x, y = (sw - self.width) // 2, (sh - self.height) // 2
        self.parent.geometry(f'{self.width}x{self.height}+{x}+{y}')
        self.parent.resizable(False, False)
    
    def check_is_number(self, number):
        try:
            float(number)
            return True
        except ValueError:
            return False

    def initUI(self):
        self.parent.title(self.title)
        self.centrize_window()