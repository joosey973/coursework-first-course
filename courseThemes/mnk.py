import math
import tkinter as tk

import customtkinter as ctk

from auxiliaryClasses.baseWindow import BaseWindow
from auxiliaryClasses.baseMnk import BaseMNK
from auxiliaryClasses.topLevel import TopLevel

class MNK(BaseMNK, BaseWindow):
    def __init__(self, parent, title):
        self.x_y_list = []
        self.x_y_var = tk.Variable(value=self.x_y_list)
        super().__init__(parent, title, width=1300, height=500)
    
    def matrix_method(self, matrix, result_matrix):
        revMatrix = self.find_reversed_matrix(matrix)
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
        menu_btn = ctk.CTkButton(self, text='Вернуться в меню<', width=300, corner_radius=15, command=lambda: self.create_new_window('Меню'))
        insert_base_dots = ctk.CTkButton(self, text='Вставить базовые значения в таблицу', width=300, corner_radius=15, command=self.insert_base_dots)
        to_pro_btn = ctk.CTkButton(self, text='Перейти в Pro mode', width=300, corner_radius=15, command=self.to_pro_mode)

        menu_btn.place(relx=0.69, rely=0.82)
        insert_base_dots.place(relx=0.38, rely=0.82)
        to_pro_btn.place(relx=0.38, rely=0.9)
    
    def to_pro_mode(self):
        pro_mode_topLevel = TopLevel(self, self.width - 150, self.height, 'Аппроксимация Pro')
        self.wait_window(pro_mode_topLevel)
    
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
    
    def initUI(self):
        self.create_adding_values()
        self.create_text_field()
        self.create_answers_fields()
        self.create_deviations_fields()
        self.create_buttons()
        self.show_graphic()
        return super().initUI()