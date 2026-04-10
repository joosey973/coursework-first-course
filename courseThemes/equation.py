import tkinter as tk
import tkinter.messagebox as tkm

import numpy as np
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from auxiliaryClasses.baseWindow import BaseWindow


class Equation(BaseWindow):
    def __init__(self, parent, title):
        self.photos = []
        self.sections = []
        self.current_section_index = 0
        self.ax = None
        self.figure = None
        self.canvas = None
        super().__init__(parent, title, width=1200, height=700)
    
    def first_function(self, x):
        return 3**x - 2*x - 5
    
    def second_function(self, x):
        return 3*x**4 + 8*x**3 + 6*x**2 - 10
    
    def derivative_of_first_function(self, x):
        return 3**x * np.log(3) - 2
    
    def derivative_of_second_function(self, x):
        return 12*x**3 + 24*x**2 + 12*x
    
    def second_derivative_of_first_function(self, x):
        return 3**x * np.log(3)**2
    
    def second_derivative_of_second_function(self, x):
        return 36*x**2 + 48*x + 12
    
    def find_function_values(self, x, function_choice):
        return self.first_function(x) if function_choice == 1 else self.second_function(x)
    
    def find_derivative(self, x, function_choice):
        return self.derivative_of_first_function(x) if function_choice == 1 else self.derivative_of_second_function(x)
    
    def find_second_derivative(self, x, function_choice):
        return self.second_derivative_of_first_function(x) if function_choice == 1 else self.second_derivative_of_second_function(x)
    
    def create_values_fields(self):
        values_frame = ctk.CTkFrame(self, corner_radius=15, width=380, height=200)
        values_frame.place(relx=0.02, rely=0.03)
        
        title_label = ctk.CTkLabel(values_frame, text='Параметры', font=('Arial', 16, 'bold'))
        title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        a_label = ctk.CTkLabel(values_frame, text='a:', font=('Arial', 14, 'bold'))
        a_label.place(relx=0.1, rely=0.35)
        
        self.a_field = ctk.CTkEntry(values_frame, font=('Arial', 14), width=200, corner_radius=8)
        self.a_field.place(relx=0.3, rely=0.35)
        self.a_field.bind('<KeyRelease>', lambda e: self.clear_method_fields())
        
        b_label = ctk.CTkLabel(values_frame, text='b:', font=('Arial', 14, 'bold'))
        b_label.place(relx=0.1, rely=0.55)
        
        self.b_field = ctk.CTkEntry(values_frame, font=('Arial', 14), width=200, corner_radius=8)
        self.b_field.place(relx=0.3, rely=0.55)
        self.b_field.bind('<KeyRelease>', lambda e: self.clear_method_fields())

        eps_label = ctk.CTkLabel(values_frame, text='ε:', font=('Arial', 14, 'bold'))
        eps_label.place(relx=0.1, rely=0.75)

        self.eps_field = ctk.CTkEntry(values_frame, font=('Arial', 14), width=200, corner_radius=8)
        self.eps_field.place(relx=0.3, rely=0.75)
        self.eps_field.insert(0, '0.0001')
        self.eps_field.bind('<KeyRelease>', lambda e: self.clear_method_fields())
    
    def create_methods_fields(self):
        methods_frame = ctk.CTkFrame(self, corner_radius=15, width=550, height=450)
        methods_frame.place(relx=0.02, rely=0.33)
        
        title_label = ctk.CTkLabel(methods_frame, text='Результаты методов', font=('Arial', 16, 'bold'))
        title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
        
        method_header = ctk.CTkLabel(methods_frame, text='Метод', font=('Arial', 14, 'bold'))
        method_header.place(relx=0.1, rely=0.12)
        
        value_header = ctk.CTkLabel(methods_frame, text='Корень', font=('Arial', 14, 'bold'))
        value_header.place(relx=0.45, rely=0.12)
        
        iter_header = ctk.CTkLabel(methods_frame, text='Итерации', font=('Arial', 14, 'bold'))
        iter_header.place(relx=0.75, rely=0.12)

        dihotomia_label = ctk.CTkLabel(methods_frame, text='Дихотомия:', font=('Arial', 13))
        dihotomia_label.place(relx=0.1, rely=0.22)
        
        self.dihotomia_field = ctk.CTkEntry(methods_frame, font=('Arial', 13), width=150, corner_radius=8, height=30)
        self.dihotomia_field.place(relx=0.4, rely=0.22)
        
        self.dihotomia_iter_field = ctk.CTkEntry(methods_frame, font=('Arial', 13), width=80, corner_radius=8, height=30)
        self.dihotomia_iter_field.place(relx=0.75, rely=0.22)

        hord_label = ctk.CTkLabel(methods_frame, text='Хорд:', font=('Arial', 13))
        hord_label.place(relx=0.1, rely=0.32)
        
        self.hord_field = ctk.CTkEntry(methods_frame, font=('Arial', 13), width=150, corner_radius=8, height=30)
        self.hord_field.place(relx=0.4, rely=0.32)
        
        self.hord_iter_field = ctk.CTkEntry(methods_frame, font=('Arial', 13), width=80, corner_radius=8, height=30)
        self.hord_iter_field.place(relx=0.75, rely=0.32)

        kas_label = ctk.CTkLabel(methods_frame, text='Касательных:', font=('Arial', 13))
        kas_label.place(relx=0.1, rely=0.42)
        
        self.kas_field = ctk.CTkEntry(methods_frame, font=('Arial', 13), width=150, corner_radius=8, height=30)
        self.kas_field.place(relx=0.4, rely=0.42)
        
        self.kas_iter_field = ctk.CTkEntry(methods_frame, font=('Arial', 13), width=80, corner_radius=8, height=30)
        self.kas_iter_field.place(relx=0.75, rely=0.42)

        comb_label = ctk.CTkLabel(methods_frame, text='Комбинированный:', font=('Arial', 13))
        comb_label.place(relx=0.1, rely=0.52)
        
        self.comb_field = ctk.CTkEntry(methods_frame, font=('Arial', 13), width=150, corner_radius=8, height=30)
        self.comb_field.place(relx=0.4, rely=0.52)
        
        self.comb_iter_field = ctk.CTkEntry(methods_frame, font=('Arial', 13), width=80, corner_radius=8, height=30)
        self.comb_iter_field.place(relx=0.75, rely=0.52)

        iter_label = ctk.CTkLabel(methods_frame, text='Итераций:', font=('Arial', 13))
        iter_label.place(relx=0.1, rely=0.62)
        
        self.iter_field = ctk.CTkEntry(methods_frame, font=('Arial', 13), width=150, corner_radius=8, height=30)
        self.iter_field.place(relx=0.4, rely=0.62)
        
        self.iter_iter_field = ctk.CTkEntry(methods_frame, font=('Arial', 13), width=80, corner_radius=8, height=30)
        self.iter_iter_field.place(relx=0.75, rely=0.62)

        readonly_fields = [
            self.dihotomia_field, self.dihotomia_iter_field,
            self.hord_field, self.hord_iter_field,
            self.kas_field, self.kas_iter_field,
            self.comb_field, self.comb_iter_field,
            self.iter_field, self.iter_iter_field
        ]
        
        for field in readonly_fields:
            field.configure(state='readonly')
    
    def create_functions_choice(self):
        functions_frame = ctk.CTkFrame(self, corner_radius=15, width=250, height=200)
        functions_frame.place(relx=0.35, rely=0.03)
        
        title_label = ctk.CTkLabel(functions_frame, text='Выберите функцию', font=('Arial', 16, 'bold'))
        title_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.radio_var = tk.IntVar(value=1)
        first_function_btn = ctk.CTkRadioButton(functions_frame, text='f(x) = 3ˣ - 2x - 5', 
                                                variable=self.radio_var, value=1, 
                                                command=self.on_function_change,
                                                font=('Arial', 13))
        second_function_btn = ctk.CTkRadioButton(functions_frame, text='f(x) = 3x⁴ + 8x³ + 6x² - 10', 
                                                 variable=self.radio_var, value=2,
                                                 command=self.on_function_change,
                                                 font=('Arial', 13))

        first_function_btn.place(relx=0.1, rely=0.45)
        second_function_btn.place(relx=0.1, rely=0.7)
    
    def create_buttons(self):
        buttons_frame = ctk.CTkFrame(self, corner_radius=15, width=400, height=150)
        buttons_frame.place(relx=0.65, rely=0.75)

        update_sections_btn = ctk.CTkButton(buttons_frame, text='Автоподбор отрезка', 
                                           corner_radius=10, width=180, height=35, 
                                           font=('Arial', 13),
                                           command=self.update_sections)
        update_sections_btn.place(relx=0.05, rely=0.2)

        solve_btn = ctk.CTkButton(buttons_frame, text='Решить уравнение', 
                                   corner_radius=10, width=180, height=35,
                                   font=('Arial', 13),
                                   command=self.solve_equation)
        solve_btn.place(relx=0.52, rely=0.2)

        graphic_btn = ctk.CTkButton(buttons_frame, text='Построить график', 
                                     corner_radius=10, width=180, height=35,
                                     font=('Arial', 13),
                                     command=self.build_graphic)
        graphic_btn.place(relx=0.05, rely=0.55)

        back_to_menu_btn = ctk.CTkButton(buttons_frame, text='Вернуться в меню<', 
                                          corner_radius=10, width=180, height=35,
                                          font=('Arial', 13),
                                          command=lambda: self.create_new_window('Меню'))
        back_to_menu_btn.place(relx=0.52, rely=0.55)
    
    def show_graphic(self):
        graphic_frame = ctk.CTkFrame(self, corner_radius=15, width=500, height=450)
        graphic_frame.place(relx=0.57, rely=0.03)
        
        title_label = ctk.CTkLabel(graphic_frame, text='График функции', font=('Arial', 16, 'bold'))
        title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
        
        self.figure = Figure(figsize=(5.5, 4.5), dpi=90)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('x', fontsize=10)
        self.ax.set_ylabel('y', fontsize=10)
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.figure, master=graphic_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.5, rely=0.55, anchor=tk.CENTER, width=480, height=380)
        
        self.on_function_change()
    
    def on_function_change(self):
        self.clear_method_fields()
        self.auto_set_bounds()
        self.build_graphic()
    
    def auto_set_bounds(self):
        function_choice = self.radio_var.get()
        
        if function_choice == 1:
            self.a_field.delete(0, tk.END)
            self.a_field.insert(0, '0')
            self.b_field.delete(0, tk.END)
            self.b_field.insert(0, '3')
        else:
            self.a_field.delete(0, tk.END)
            self.a_field.insert(0, '-3')
            self.b_field.delete(0, tk.END)
            self.b_field.insert(0, '1')
    
    def clear_method_fields(self):
        fields = [
            self.dihotomia_field, self.dihotomia_iter_field,
            self.hord_field, self.hord_iter_field,
            self.kas_field, self.kas_iter_field,
            self.comb_field, self.comb_iter_field,
            self.iter_field, self.iter_iter_field
        ]
        
        for field in fields:
            field.configure(state='normal')
            field.delete(0, tk.END)
            field.configure(state='readonly')
    
    def validate_inputs(self):
        try:
            a = float(self.a_field.get().replace(',', '.'))
            b = float(self.b_field.get().replace(',', '.'))
            eps = float(self.eps_field.get().replace(',', '.'))
            
            if a >= b:
                tkm.showerror('Ошибка', 'a должно быть меньше b')
                return False
            
            if eps <= 0 or eps >= 1:
                tkm.showerror('Ошибка', 'Точность должна быть в интервале (0, 1)')
                return False
            
            return True
        except ValueError:
            tkm.showerror('Ошибка', 'Введите корректные числовые значения')
            return False
    
    def update_sections(self):
        function_choice = self.radio_var.get()
    
        section = self.find_section(function_choice)[0]
        self.update_idletasks()
        if section:
            self.a_field.delete(0, tk.END)
            self.a_field.insert(0, f'{section[0]:.4f}')
            self.b_field.delete(0, tk.END)
            self.b_field.insert(0, f'{section[1]:.4f}')
            
            self.clear_method_fields()
            
            self.build_graphic()
            
            tkm.showinfo('Информация', 
                        f'Найден отрезок [{section[0]:.4f}; {section[1]:.4f}]\n'
                        f'Значения автоматически подставлены в поля')
        else:
            tkm.showwarning('Предупреждение', 'Не удалось найти подходящий отрезок')
    
    def find_section(self, function_choice, a=0, b=0, step=0.05):
        if b == 0:
            b = a + step
        flag = True
        while flag:
            x = np.linspace(a, b, int((b - a) / step) + 1)
            function_values = self.find_function_values(x, function_choice)
            index = np.where(function_values == 0)[0]
            x = np.round(np.delete(x, index), 5)
            function_values = np.round(np.delete(function_values, index), 5)
            first_derivative = self.find_derivative(x, function_choice)
            second_derivative = self.find_second_derivative(x, function_choice)
            ls = list(zip(function_values, first_derivative, second_derivative, x))
            sections = []
            for i in range(1, len(ls)):
                if ls[i][0] * ls[i - 1][0] < 0 and ls[i][1] * ls[i - 1][1] > 0 and ls[i][2] * ls[i - 1][2] > 0:
                    sections.append((np.round(ls[i - 1][-1], 5), np.round(ls[i][-1], 5)))
                    flag = False
            b += step
        sections = sorted(sections, key=lambda x: abs(x[0] - x[1]))
        return sections
    
    def dihotomia(self, section, eps, function_choice):
        a, b = section
        iterations = 1
        
        fa = self.find_function_values(a, function_choice)
        fb = self.find_function_values(b, function_choice)
        
        if fa * fb > 0:
            raise ValueError("Функция должна иметь разные знаки на концах отрезка")
        
        while True:
            x_mid = (a + b) / 2
            f_mid = self.find_function_values(x_mid, function_choice)
            
            if np.abs(b - a) <= float(eps):
                return np.round(x_mid, 9), iterations
            
            if fa * f_mid <= 0:
                b = x_mid
                fb = f_mid
            else:
                a = x_mid
                fa = f_mid
            
            iterations += 1

    def kas(self, section, eps, function_choice):
        a, b = section
        fa = self.find_function_values(a, function_choice)
        f2a = self.find_second_derivative(a, function_choice)
        xn = a if fa * f2a > 0 else b
        xn_last = xn
        flag = True
        iterations = 1
        while flag:
            if function_choice == 1:
                xn = xn - self.first_function(xn) / self.derivative_of_first_function(xn)
            else:
                xn = xn - self.second_function(xn) / self.derivative_of_second_function(xn)
            if np.abs(xn_last - xn) <= float(eps):
                return np.round(xn, 9), iterations
            xn_last = xn
            iterations += 1

    def hord(self, section, eps, function_choice):
        a, b = section
        fa = self.find_function_values(a, function_choice)
        f2a = self.find_second_derivative(a, function_choice)
        a, b = a if fa * f2a > 0 else b, b if fa * f2a > 0 else a
        bn = b
        bn_last = bn
        flag = True
        iterations = 1
        while flag:
            if function_choice == 1:
                bn = bn - (self.first_function(bn) * (bn - a) / (self.first_function(bn) - self.first_function(a)))
            else:
                bn = bn - (self.second_function(bn) * (bn - a) / (self.second_function(bn) - self.second_function(a)))
            if np.abs(bn_last - bn) <= float(eps):
                return np.round(bn, 9), iterations
            bn_last = bn
            iterations += 1

    def comb(self, section, eps, function_choice):
        a, b = section
        fa = self.find_function_values(a, function_choice)
        f2a = self.find_second_derivative(a, function_choice)
        an = a if fa * f2a > 0 else b
        bn = b if fa * f2a > 0 else a
        a, b = a if fa * f2a > 0 else b, b if fa * f2a > 0 else a
        flag = True
        iterations = 1
        while flag:
            if function_choice == 1:
                an = an - self.first_function(an) / self.derivative_of_first_function(an)
                bn = bn - (self.first_function(bn) * (bn - a) / (self.first_function(bn) - self.first_function(a)))
            else:
                an = an - self.second_function(an) / self.derivative_of_second_function(an)
                bn = bn - (self.second_function(bn) * (bn - a) / (self.second_function(bn) - self.second_function(a)))
            if np.abs(an - bn) <= float(eps):
                return np.round((an + bn) / 2, 9), iterations
            iterations += 1

    def iterat(self, section, eps, function_choice):
        temp_a, temp_b = self.find_section(function_choice, section[0])[0]
        f1a, f1b = self.find_derivative(temp_a, function_choice), self.find_derivative(temp_b, function_choice)
        M = np.ceil(max(f1a, f1b)) if temp_a > 0 else np.floor(max(f1a, f1b))
        a, b = section
        flag = True
        xn = a
        xn_last = xn
        iterations = 1
        while flag:
            if function_choice == 1:
                xn = xn - self.first_function(xn) / M
            else:
                xn = xn - self.second_function(xn) / M
            if np.abs(xn - xn_last) <= float(eps):
                return np.round(xn, 9), iterations
            xn_last = xn
            iterations += 1

    def show_error(self, text):
        tkm.showerror('Ошибка', message=text)
    
    def solve_equation(self):
        if not self.validate_inputs():
            return
        
        function_choice = self.radio_var.get()
        a = float(self.a_field.get().replace(',', '.'))
        b = float(self.b_field.get().replace(',', '.'))
        eps = float(self.eps_field.get().replace(',', '.'))
        
        segment = self.find_section(function_choice, a, b)
        a, b = segment[0][0], segment[0][1]
        fa = self.find_function_values(a, function_choice)
        fb = self.find_function_values(b, function_choice)
        if fa * fb > 0:
            self.show_error('На указанном отрезке может не быть корня.\n')
            return
        
        self.clear_method_fields()
        
        try:
            root, iterations = self.dihotomia((a, b), eps, function_choice)
            self.update_field(self.dihotomia_field, root)
            self.update_field(self.dihotomia_iter_field, iterations)
            
            root, iterations = self.hord((a, b), eps, function_choice)
            self.update_field(self.hord_field, root)
            self.update_field(self.hord_iter_field, iterations)
            
            root, iterations = self.kas((a, b), eps, function_choice)
            self.update_field(self.kas_field, root)
            self.update_field(self.kas_iter_field, iterations)
            
            root, iterations = self.comb((a, b), eps, function_choice)
            self.update_field(self.comb_field, root)
            self.update_field(self.comb_iter_field, iterations)
            
            root, iterations = self.iterat((a, b), eps, function_choice)
            self.update_field(self.iter_field, root)
            self.update_field(self.iter_iter_field, iterations)
            
        except Exception as e:
            tkm.showerror('Ошибка', f'Ошибка при вычислении: {str(e)}')
    
    def update_field(self, field, value):
        field.configure(state='normal')
        field.delete(0, tk.END)
        if isinstance(value, float):
            if abs(value) < 0.0001:
                field.insert(0, f'{value:.6e}')
            else:
                field.insert(0, f'{value:.8f}')
        else:
            field.insert(0, str(value))
        field.configure(state='readonly')
    
    def build_graphic(self):
        if not self.validate_inputs():
            return
        
        function_choice = self.radio_var.get()
        a = float(self.a_field.get().replace(',', '.'))
        b = float(self.b_field.get().replace(',', '.'))
        
        padding = (b - a) * 0.1
        x_min = a - padding
        x_max = b + padding
        
        x = np.linspace(x_min, x_max, 1000)
        y = self.find_function_values(x, function_choice)
        
        self.ax.clear()
        self.ax.plot(x, y, 'b-', linewidth=2, label='f(x)')
        self.ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5, alpha=0.5)
        self.ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5, alpha=0.5)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('x', fontsize=10)
        self.ax.set_ylabel('y', fontsize=10)
        
        if function_choice == 1:
            self.ax.set_title('f(x) = 3ˣ - 2x - 5', fontsize=12)
        else:
            self.ax.set_title('f(x) = 3x⁴ + 8x³ + 6x² - 10', fontsize=12)
        
        self.ax.axvline(x=a, color='r', linestyle='--', alpha=0.5, linewidth=1, label=f'a = {a:.4f}')
        self.ax.axvline(x=b, color='g', linestyle='--', alpha=0.5, linewidth=1, label=f'b = {b:.4f}')
        
        y_min, y_max = np.min(y), np.max(y)
        y_padding = max(0.1, (y_max - y_min) * 0.1)
        self.ax.set_ylim(y_min - y_padding, y_max + y_padding)
        
        self.ax.legend(fontsize=9, loc='best')
        
        self.canvas.draw()
    
    def initUI(self):
        super().initUI()
        self.create_values_fields()
        self.create_functions_choice()
        self.create_buttons()
        self.create_methods_fields()
        self.show_graphic()