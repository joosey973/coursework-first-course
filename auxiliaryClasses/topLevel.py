__all__ = []

import re
import tkinter as tk

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import sympy as sp

from auxiliaryClasses.baseMnk import BaseMNK
import config


class TopLevel(BaseMNK, ctk.CTkToplevel):
    def __init__(self, parent, width, height, window_title):
        super().__init__(parent)
        self.parent = parent
        self.width = width
        self.height = height
        self.window_title = window_title
        self.x_y_list = []
        self.x_y_var = tk.Variable(value=self.x_y_list)
        self.GRAPHIC_FRAME_WIDTH = 400
        self.GRAPHIC_FRAME_HEIGHT = 320
        self.config(bg=config.BACKGROUNG_COLOR)
        self.initTopLevel()

    def create_text_field(self):
        super().create_text_field()
        self.x_label.place(relx=0.095, rely=0.03)
        self.y_label.place(relx=0.227, rely=0.03)

    def create_adding_values(self):
        super().create_adding_values()
        self.x_adding_label.place(relx=0.09, rely=0.64)
        self.y_field.place(relx=0.2, rely=0.7)
        self.y_adding_label.place(relx=0.24, rely=0.64)
        self.remove_btn.place(relx=0.18, rely=0.82)

    def show_graphic(self):
        self.graphic_frame = ctk.CTkFrame(
            self,
            corner_radius=15,
            width=self.GRAPHIC_FRAME_WIDTH,
            height=self.GRAPHIC_FRAME_HEIGHT,
            fg_color=config.BACKGROUND_FRAME,
            bg_color=config.BACKGROUNG_COLOR,
        )
        self.graphic_frame.place(relx=0.62, rely=0.03)

        title_label = ctk.CTkLabel(
            self.graphic_frame,
            text='Аппроксимация методом наименьших квадратов',
            font=('Arial', 15, 'bold'),
            text_color=config.TEXT_COLOR_IN_FRAME,
        )
        title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        self.figure = Figure(figsize=(5.5, 4.5), dpi=65)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('x', fontsize=10)
        self.ax.set_ylabel('y', fontsize=10)
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graphic_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(
            relx=0.5, rely=0.54, anchor=tk.CENTER, width=350, height=270,
        )

    def insert_base_dots(self):
        x = [0.01, 0.02, 0.1, 0.2, 0.34, 0.4, 0.55, 0.6, 0.77, 0.87, 0.9, 1]
        y = [10, 9.2, 8.5, 6.1, 4.3, 3.4, 3.3, 2.5, 2.2, 1.5, 1.1, 0.1]
        self.x_y_list = list(zip(x, y))
        self.update_listbox()

    def create_buttons(self):
        insert_base_dots = ctk.CTkButton(
            self,
            text='Вставить базовые значения в таблицу',
            width=300,
            corner_radius=15,
            command=self.insert_base_dots,
            fg_color=config.BUTTON_COLOR,
            text_color=config.TEXT_COLOR_IN_BTN,
            hover_color=config.HOVER_BUTTON_COLOR,
            bg_color=config.BACKGROUNG_COLOR,
        )
        to_pro_btn = ctk.CTkButton(
            self,
            text='Перейти в Base mode',
            width=300,
            corner_radius=15,
            command=lambda: self.destroy(),
            fg_color=config.BUTTON_COLOR,
            text_color=config.TEXT_COLOR_IN_BTN,
            hover_color=config.HOVER_BUTTON_COLOR,
            bg_color=config.BACKGROUNG_COLOR,
        )

        insert_base_dots.place(relx=0.38, rely=0.82)
        to_pro_btn.place(relx=0.38, rely=0.9)

    def create_function_fields(self):
        approximation_type_label = ctk.CTkLabel(
            self,
            text='Выберите тип аппроксимации',
            font=('Arial', 15, 'bold'),
            text_color=config.TEXT_COLOR_IN_FRAME,
            bg_color=config.BACKGROUNG_COLOR,
        )
        approximation_type_label.place(relx=0.3, rely=0.05)

        self.approximation_type_var = tk.StringVar(
            value='Полиномиальная регрессия',
        )
        self.approximation_type_menu = ctk.CTkOptionMenu(
            self,
            values=[
                'Полиномиальная регрессия',
                'Экспоненциальная регрессия',
                'Логарифмическая регрессия',
                'Дробно-рациональная (общая)',
            ],
            variable=self.approximation_type_var,
            width=340,
            corner_radius=15,
            command=self.on_approximation_type_change,
            bg_color=config.BACKGROUNG_COLOR,
            fg_color=config.BUTTON_COLOR,
            text_color=config.TEXT_COLOR_IN_BTN,
            button_hover_color=config.HOVER_BUTTON_COLOR,
            button_color=config.BUTTON_COLOR,
            dropdown_fg_color=config.TEXT_COLOR_IN_BTN,
            dropdown_hover_color=config.TEXT_COLOR_IN_BTN,
        )
        self.approximation_type_menu.place(relx=0.3, rely=0.12)

        approxima_view_label = ctk.CTkLabel(
            self,
            text='Введите вид аппроксимируемой функции',
            font=('Arial', 15, 'bold'),
            text_color=config.TEXT_COLOR_IN_FRAME,
            bg_color=config.BACKGROUNG_COLOR,
        )
        self.approxima_view_field = ctk.CTkEntry(
            self,
            width=340,
            height=33,
            corner_radius=15,
            fg_color=config.BACKGROUND_FIELD_COLOR,
            text_color=config.TEXT_COLOR_IN_FRAME,
            border_color=config.BORDER_COLOR,
            bg_color=config.BACKGROUNG_COLOR,
        )

        approxima_view_label.place(relx=0.3, rely=0.2)
        self.approxima_view_field.place(relx=0.3, rely=0.27)

        solve_btn = ctk.CTkButton(
            self,
            text='Найти аппроксимируемую функцию',
            corner_radius=15,
            command=self.find_approxima_func,
            fg_color=config.BUTTON_COLOR,
            text_color=config.TEXT_COLOR_IN_BTN,
            hover_color=config.HOVER_BUTTON_COLOR,
            bg_color=config.BACKGROUNG_COLOR,
        )
        solve_btn.place(relx=0.34, rely=0.35)

        approxima_func_label = ctk.CTkLabel(
            self,
            text='Аппроксимируемая функция',
            font=('Arial', 15, 'bold'),
            text_color=config.TEXT_COLOR_IN_FRAME,
            bg_color=config.BACKGROUNG_COLOR,
        )
        self.approxima_func_field = ctk.CTkEntry(
            self,
            width=340,
            height=33,
            corner_radius=15,
            fg_color=config.BACKGROUND_FIELD_COLOR,
            text_color=config.TEXT_COLOR_IN_FRAME,
            border_color=config.BORDER_COLOR,
            bg_color=config.BACKGROUNG_COLOR,
        )

        approxima_func_label.place(relx=0.3, rely=0.43)
        self.approxima_func_field.place(relx=0.3, rely=0.5)
        self.approxima_func_field.configure(state='readonly')

        self.on_approximation_type_change('Полиномиальная регрессия')

    def adjust_font_size(self, text):
        import tkinter.font as tkfont

        max_width = 315
        font_size = 15

        test_font = tkfont.Font(family='Arial', size=font_size)
        text_width = test_font.measure(text)

        while text_width > max_width and font_size > 8:
            font_size -= 1
            test_font.configure(size=font_size)
            text_width = test_font.measure(text)

        self.approxima_func_field.configure(font=('Arial', font_size))

    def on_change_clear(self, txt=''):
        self.ax.clear()
        self.ax.set_xlabel('x', fontsize=10)
        self.ax.set_ylabel('y', fontsize=10)
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()

        self.approxima_func_field.configure(state='normal')
        self.approxima_func_field.delete(0, 'end')
        self.approxima_func_field.insert(0, txt)
        self.approxima_func_field.configure(state='readonly')

    def on_approximation_type_change(self, choice):
        self.on_change_clear()
        if choice == 'Полиномиальная регрессия':
            self.approxima_view_field.configure(state='normal')
            self.approxima_view_field.delete(0, 'end')
            self.approxima_view_field.insert(0, 'a*x + b')
        elif choice == 'Экспоненциальная регрессия':
            self.approxima_view_field.configure(state='normal')
            self.approxima_view_field.delete(0, 'end')
            self.approxima_view_field.insert(0, 'a * exp(-b * x)')
            self.approxima_view_field.configure(state='readonly')
        elif choice == 'Логарифмическая регрессия':
            self.approxima_view_field.configure(state='normal')
            self.approxima_view_field.delete(0, 'end')
            self.approxima_view_field.insert(0, 'a * ln(x) + b')
            self.approxima_view_field.configure(state='readonly')
        elif choice == 'Дробно-рациональная (общая)':
            self.approxima_view_field.configure(state='normal')
            self.approxima_view_field.delete(0, 'end')
            self.approxima_view_field.insert(0, '1/(a*x^2 + b*x + c)')

    def polynomial_approximation(self, func_str):
        try:
            params = self.parse_function(func_str)
            x_sym = sp.Symbol('x')
            param_syms = {p: sp.Symbol(p) for p in params}

            func = sp.sympify(func_str, locals=param_syms)
            x_data, y_data = [], []
            for x, y in self.x_y_list:
                x_data.append(x)
                y_data.append(y)

            basis_sym = [sp.diff(func, param_syms[p]) for p in params]
            basis_num = [sp.lambdify(x_sym, bf, 'numpy') for bf in basis_sym]

            if not self.check_linear_independence(basis_num, x_data):
                return None, None

            n_params = len(params)
            G = [[0 for j in range(n_params)] for i in range(n_params)]
            for i in range(n_params):
                for j in range(n_params):
                    G[i][j] = sum(
                        [basis_num[i](x) * basis_num[j](x) for x in x_data],
                    )

            G_2 = np.array(G)
            if np.linalg.cond(G_2) > 1e10:
                self.show_popup(
                    'Ошибка: вырожденная система уравнений!\nПроверьте,'
                    ' что параметры функции линейно независимы.\n'
                    'Например, запись "a*x^2 + b*x^2" приводит'
                    ' к зависимости параметров.',
                    'error',
                )
                return None, None

            B = [[0] for i in range(n_params)]
            for i in range(n_params):
                B[i][0] = sum(
                    [y * basis_num[i](x) for x, y in zip(x_data, y_data)],
                )

            coefficients = self.matrix_multiplication(
                self.find_reversed_matrix(G), B,
            )
            coefficients = [float(coef[0]) for coef in coefficients]
            return coefficients, params
        except Exception:
            self.show_popup(
                f'Ошибка в синтаксисе функции: {func_str}\n'
                'Проверьте правильность записи.',
                'error',
            )
            self.on_change_clear()
            return None, None

    def exponential_approximation(self):
        x_data, y_data = [], []
        for x, y in self.x_y_list:
            if y <= 0:
                continue

            x_data.append(x)
            y_data.append(y)

        if len(x_data) < 2:
            return None, None

        ln_y_data = [np.log(y) for y in y_data]

        n = len(x_data)
        sum_x = sum(x_data)
        sum_y = sum(ln_y_data)
        sum_xy = sum([x * y for x, y in zip(x_data, ln_y_data)])
        sum_x2 = sum([x**2 for x in x_data])

        det = n * sum_x2 - sum_x**2
        if abs(det) < 1e-10:
            return None, None

        b = -(n * sum_xy - sum_x * sum_y) / det
        ln_a = (sum_y * sum_x2 - sum_x * sum_xy) / det
        a = np.exp(ln_a)

        return [a, b], ['a', 'b']

    def logarithmic_approximation(self):
        x_data, y_data = [], []
        for x, y in self.x_y_list:
            if x <= 0:
                continue

            x_data.append(x)
            y_data.append(y)

        if len(x_data) < 2:
            return None, None

        ln_x_data = [np.log(x) for x in x_data]

        n = len(x_data)
        sum_x = sum(ln_x_data)
        sum_y = sum(y_data)
        sum_xy = sum([x * y for x, y in zip(ln_x_data, y_data)])
        sum_x2 = sum([x**2 for x in ln_x_data])

        det = n * sum_x2 - sum_x**2

        a = (n * sum_xy - sum_x * sum_y) / det
        b = (sum_y * sum_x2 - sum_x * sum_xy) / det

        return [a, b], ['a', 'b']

    def universal_rational_approximation(self, func_str):
        try:
            if '/' not in func_str:
                raise ValueError

            x_sym = sp.Symbol('x')
            params = self.parse_function(func_str)
            param_syms = {p: sp.Symbol(p) for p in params}

            func = sp.sympify(func_str, locals=param_syms)

            numerator, denominator = sp.fraction(func)

            x_data = [x for x, y in self.x_y_list]
            y_data = [y for x, y in self.x_y_list]

            expr = sp.expand(sp.Symbol('y') * denominator - numerator)

            equations = []
            for x_val, y_val in zip(x_data, y_data):
                subs_expr = expr.subs({x_sym: x_val, sp.Symbol('y'): y_val})
                linear_expr = sp.expand(subs_expr)

                equation = []
                for param in params:
                    param_sym = param_syms[param]
                    coeff = linear_expr.coeff(param_sym)
                    equation.append(float(coeff))

                free_term = -float(
                    linear_expr.subs({param_syms[p]: 0 for p in params}),
                )
                equations.append((equation, free_term))

            A = []
            B = []
            for coeffs, free in equations:
                if any(abs(c) > 1e-10 for c in coeffs):
                    A.append(coeffs)
                    B.append(free)

            if len(A) < 2:
                self.show_popup('Недостаточно независимых уравнений', 'error')
                return None, None

            A = np.array(A, dtype=float)
            B = np.array(B, dtype=float)

            coefficients, residuals, rank, s = np.linalg.lstsq(
                A, B, rcond=None,
            )

            first_nonzero = (
                np.argmax(np.abs(coefficients) > 1e-6)
                if len(coefficients) > 0
                else 0
            )
            if first_nonzero < len(coefficients):
                coefficients = coefficients / coefficients[first_nonzero]

            return coefficients.tolist(), params

        except Exception:
            self.show_popup(
                f'Ошибка в синтаксисе функции: {func_str}\n'
                'Проверьте правильность записи.',
                'error',
            )
            self.on_change_clear()
            return None, None

    def check_linear_independence(self, basis_functions, x_data):
        if len(basis_functions) <= 1:
            return True

        n_points = min(len(x_data), 100)
        if n_points < len(basis_functions):
            return True

        indices = np.linspace(0, len(x_data) - 1, n_points, dtype=int)
        x_sample = [x_data[i] for i in indices]

        A = []
        for x in x_sample:
            row = [bf(x) for bf in basis_functions]
            A.append(row)

        A = np.array(A)
        rank = np.linalg.matrix_rank(A, tol=1e-10)

        if rank < len(basis_functions):
            self.show_popup(
                f'Обнаружена линейная зависимость параметров!\n'
                f'Ранг матрицы: {rank}, количество'
                f' параметров: {len(basis_functions)}\n'
                f'Проверьте, что все параметры входят в функцию независимо.',
                'error',
            )
            return False

        return True

    def check_enough_points(self, required_points=2):
        if len(self.x_y_list) < required_points:
            self.show_popup(
                'Недостаточно точек для аппроксимации! Требуется'
                f' минимум {required_points} точек,'
                f' получено {len(self.x_y_list)}',
                'error',
            )
            return False

        return True

    def check_enough_points_for_exponential(self):
        if len(self.x_y_list) < 2:
            self.show_popup(
                'Недостаточно точек для экспоненциальной аппроксимации!'
                f' Требуется минимум 2 точки, получено {len(self.x_y_list)}',
                'error',
            )
            return False

        invalid_points = [(x, y) for x, y in self.x_y_list if y <= 0]
        if invalid_points:
            self.show_popup(
                'Для экспоненциальной регрессии все y должны быть > 0!'
                f' Найдены точки с y <= 0: {invalid_points[:3]}...',
                'error',
            )
            return False

        return True

    def check_enough_points_for_logarithmic(self):
        if len(self.x_y_list) < 2:
            self.show_popup(
                'Недостаточно точек для логарифмической аппроксимации!'
                f' Требуется минимум 2 точки, получено {len(self.x_y_list)}',
                'error',
            )
            return False

        invalid_points = [(x, y) for x, y in self.x_y_list if x <= 0]
        if invalid_points:
            self.show_popup(
                'Для логарифмической регрессии все x должны быть > 0!'
                f' Найдены точки с x <= 0: {invalid_points[:3]}...',
                'error',
            )
            return False

        return True

    def check_enough_points_for_rational(self, func_str):
        if len(self.x_y_list) < 2:
            self.show_popup(
                f'Недостаточно точек для дробно-рациональной аппроксимации!'
                f' Требуется минимум 2 точки, получено {len(self.x_y_list)}',
                'error',
            )
            return False

        params = self.parse_function(func_str)
        n_params = len(params)

        if len(self.x_y_list) < n_params:
            self.show_popup(
                f'Недостаточно точек для определения {n_params} параметров!'
                f' Требуется минимум {n_params} точки,'
                f' получено {len(self.x_y_list)}',
                'error',
            )
            return False

        if len(self.x_y_list) < n_params + 1:
            self.show_popup(
                'Для устойчивости дробно-рациональной аппроксимации'
                ' рекомендуется иметь хотя бы на 1 точку больше, чем'
                f' параметров. Сейчас: {len(self.x_y_list)} точек,'
                f' параметров: {n_params}',
                'warning',
            )

        x_values = [x for x, y in self.x_y_list]
        if len(x_values) != len(set(x_values)):
            self.show_popup(
                'Обнаружены повторяющиеся значения x! Это может'
                ' привести к вырожденности системы',
                'warning',
            )

        return True

    def check_enough_points_for_polynomial(self, func_str):
        if len(self.x_y_list) < 2:
            self.show_popup(
                'Недостаточно точек для полиномиальной аппроксимации!'
                f' Требуется минимум 2 точки, получено {len(self.x_y_list)}',
                'error',
            )
            return False

        params = self.parse_function(func_str)
        n_params = len(params)

        if len(self.x_y_list) < n_params:
            self.show_popup(
                f'Недостаточно точек для определения {n_params} параметров!'
                f' Требуется минимум {n_params}'
                f' точки, получено {len(self.x_y_list)}',
                'error',
            )
            return False

        return True

    def find_approxima_func(self):
        approximation_type = self.approximation_type_var.get()
        func_str_result = ''

        if not self.check_enough_points(2):
            return

        if approximation_type == 'Полиномиальная регрессия':
            func_str = self.approxima_view_field.get()

            if not self.check_enough_points_for_polynomial(func_str):
                self.on_change_clear()
                return

            coefficients, params = self.polynomial_approximation(func_str)

            if coefficients is not None:
                func_str_result = func_str
                for param, coef in zip(params, coefficients):
                    func_str_result = func_str_result.replace(
                        param,
                        f'{coef:.6f}',
                    )

                func_str_result = (
                    func_str_result.replace('+ -', '-')
                    .replace('- -', '+')
                    .replace('+-', '-')
                    .replace('--', '+')
                )
                self.approxima_func_field.configure(state='normal')
                self.approxima_func_field.delete(0, 'end')
                self.approxima_func_field.insert(0, func_str_result)
                self.approxima_func_field.configure(state='readonly')
                self.plot_approximation(func_str_result)

        elif approximation_type == 'Экспоненциальная регрессия':
            if not self.check_enough_points_for_exponential():
                self.on_change_clear()
                return

            coefficients, params = self.exponential_approximation()

            if coefficients is not None:
                a, b = coefficients
                func_str_result = f'{a:.6f} * exp(-{b:.6f} * x)'
                func_str_result = (
                    func_str_result.replace('+ -', '-')
                    .replace('- -', '+')
                    .replace('--', '+')
                    .replace('+-', '-')
                )
                self.approxima_func_field.configure(state='normal')
                self.approxima_func_field.delete(0, 'end')
                self.approxima_func_field.insert(0, func_str_result)
                self.approxima_func_field.configure(state='readonly')
                self.plot_approximation(func_str_result, 'exponential')

        elif approximation_type == 'Логарифмическая регрессия':
            if not self.check_enough_points_for_logarithmic():
                self.on_change_clear()
                return

            coefficients, params = self.logarithmic_approximation()

            if coefficients is not None:
                a, b = coefficients
                func_str_result = f'{a:.6f} * ln(x) + {b:.6f}'
                func_str_result = (
                    func_str_result.replace('+ -', '-')
                    .replace('- -', '+')
                    .replace('--', '+')
                    .replace('+-', '-')
                )
                self.approxima_func_field.configure(state='normal')
                self.approxima_func_field.delete(0, 'end')
                self.approxima_func_field.insert(0, func_str_result)
                self.approxima_func_field.configure(state='readonly')
                self.plot_approximation(func_str_result, 'logarithmic')

        elif approximation_type == 'Дробно-рациональная (общая)':
            func_str = self.approxima_view_field.get()

            if not self.check_enough_points_for_rational(func_str):
                self.on_change_clear()
                return

            coefficients, params = self.universal_rational_approximation(
                func_str,
            )

            if coefficients is not None:
                func_str_result = func_str
                for param, coef in zip(params, coefficients):
                    func_str_result = func_str_result.replace(
                        param,
                        f'{coef:.6f}',
                    )

                func_str_result = (
                    func_str_result.replace('+ -', '-')
                    .replace('- -', '+')
                    .replace('--', '+')
                    .replace('+-', '-')
                )
                self.approxima_func_field.configure(state='normal')
                self.approxima_func_field.delete(0, 'end')
                self.approxima_func_field.insert(0, func_str_result)
                self.approxima_func_field.configure(state='readonly')
                self.plot_approximation(func_str_result, 'rational')

        self.adjust_font_size(func_str_result)

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
            self.on_change_clear()

        self.update_listbox()

    def remove_values(self):
        selected_values = self.values_listbox.curselection()
        if not selected_values:
            self.show_popup('Не выбраны значения для удаления', 'info')
            return

        selected_values = selected_values[0]
        self.x_y_list.pop(selected_values)
        self.update_listbox()
        self.on_change_clear()

    def clear_table(self):
        self.x_y_list = []
        self.update_listbox()
        self.show_graphic()
        self.on_change_clear()

    def calculate_sse(self, func_num, x_data, y_data):
        y_pred = func_num(x_data)
        sse = np.sum((np.array(y_data) - y_pred) ** 2)
        return sse

    def plot_approximation(self, func_str, func_type='polynomial'):
        self.ax.clear()

        x_data, y_data = [], []
        for x, y in self.x_y_list:
            x_data.append(x)
            y_data.append(y)

        self.ax.scatter(
            x_data,
            y_data,
            color='red',
            label='Исходные точки',
            zorder=5,
        )

        try:
            if func_type == 'exponential':
                a, b = self.exponential_approximation()[0]
                x_plot = np.array([val[0] for val in self.x_y_list])
                func_num = lambda x: a * np.exp(-b * x)
                y_plot = func_num(x_plot)

            elif func_type == 'logarithmic':
                a, b = self.logarithmic_approximation()[0]
                x_plot = np.array([val[0] for val in self.x_y_list])

                has_error = False
                for x_val in x_plot:
                    if x_val <= 0:
                        self.show_popup('Ошибка! x должен быть больше 0!')
                        has_error = True
                        break

                if has_error:
                    self.on_change_clear('-')
                    return

                func_num = lambda x: a * np.log(x) + b
                y_plot = func_num(x_plot)

            else:
                x_sym = sp.Symbol('x')
                sympy_func_str = func_str.replace('^', '**')
                func = sp.sympify(sympy_func_str)
                func_num = sp.lambdify(
                    x_sym,
                    func,
                    modules=[
                        'numpy',
                        {'exp': np.exp, 'log': np.log, 'ln': np.log},
                    ],
                )

                x_plot = np.array([val[0] for val in self.x_y_list])
                y_plot = func_num(x_plot)

            def smart_format(value):
                if value == 0 or value < 1e-10:
                    return '0'
                elif value < 0.001:
                    return f'{value:.2e}'
                elif value < 1:
                    return f'{value:.6f}'.rstrip('0').rstrip('.')
                else:
                    return f'{value:.4f}'.rstrip('0').rstrip('.')

            y_pred_at_points = func_num(np.array(x_data))
            sse = np.sum((np.array(y_data) - y_pred_at_points) ** 2)
            sse_formatted = smart_format(sse)
            text_str = f'$\\sum (y_i - f(x_i))^2 = {sse_formatted}$'
            self.ax.plot(
                x_plot,
                y_plot,
                'b-',
                label='Аппроксимация',
                linewidth=2,
            )
            self.ax.text(
                0.5,
                1.04,
                text_str,
                transform=self.ax.transAxes,
                fontsize=10,
                verticalalignment='bottom',
                horizontalalignment='center',
                bbox=dict(
                    boxstyle='round,pad=0.5',
                    facecolor='lightyellow',
                    alpha=0.9,
                    edgecolor='gray',
                    linewidth=1,
                ),
                fontfamily='monospace',
                fontweight='bold',
            )

        except Exception:
            pass

        self.ax.set_xlabel('x', fontsize=10)
        self.ax.set_ylabel('y', fontsize=10)
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.canvas.draw()

    def parse_function(self, func_str):
        func_str = func_str.replace('^', '**')

        params = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', func_str)
        params = list(
            set(
                [
                    p
                    for p in params
                    if p
                    not in [
                        'x',
                        'exp',
                        'sin',
                        'cos',
                        'tan',
                        'log',
                        'sqrt',
                        'ln',
                    ]
                ],
            ),
        )
        params.sort()
        return params

    def centrize_window(self):
        self.parent.update_idletasks()

        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()

        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()

        x = parent_x + (parent_width - self.width) // 2
        y = parent_y + (parent_height - self.height) // 2

        self.geometry(f'{self.width}x{self.height}+{x}+{y}')
        self.resizable(False, False)

    def _setup_window(self):
        self.title(self.window_title)
        self.grab_set()
        self.transient(self.parent)
        self.focus_set()
        self.centrize_window()

    def initTopLevel(self):
        self._setup_window()
        self.create_text_field()
        self.create_adding_values()
        self.show_graphic()
        self.create_buttons()
        self.create_function_fields()
