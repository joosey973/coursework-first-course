import tkinter as tk
import tkinter.messagebox as tkm

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from auxiliaryClasses.baseWindow import BaseWindow

class Polinom(BaseWindow):
    def __init__(self, parent, title):
        self.x_y_list = []
        self.x_y_var = tk.Variable(value=self.x_y_list)
        self.polinoms_fields = {}
        self.kanon_res = []
        super().__init__(parent, title, width=1000, height=500)
    
    def find_minor(self, matrix, row, col):
        matrix = [cop[:] for cop in matrix]
        del matrix[row]
        for i in range(len(matrix)):
            matrix[i] = matrix[i][:col] + matrix[i][col + 1:]
        return matrix
    
    def find_determinante(self, matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        summa = 0
        for j in range(len(matrix)):
            summa += matrix[0][j] * (-1) ** j * self.find_determinante(self.find_minor(matrix, 0, j))
        return summa

    def find_reversed_matrix(self, matrix, det=None):
        if det is None:
            det = self.find_determinante(matrix)
        
        if det == 0:
            return

        arr = []
        for i in range(len(matrix)):
            temp = []
            for j in range(len(matrix)):
                alg_dop = (-1) ** (i + j) * self.find_determinante(self.find_minor(matrix, i, j))
                temp.append(alg_dop)
            arr.append(temp)
        rev_arr = list(map(lambda x: [i / det for i in x], zip(*arr)))
        return rev_arr
    
    def create_matrix(self, x, y=None):
        matrix = []
        if y is None:
            for i in range(len(x)):
                temp = []
                for j in range(len(x)):
                    temp.append(x[i] ** j)
                matrix.append(temp)
        return matrix
    
    def kanon_polinom(self, x, y):
        A = self.create_matrix(x)
        detA = self.find_determinante(A)
        revA = self.find_reversed_matrix(A, detA)
        if revA is None:
            return

        C = []
        for i in range(len(revA)):
            summa = 0
            for j in range(len(revA)):
                summa += revA[i][j] * y[j]
            C.append(summa)
        return C
    
    def kramer_polinom(self, x, y):
        A = self.create_matrix(x)
        detA = self.find_determinante(A)
        determinates = []
        for i in range(len(A)):
            matrix = [el[:] for el in A]
            for j in range(len(A)):
                matrix[j][i] = y[j]
            determinates.append(self.find_determinante(matrix))
        C = [det / detA for det in determinates]
        return C
    
    def lagrange_polinom(self, x, y, x_dot):
        def lagrange_basis(x, y, i, x_val):
            li = 1
            for j in range(len(x)):
                if j != i:
                    li *= (x_val - x[j]) / (x[i] - x[j])
            return li

        def interpolate(x, y, x_val):
            result = 0
            for i in range(len(x)):
                result += y[i] * lagrange_basis(x, y, i, x_val)
            return result
        
        result = interpolate(x, y, x_dot)
        return round(result, 3)
    
    def newton_polinom(self, x, y, x_dot):
        is_const_h = True
        past_h = x[1] - x[0]
        for i in range(3, len(x)):
            if abs(x[i] - x[i - 1] - past_h) > 1e-10:
                is_const_h = False
                break
        if not is_const_h:
            return
        
        n = len(y)
        diff_table = [y.copy()]
        
        for order in range(1, n):
            prev_row = diff_table[order - 1]
            new_row = []
            for i in range(len(prev_row) - 1):
                new_row.append(prev_row[i + 1] - prev_row[i])
            diff_table.append(new_row)
        
        h = x[1] - x[0]
        t = (x_dot - x[0]) / h
        
        result = y[0]
        term = 1
        
        for k in range(1, n):
            term = term * (t - (k - 1)) / k
            result += diff_table[k][0] * term
        
        return round(result, 3)

    def create_text_field(self):
        self.values_listbox = tk.Listbox(self, width=30, height=15, listvariable=self.x_y_var)
        self.values_listbox.place(relx=0.05, rely=0.1)
        x_label = ctk.CTkLabel(self, text='x', font=('Arial', 15, 'bold'))
        x_label.place(relx=0.1, rely=0.03)
        y_label = ctk.CTkLabel(self, text='y', font=('Arial', 15, 'bold'))
        y_label.place(relx=0.25, rely=0.03)
    
    def create_adding_values(self):
        x_label = ctk.CTkLabel(self, text='x', font=('Arial', 15, 'bold'))
        self.x_field = ctk.CTkEntry(self, width=100, height=37, corner_radius=15)
        self.x_field.place(relx=0.05, rely=0.7)
        x_label.place(relx=0.094, rely=0.64)
        y_label = ctk.CTkLabel(self, text='y', font=('Arial', 15, 'bold'))
        self.y_field = ctk.CTkEntry(self, width=100, height=37, corner_radius=15)
        self.y_field.place(relx=0.22, rely=0.7)
        y_label.place(relx=0.264, rely=0.64)
        add_btn = ctk.CTkButton(self, text='Добавить значения', width=150, corner_radius=15, command=self.add_values)
        add_btn.place(relx=0.115, rely=0.82)
        remove_btn = ctk.CTkButton(self, text='Удалить значения', width=150, corner_radius=15, command=self.remove_values)
        remove_btn.place(relx=0.115, rely=0.9)
    
    def point_equation(self):
        point_label = ctk.CTkLabel(self, text='x0', font=('Arial', 15, 'bold'))
        self.point_field = ctk.CTkEntry(self, width=100, height=37, corner_radius=15)
        self.point_field.place(relx=0.45, rely=0.7)
        point_label.place(relx=0.49, rely=0.64)
        solve_btn = ctk.CTkButton(self, text='Посчитать полином в точке', width=150, corner_radius=15, command=self.solve_polinom)
        solve_btn.place(relx=0.395, rely=0.82)
        menu_btn = ctk.CTkButton(self, text='Вернуться в меню<', 
                                          corner_radius=15, width=150,
                                          command=lambda: self.create_new_window('Меню'))
        menu_btn.place(relx=0.72, rely=0.82)
    
    def kanon_in_dot(self, x, y, x_dot, pol_type='kanon'):
        if pol_type == 'kanon':
            kanon_coef = self.kanon_polinom(x, y)
        else:
            kanon_coef = self.kramer_polinom(x, y)
        result = kanon_coef[0]
        for i in range(1, len(kanon_coef)):
                result += kanon_coef[i] * x_dot ** i
        return round(result, 3)
    
    def solve_polinom(self):
        if len(self.x_y_list) == 1:
            self.show_popup('Нельзя посчитать значения в точке, тк не построен полином!')
            return
        
        x_dot = self.point_field.get().replace(',', '.')
        if not self.check_is_number(x_dot):
            self.show_popup('x_dot не число!')
            return
        
        if not self.x_y_list:
            x = [-1, -0.5, 0, 0.5, 1, 1.5]
            y = [0, 2, ъ, -4, 3, 7]
            self.x_y_list = list(zip(x, y))
            self.update_listbox()
            self.update_polinom_field()
            self.update_idletasks()

        x = [i[0] for i in self.x_y_list]
        y = [i[1] for i in self.x_y_list]
        x_dot = float(x_dot)
        kanon_res_matr = self.kanon_in_dot(x, y, x_dot)
        kanon_res_kram = self.kanon_in_dot(x, y, x_dot, 'krammer')
        lagrange_res = self.lagrange_polinom(x, y, x_dot)
        newton_res = self.newton_polinom(x, y, x_dot)
        newton_res = '-' if newton_res is None else newton_res
        results = [kanon_res_matr, kanon_res_kram, lagrange_res, newton_res]
        keys = list(self.polinoms_fields.keys())
        for i in range(len(results)):
            keys[i].configure(state='normal')
            keys[i].delete(0, ctk.END)
            keys[i].insert(0, str(results[i]))
            keys[i].configure(state='readonly')
    
    def remove_values(self):
        selected_values = self.values_listbox.curselection()
        if not selected_values:
            self.show_popup('Не выбраны значения для удаления', 'info')
            return

        selected_values = selected_values[0]
        self.x_y_list.pop(selected_values)
        self.clear_fields()
        self.update_listbox()
        self.update_polinom_field()
    
    def add_values(self):
        x = self.x_field.get().replace(',', '.')
        y = self.y_field.get().replace(',', '.')
        if not self.check_is_number(x):
            self.show_popup('x не число!')
            return

        if not self.check_is_number(y):
            self.show_popup('y не число!')
            return

        x, y = float(x), float(y)
        is_warned = False
        if x in [i[0] for i in self.x_y_list]:
            self.show_popup('Такая точка x уже добавлена в список!', 'info')
            is_warned = True
        if not is_warned:
            self.x_y_list.append((x, y))
            self.x_y_list = sorted(self.x_y_list, key=lambda cort: cort[0])
            self.clear_fields()
        else:
            self.clear_fields(warned=True)
        self.update_polinom_field()
        self.update_listbox()
        
    
    def update_listbox(self):
        formatted_values = self.format_values()
        self.x_y_var.set(formatted_values)
    
    def format_values(self):
        formatted_list = []
        for x, y in self.x_y_list:
            formatted_list.append('\t' + 5 * ' ' + f'{x:<15}' + '\t' * 4 + f'{y:<15}')
        return formatted_list

    def create_polinom_formule_field(self):
        self.polinom_formule_field = ctk.CTkEntry(self, width=300, height=37, corner_radius=15)
        self.polinom_formule_field.configure(state='readonly')
        self.polinom_formule_field.place(relx=0.65, rely=0.7)
        polinom_formule_label = ctk.CTkLabel(self, text='Формула полинома', font=('Arial', 15, 'bold'))
        polinom_formule_label.place(relx=0.725, rely=0.64)
    
    def clear_fields(self, warned=False):
        self.polinom_formule_field.configure(state='normal')
        self.polinom_formule_field.delete(0, ctk.END)
        self.polinom_formule_field.configure(state='readonly')
        
        self.ax.clear()
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()
        if not warned:
            for field in self.polinoms_fields.keys():
                field.configure(state='normal')
                field.delete(0, ctk.END)
                field.configure(state='readonly')
        self.update_polinom_field()
        self.update_listbox()

    def update_polinom_field(self):
        x = [i[0] for i in self.x_y_list]
        y = [i[1] for i in self.x_y_list]
        self.kanon_res = self.kanon_polinom(x, y)
        if self.kanon_res is not None:
            terms = []
            for i in range(len(x) - 1, -1, -1):
                coeff = round(self.kanon_res[i], 3)
                if i == 0:
                    terms.append(f'{coeff}')
                elif i == 1:
                    terms.append(f'{coeff}*x')
                else:
                    terms.append(f'{coeff}*x^{i}')
            
            polinom = f'P{len(self.kanon_res) - 1}(x)=' + ' + '.join(terms).replace(' + -', ' - ')
        else:
            polinom = ''
        self.adjust_font_size(polinom)
        self.polinom_formule_field.configure(state='normal')
        self.polinom_formule_field.delete(0, ctk.END)
        self.polinom_formule_field.insert(0, polinom)
        self.polinom_formule_field.configure(state='readonly')
        self.update_function()
        self.update_idletasks()
    
    def adjust_font_size(self, text):
        import tkinter.font as tkfont
        
        max_width = 275
        font_size = 15
        
        test_font = tkfont.Font(family='Arial', size=font_size)
        text_width = test_font.measure(text)
        
        while text_width > max_width and font_size > 8:
            font_size -= 1
            test_font.configure(size=font_size)
            text_width = test_font.measure(text)
        
        self.polinom_formule_field.configure(font=('Arial', font_size))

    def update_function(self):
        import numpy as np

        if self.x_y_list:
            x_dots = [i[0] for i in self.x_y_list]
            y_dots = [i[1] for i in self.x_y_list]
            x0, xk = self.x_y_list[0][0], self.x_y_list[-1][0]
            x = np.linspace(x0, xk, 1000)
            y = []
            for x_val in x:
                temp_x = self.kanon_res[0]
                for i in range(1, len(self.kanon_res)):
                    temp_x += self.kanon_res[i] * x_val ** i
                y.append(temp_x)
            
            self.ax.clear()
            self.ax.grid(True, alpha=0.3)
            self.ax.plot(x, y, 'b-', linewidth=2, label='Интерполяционный полином')
            self.ax.scatter(x_dots, y_dots, label='Узлы интерполяции', marker='o', color='red')
            self.ax.legend()
            self.canvas.draw()
        else:
            self.ax.clear()
            self.ax.grid(True, alpha=0.3)
            self.canvas.draw()
    
    def create_polinoms_fields(self):
        self.kanon_field_matr = ctk.CTkEntry(self, width=100, height=37, corner_radius=15)
        self.kanon_field_kram = ctk.CTkEntry(self, width=100, height=37, corner_radius=15)
        self.lagrange_field = ctk.CTkEntry(self, width=100, height=37, corner_radius=15)
        self.newton_field = ctk.CTkEntry(self, width=100, height=37, corner_radius=15)

        if not self.polinoms_fields:
            self.polinoms_fields = {self.kanon_field_matr: ctk.CTkLabel(self, text='Канонический полином (Матричный)', font=('Arial', 15, 'bold'), wraplength=100, justify=tk.LEFT),
                                    self.kanon_field_kram: ctk.CTkLabel(self, text='Канонический полином (Краммер)', font=('Arial', 15, 'bold'), wraplength=100, justify=tk.LEFT),
                                    self.lagrange_field: ctk.CTkLabel(self, text='Полином Лагранжа', font=('Arial', 15, 'bold'), wraplength=100, justify=tk.LEFT),
                                    self.newton_field: ctk.CTkLabel(self, text='Полином Ньютона', font=('Arial', 15, 'bold'), wraplength=100, justify=tk.LEFT)
            }

        for field in self.polinoms_fields.keys():
            field.configure(state='readonly')

        offset_y = 0
        for field, label in self.polinoms_fields.items():
            field.place(relx=0.48, rely=0.15 + offset_y)
            label.place(relx=0.35, rely=0.15 + offset_y)
            offset_y += 0.12
    
    def show_graphic(self):
        graphic_frame = ctk.CTkFrame(self, corner_radius=15, width=350, height=310)
        graphic_frame.place(relx=0.6, rely=0.03)

        title_label = ctk.CTkLabel(graphic_frame, text='График функции', font=('Arial', 15, 'bold'))
        title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        self.figure = Figure(figsize=(5.5, 4.5), dpi=60)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('x', fontsize=10)
        self.ax.set_ylabel('y', fontsize=10)
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.figure, master=graphic_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.5, rely=0.54, anchor=tk.CENTER, width=320, height=260)
    
    def show_popup(self, text, popup_type='error'):
        if popup_type == 'error':
            self.clear_fields(warned=True)
            tkm.showerror('Ошибка', message=text)
        elif popup_type == 'info':
            tkm.showerror('Информация', message=text)
    
    def initUI(self):
        self.create_text_field()
        self.create_adding_values()
        self.point_equation()
        self.create_polinom_formule_field()
        self.create_polinoms_fields()
        self.show_graphic()
        return super().initUI()