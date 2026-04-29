import math
import tkinter as tk
import tkinter.messagebox as tkm

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from auxiliaryClasses.baseWindow import BaseWindow

class MNK(BaseWindow):
    def __init__(self, parent, title):
        self.x_y_list = []
        self.x_y_var = tk.Variable(value=self.x_y_list)
        super().__init__(parent, title, width=1300, height=500)
    
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


    def matrix_multiplication(self, A, B):
        result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def matrix_method(self, matrix, result_matrix):
        revMatrix = self.find_reversed_matrix(matrix)
        print(revMatrix)
        if revMatrix is None:
            return
        coefMatrix = self.matrix_multiplication(revMatrix, result_matrix)
        return [val[0] for val in coefMatrix]
    
    def find_linear_coefficients(self, x, y):
        Sx, Sy, Sxy, Sx_2 = [0 for i in range(4)]
        for i in range(len(x)):
            Sx += x[i]
            Sy += y[i]
            Sxy += x[i] * y[i]
            Sx_2 += x[i] ** 2
        n = len(x)
        matrix = [[Sx_2, Sx], [Sx, n]]
        result_matrix = [[Sxy], [Sy]]
        coefs = self.matrix_method(matrix, result_matrix)
        return coefs

    def find_quadratic_coefficients(self, x, y):
        Sx, Sy, Sxy, Sx_2, Sx_2y, Sx_3, Sx_4 = [0 for i in range(7)]
        for i in range(len(x)):
            Sx += x[i]
            Sy += y[i]
            Sxy += x[i] * y[i]
            Sx_2y += x[i] ** 2 * y[i]
            Sx_2 += x[i] ** 2
            Sx_3 += x[i] ** 3
            Sx_4 += x[i] ** 4
        n = len(x)
        matrix = [[Sx_4, Sx_3, Sx_2], [Sx_3, Sx_2, Sx], [Sx_2, Sx, n]]
        result_matrix = [[Sx_2y], [Sxy], [Sy]]
        coefs = self.matrix_method(matrix, result_matrix)
        return coefs

    def find_own_coefficients(self, x, y):
        Sx, Sy, Sxy, Sx_2 = [0 for i in range(4)]
        for i in range(len(x)):
            Sx += x[i]
            Sy += math.log(y[i], math.e)
            Sxy += x[i] * math.log(y[i], math.e)
            Sx_2 += x[i] ** 2
        n = len(x)
        matrix = [[n, Sx], [Sx, Sx_2]]
        result_matrix = [[Sy], [Sxy]]
        coefs = self.matrix_method(matrix, result_matrix)
        if coefs is None:
            return

        coefs[0] = math.e ** coefs[0]
        coefs[1] = -coefs[1]
        return coefs
    
    def find_coefficients(self, x, y):
        linear_coefs = self.find_linear_coefficients(x, y)
        if len(x) > 2:
            quadratic_coefs = self.find_quadratic_coefficients(x, y)
        else:
            quadratic_coefs = None
        exponential_coefs = self.find_own_coefficients(x, y)
        return linear_coefs, quadratic_coefs, exponential_coefs
    
    def create_buttons(self):
        menu_btn = ctk.CTkButton(self, text='Вернуться в меню<', width=200, corner_radius=15, command=lambda: self.create_new_window('Меню'))
        insert_base_dots = ctk.CTkButton(self, text='Вставить базовые значения в таблицу', width=200, corner_radius=15, command=self.insert_base_dots)

        menu_btn.place(relx=0.73, rely=0.82)
        insert_base_dots.place(relx=0.38, rely=0.82)

    def insert_base_dots(self):
        x = [0.01, 0.02, 0.1, 0.2, 0.34, 0.4, 0.55, 0.6, 0.77, 0.87, 0.9, 1]
        y = [10, 9.2, 8.5, 6.1, 4.3, 3.4, 3.3, 2.5, 2.2, 1.5, 1.1, 0.1]
        self.x_y_list = list(zip(x, y))
        self.update_listbox()
        coef1, coef2, coef3 = self.find_coefficients(x, y)
        self.update_functions_fields(coef1, coef2, coef3)
        self.build_graphic(coef1, coef2, coef3)
    
    def get_function(self, coefs, function='polinomial'):
        func = 'y(x) = '
        if function == 'polinomial':
            terms = []
            for i in range(len(coefs) - 1, -1, -1):
                coeff = round(coefs[len(coefs) - i - 1], 3)
                if i == 0:
                    terms.append(f'{coeff}')
                elif i == 1:
                    terms.append(f'{coeff}*x')
                else:
                    terms.append(f'{coeff}*x^{i}')
            func += ' + '.join(terms).replace(' + -', ' - ')
        else:
            func += f'{round(coefs[0], 3)}e^(-{round(coefs[1], 3)}x)'
        func = func.replace('--', '').replace('+ -', '-')
        return func
    
    def get_devitation(self, f):
        diff_squared = 0
        y = [val[1] for val in self.x_y_list]
        for i in range(len(y)):
            diff_squared += (y[i] - f[i]) ** 2
        return round(diff_squared / len(y), 3)

    def update_functions_fields(self, coef1=None, coef2=None, coef3=None):
        func_arr = []

        if coef1 is not None:
            f1 = self.get_function(coef1)
            f11 = [coef1[0] * x_val + coef1[1] for x_val, _ in self.x_y_list]
            func_arr.append(f1)
        else:
            func_arr.append('-')

        if coef2 is not None:
            f2 = self.get_function(coef2)
            f22 = [coef2[0] * x_val ** 2 + coef2[1] * x_val + coef2[2] for x_val, _ in self.x_y_list]
            func_arr.append(f2)
        else:
            func_arr.append('-')
            f22 = None

        if coef3 is not None:
            f3 = self.get_function(coef3, 'exp')
            f33 = [coef3[0] * math.e ** (-coef3[1] * x_val) for x_val, _ in self.x_y_list]
            func_arr.append(f3)
        else:
            func_arr.append('-')

        field_arr = [self.linear_field, self.quadratic_field, self.exponential_field]

        for i in range(len(field_arr)):
            field = field_arr[i]
            answer = func_arr[i]
            field.configure(state='normal')
            field.delete(0, ctk.END)
            field.insert(0, answer)
            field.configure(state='readonly')

        deviation_values = []
        if coef1 is not None:
            deviation_values.append(f11)
        else:
            deviation_values.append(None)

        if f22 is not None:
            deviation_values.append(f22)
        else:
            deviation_values.append(None)

        if coef3 is not None:
            deviation_values.append(f33)
        else:
            deviation_values.append(None)

        deviation_field_arr = [
            self.linear_devitation_field,
            self.quadratic_devitation_field,
            self.exponential_devitation_field
        ]

        for i in range(len(deviation_field_arr)):
            field = deviation_field_arr[i]
            if deviation_values[i] is not None:
                answer = self.get_devitation(deviation_values[i])
            else:
                answer = '-'
            field.configure(state='normal')
            field.delete(0, ctk.END)
            field.insert(0, answer)
            field.configure(state='readonly')
        
    def build_graphic(self, coef1=None, coef2=None, coef3=None):
        self.ax.clear()
        self.ax.grid(True, alpha=0.3)
        if coef1 is not None:
            x_dots = []
            y_dots = []
            for x, y in self.x_y_list:
                x_dots.append(x)
                y_dots.append(y)
            y1 = [coef1[0] * x_val + coef1[1] for x_val, _ in self.x_y_list]
            y2 = [coef2[0] * x_val ** 2 + coef2[1] * x_val + coef2[2] for x_val, _ in self.x_y_list]
            y3 = [coef3[0] * math.e ** (-coef3[1] * x_val) for x_val, _ in self.x_y_list]
            self.ax.plot(x_dots, y1, linewidth=2, label='Линейная регрессия', color='green')
            self.ax.plot(x_dots, y2, linewidth=2, label='Квадратичная регрессия', color='red')
            self.ax.plot(x_dots, y3, linewidth=2, label='Экспоненциальная регрессия', color='black')
            self.ax.scatter(x_dots, y_dots, label='Экспериментальные точки', marker='o', color='blue')
            self.ax.legend()
        self.canvas.draw()

    def show_graphic(self):
        graphic_frame = ctk.CTkFrame(self, corner_radius=15, width=450, height=380)
        graphic_frame.place(relx=0.63, rely=0.03)

        title_label = ctk.CTkLabel(graphic_frame, text='Аппроксимация методом наименьших квадратов', font=('Arial', 15, 'bold'))
        title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        self.figure = Figure(figsize=(5.5, 4.5), dpi=65)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('x', fontsize=10)
        self.ax.set_ylabel('y', fontsize=10)
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.figure, master=graphic_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.5, rely=0.54, anchor=tk.CENTER, width=400, height=320)
    
    def create_answers_fields(self):
        WIDTH = 250
        HEIGHT = 35
        linear_label = ctk.CTkLabel(self, text='Линейная регрессия', font=('Arial', 15, 'bold'))
        quadratic_label = ctk.CTkLabel(self, text='Квадратичная регрессия', font=('Arial', 15, 'bold'))
        exponential_label = ctk.CTkLabel(self, text='Экспоненциальная регрессия', font=('Arial', 15, 'bold'))
        self.linear_field = ctk.CTkEntry(self, width=WIDTH, height=HEIGHT, corner_radius=15)
        self.quadratic_field = ctk.CTkEntry(self, width=WIDTH, height=HEIGHT, corner_radius=15)
        self.exponential_field = ctk.CTkEntry(self, width=WIDTH, height=HEIGHT, corner_radius=15)

        linear_label.place(relx=0.3, rely=0.1)
        quadratic_label.place(relx=0.3, rely=0.3)
        exponential_label.place(relx=0.3, rely=0.5)

        self.linear_field.place(relx=0.3, rely=0.2)
        self.quadratic_field.place(relx=0.3, rely=0.4)
        self.exponential_field.place(relx=0.3, rely=0.6)

        self.linear_field.configure(state='readonly')
        self.quadratic_field.configure(state='readonly')
        self.exponential_field.configure(state='readonly')
    
    def create_deviations_fields(self):
        WIDTH = 100
        HEIGHT = 35
        sum_label = ctk.CTkLabel(self, text='Среднее квадратичное отклонение', wraplength=100, justify=tk.LEFT, font=('Arial', 15, 'bold'))

        self.linear_devitation_field = ctk.CTkEntry(self, width=WIDTH, height=HEIGHT, corner_radius=15)
        self.quadratic_devitation_field = ctk.CTkEntry(self, width=WIDTH, height=HEIGHT, corner_radius=15)
        self.exponential_devitation_field = ctk.CTkEntry(self, width=WIDTH, height=HEIGHT, corner_radius=15)
        
        sum_label.place(relx=0.52, rely=0.05)
        self.linear_devitation_field.place(relx=0.52, rely=0.2)
        self.quadratic_devitation_field.place(relx=0.52, rely=0.4)
        self.exponential_devitation_field.place(relx=0.52, rely=0.6)

        self.linear_devitation_field.configure(state='readonly')
        self.quadratic_devitation_field.configure(state='readonly')
        self.exponential_devitation_field.configure(state='readonly')

    def create_text_field(self):
        self.values_listbox = tk.Listbox(self, width=30, height=15, listvariable=self.x_y_var)
        self.values_listbox.place(relx=0.05, rely=0.1)
        x_label = ctk.CTkLabel(self, text='x', font=('Arial', 15, 'bold'))
        x_label.place(relx=0.091, rely=0.03)
        y_label = ctk.CTkLabel(self, text='y', font=('Arial', 15, 'bold'))
        y_label.place(relx=0.205, rely=0.03)
    
    def create_adding_values(self):
        x_label = ctk.CTkLabel(self, text='x', font=('Arial', 15, 'bold'))
        self.x_field = ctk.CTkEntry(self, width=100, height=37, corner_radius=15)
        self.x_field.place(relx=0.05, rely=0.7)
        x_label.place(relx=0.085, rely=0.64)
        y_label = ctk.CTkLabel(self, text='y', font=('Arial', 15, 'bold'))
        self.y_field = ctk.CTkEntry(self, width=100, height=37, corner_radius=15)
        self.y_field.place(relx=0.18, rely=0.7)
        y_label.place(relx=0.215, rely=0.64)
        add_btn = ctk.CTkButton(self, text='Добавить значения', width=150, corner_radius=15, command=self.add_values)
        add_btn.place(relx=0.025, rely=0.82)
        remove_btn = ctk.CTkButton(self, text='Удалить значения', width=150, corner_radius=15, command=self.remove_values)
        remove_btn.place(relx=0.17, rely=0.82)
        remove_btn = ctk.CTkButton(self, text='Очистить значения', width=150, corner_radius=15, command=self.clear_table)
        remove_btn.place(relx=0.095, rely=0.9)
    
    def clear_main_fields(self):
        functions_arr = [self.linear_field, self.quadratic_field, self.exponential_field]
        dev_arr = [self.linear_devitation_field, self.quadratic_devitation_field, self.exponential_devitation_field]
        for i in range(len(dev_arr)):
            field_1 = functions_arr[i]
            field_2 = dev_arr[i]
            field_1.configure(state='normal')
            field_1.delete(0, ctk.END)
            field_1.configure(state='readonly')
            field_2.configure(state='normal')
            field_2.delete(0, ctk.END)
            field_2.configure(state='readonly')
    
    def clear_table(self):
        self.x_y_list = []
        self.update_listbox()
        self.clear_main_fields()
        self.build_graphic()
    
    def remove_values(self):
        selected_values = self.values_listbox.curselection()
        if not selected_values:
            self.show_popup('Не выбраны значения для удаления', 'info')
            return

        selected_values = selected_values[0]
        self.x_y_list.pop(selected_values)
        self.update_listbox()
        x, y = [], []
        for x_val, y_val in self.x_y_list:
            x.append(x_val)
            y.append(y_val)
        coef1, coef2, coef3 = self.find_coefficients(x, y)
        if x:
            self.update_functions_fields(coef1, coef2, coef3)
        else:
            self.clear_main_fields()
        self.build_graphic(coef1, coef2, coef3)
    
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
        self.update_listbox()
        x, y = [], []
        for x_val, y_val in self.x_y_list:
            x.append(x_val)
            y.append(y_val)
        coef1, coef2, coef3 = self.find_coefficients(x, y)
        self.update_functions_fields(coef1, coef2, coef3)
        self.build_graphic(coef1, coef2, coef3)
    
    def clear_fields(self, warned=False):
        pass
    
    def show_popup(self, text, popup_type='error'):
        if popup_type == 'error':
            self.clear_fields(warned=True)
            tkm.showerror('Ошибка', message=text)
        elif popup_type == 'info':
            tkm.showerror('Информация', message=text)
    
    def update_listbox(self):
        formatted_values = self.format_values()
        self.x_y_var.set(formatted_values)
    
    def format_values(self):
        formatted_list = []
        for x, y in self.x_y_list:
            formatted_list.append('\t' + 5 * ' ' + f'{x:<13}' + '\t' * 4 + f'{y:<13}')
        return formatted_list
    
    def initUI(self):
        self.create_adding_values()
        self.create_text_field()
        self.create_answers_fields()
        self.create_deviations_fields()
        self.create_buttons()
        self.show_graphic()
        return super().initUI()