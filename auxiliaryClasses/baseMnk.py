
import tkinter as tk
import tkinter.messagebox as tkm

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from auxiliaryClasses.baseWindow import BaseMethods

class BaseMNK(BaseMethods):
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
    
    def insert_base_dots(self):
        x = [0.01, 0.02, 0.1, 0.2, 0.34, 0.4, 0.55, 0.6, 0.77, 0.87, 0.9, 1]
        y = [10, 9.2, 8.5, 6.1, 4.3, 3.4, 3.3, 2.5, 2.2, 1.5, 1.1, 0.1]
        self.x_y_list = list(zip(x, y))
        self.update_listbox()
        coef1, coef2, coef3 = self.find_coefficients(x, y)
        self.update_functions_fields(coef1, coef2, coef3)
        self.build_graphic(coef1, coef2, coef3)
    
    def get_devitation(self, f):
        diff_squared = 0
        y = [val[1] for val in self.x_y_list]
        for i in range(len(y)):
            diff_squared += (y[i] - f[i]) ** 2
        return round(diff_squared, 3)
    
    def show_graphic(self):
        self.GRAPHIC_FRAME_WIDTH = 450
        self.GRAPHIC_FRAME_HEIGHT = 380
        self.graphic_frame = ctk.CTkFrame(self, corner_radius=15, width=self.GRAPHIC_FRAME_WIDTH, height=self.GRAPHIC_FRAME_HEIGHT)
        self.graphic_frame.place(relx=0.63, rely=0.03)

        title_label = ctk.CTkLabel(self.graphic_frame, text='Аппроксимация методом наименьших квадратов', font=('Arial', 15, 'bold'))
        title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        self.figure = Figure(figsize=(5.5, 4.5), dpi=65)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('x', fontsize=10)
        self.ax.set_ylabel('y', fontsize=10)
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graphic_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.5, rely=0.54, anchor=tk.CENTER, width=400, height=320)
    
    def create_text_field(self):
        self.values_listbox = tk.Listbox(self, width=30, height=15, listvariable=self.x_y_var)
        self.values_listbox.place(relx=0.05, rely=0.1)
        self.x_label = ctk.CTkLabel(self, text='x', font=('Arial', 15, 'bold'))
        self.x_label.place(relx=0.091, rely=0.03)
        self.y_label = ctk.CTkLabel(self, text='y', font=('Arial', 15, 'bold'))
        self.y_label.place(relx=0.205, rely=0.03)
    
    def create_adding_values(self):
        self.x_adding_label = ctk.CTkLabel(self, text='x', font=('Arial', 15, 'bold'))
        self.x_field = ctk.CTkEntry(self, width=100, height=37, corner_radius=15)
        self.x_field.place(relx=0.05, rely=0.7)
        self.x_adding_label.place(relx=0.085, rely=0.64)
        
        self.y_adding_label = ctk.CTkLabel(self, text='y', font=('Arial', 15, 'bold'))
        self.y_field = ctk.CTkEntry(self, width=100, height=37, corner_radius=15)
        self.y_field.place(relx=0.18, rely=0.7)
        self.y_adding_label.place(relx=0.215, rely=0.64)

        self.add_btn = ctk.CTkButton(self, text='Добавить значения', width=150, corner_radius=15, command=self.add_values)
        self.add_btn.place(relx=0.025, rely=0.82)
        self.remove_btn = ctk.CTkButton(self, text='Удалить значения', width=150, corner_radius=15, command=self.remove_values)
        self.remove_btn.place(relx=0.17, rely=0.82)
        self.clear_btn = ctk.CTkButton(self, text='Очистить значения', width=150, corner_radius=15, command=self.clear_table)
        self.clear_btn.place(relx=0.095, rely=0.9)
    
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
        self.update_listbox()
        x, y = [], []
        for x_val, y_val in self.x_y_list:
            x.append(x_val)
            y.append(y_val)
        coef1, coef2, coef3 = self.find_coefficients(x, y)
        self.update_functions_fields(coef1, coef2, coef3)
        self.build_graphic(coef1, coef2, coef3)
    
    def show_popup(self, text, popup_type='error'):
        if popup_type == 'error':
            self.clear_fields(warned=True)
            tkm.showerror('Ошибка', message=text)
        elif popup_type == 'info':
            tkm.showerror('Информация', message=text)
    
    def clear_fields(self, warned=False):
        pass

    def update_listbox(self):
        formatted_values = self.format_values()
        self.x_y_var.set(formatted_values)
    
    def format_values(self):
        formatted_list = []
        for x, y in self.x_y_list:
            formatted_list.append('\t' + 5 * ' ' + f'{x:<13}' + '\t' * 4 + f'{y:<13}')
        return formatted_list