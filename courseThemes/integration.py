import threading
import tkinter as tk
import tkinter.messagebox as tkm

import customtkinter as ctk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config
from dialogs.loading_dialog import LoadingDialog
from dialogs.runge_dialog import RungeDialog

class Integration(Window):
    def __init__(self, parent, title):
        self.photos = []
        self.methods_fields = []
        self.loading_dialog = None
        self.calculation_thread = None
        self.ax = None
        super().__init__(parent, title, width=1140, height=580)
    
    def integral_func_one(self, x):
        return 1 / np.sqrt(3 * x ** 2 - 2.5)

    def integral_func_two(self, x):
        return np.sqrt(0.3 * x ** 2 + 2.3) / (1.8 + np.sqrt(2 * x - 2.6))
    
    def rectl(self, f, step):
        return step * sum(f[:-1])

    def rectr(self, f, step):
        return step * sum(f[1:])

    def trap(self, f, step):
        return (step / 2) * (f[0] + f[-1] + 2 * sum(f[1:-1]))

    def simp(self, f, step):
        if (len(f) - 1) % 2 != 0:
            return None
        
        return (step / 3) * ((4 * np.sum(f[1:-1:2])) + (2 * np.sum(f[2:-1:2])) + f[0] + f[-1])
    
    def smart_round(self, val, ind):
        if val is None:
            return '-'
        return str(val)[:str(val).find('.') + ind + 1]
        
    def create_values_fields(self):
        values_frame = ctk.CTkFrame(self, corner_radius=15, width=400, height=250)
        values_frame.place(relx=0.02, rely=0.03)
        
        a_label = ctk.CTkLabel(values_frame, text='a:', font=('Arial', 15, 'bold'))
        a_label.place(relx=0.05, rely=0.1)
        
        self.a_field = ctk.CTkEntry(values_frame, font=('Arial', 15, 'bold'), width=200, corner_radius=10)
        self.a_field.place(relx=0.4, rely=0.1)
        
        b_label = ctk.CTkLabel(values_frame, text='b:', font=('Arial', 15, 'bold'))
        b_label.place(relx=0.05, rely=0.4)
        
        self.b_field = ctk.CTkEntry(values_frame, font=('Arial', 15, 'bold'), width=200, corner_radius=10)
        self.b_field.place(relx=0.4, rely=0.4)

        n_label = ctk.CTkLabel(values_frame, text='n:', font=('Arial', 15, 'bold'))
        n_label.place(relx=0.05, rely=0.7)

        self.n_field = ctk.CTkEntry(values_frame, font=('Arial', 15, 'bold'), width=200, corner_radius=10)
        self.n_field.place(relx=0.4, rely=0.7)
    
    def create_methods_fields(self):
        methods_frame = ctk.CTkFrame(self, corner_radius=15, width=400, height=275)
        methods_frame.place(relx=0.02, rely=0.5)

        leftrect_label = ctk.CTkLabel(methods_frame, text='Левые прям-ки:', font=('Arial', 15, 'bold'))
        leftrect_label.place(relx=0.05, rely=0.05)
        
        self.leftrect_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=200, corner_radius=10)
        self.leftrect_field.place(relx=0.45, rely=0.05)

        rightrect_label = ctk.CTkLabel(methods_frame, text='Правые прям-ки:', font=('Arial', 15, 'bold'))
        rightrect_label.place(relx=0.05, rely=0.25)
        
        self.rightrect_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=200, corner_radius=10)
        self.rightrect_field.place(relx=0.45, rely=0.25)

        trap_label = ctk.CTkLabel(methods_frame, text='Трапеция:', font=('Arial', 15, 'bold'))
        trap_label.place(relx=0.05, rely=0.45)

        self.trap_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=200, corner_radius=10)
        self.trap_field.place(relx=0.45, rely=0.45)

        simp_label = ctk.CTkLabel(methods_frame, text='Симпсона:', font=('Arial', 15, 'bold'))
        simp_label.place(relx=0.05, rely=0.65)

        self.simp_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=200, corner_radius=10)
        self.simp_field.place(relx=0.45, rely=0.65)

        nmin_label = ctk.CTkLabel(methods_frame, text='Минимальное n:', font=('Arial', 15, 'bold'))
        nmin_label.place(relx=0.05, rely=0.85)

        self.nmin_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=200, corner_radius=10)
        self.nmin_field.place(relx=0.45, rely=0.85)

        self.leftrect_field.configure(state='readonly')
        self.rightrect_field.configure(state='readonly')
        self.trap_field.configure(state='readonly')
        self.simp_field.configure(state='readonly')
        self.nmin_field.configure(state='readonly')

        self.methods_fields = [(self.leftrect_field, self.rectl),
                               (self.rightrect_field, self.rectr),
                               (self.trap_field, self.trap),
                               ]
    
    def clear_and_update_fields(self):
        function_choice = self.radio_var.get()
        self.ax.set_title(f'График {"первой" if not function_choice else "второй"} функции')
        self.canvas.draw()

        self.ax.clear()
        
        self.ax.set_title(f'График {"первой" if not function_choice else "второй"} функции')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.grid(True)
        
        self.canvas.draw()

        additional_fields = self.methods_fields + [(self.simp_field, ''), (self.nmin_field, '')]
        for field, _ in additional_fields:
            field.configure(state='normal')
            field.delete(0, tk.END)
            field.configure(state='readonly')
        return
    
    def create_integrals(self):
        integral_frame = ctk.CTkFrame(self, corner_radius=15, width=310, height=250)
        integral_frame.place(relx=0.4, rely=0.03)

        self.radio_var = tk.IntVar(value=0)
        first_integral_button = ctk.CTkRadioButton(integral_frame, text='', variable=self.radio_var, value=0, command=self.clear_and_update_fields)
        second_integral_button = ctk.CTkRadioButton(integral_frame, text='', variable=self.radio_var, value=1, command=self.clear_and_update_fields)

        first_integral_button.place(relx=0.05, rely=0.25)
        second_integral_button.place(relx=0.05, rely=0.65)

        canvas1 = tk.Canvas(integral_frame, height=100, width=210, bg='white')
        canvas2 = tk.Canvas(integral_frame, height=100, width=210, bg='white')

        canvas1.place(relx=0.25, rely=0.05)
        canvas2.place(relx=0.25, rely=0.5)

        first_integral = tk.PhotoImage(file=f'{config.MEDIA_ROOT + "integ1.png"}')
        self.photos.append(first_integral)
        canvas1.create_image(105, 55, image=first_integral, anchor=tk.CENTER)

        second_integral = tk.PhotoImage(file=f'{config.MEDIA_ROOT + "integ2.png"}')
        self.photos.append(second_integral)
        canvas2.create_image(105, 55, image=second_integral, anchor=tk.CENTER)
    
    def create_buttons(self):
        BTN_WIDTH = 290
        BTN_HEIGHT = 30

        buttons_frame = ctk.CTkFrame(self, corner_radius=15, width=310, height=275)
        buttons_frame.place(relx=0.4, rely=0.5)

        solve_btn = ctk.CTkButton(buttons_frame, text='Решить интеграл', corner_radius=15, width=BTN_WIDTH, height=BTN_HEIGHT, command=self.solve_integrals)
        solve_btn.place(relx=0.03, rely=0.08)

        nm_solve_btn = ctk.CTkButton(buttons_frame, text='Найти минимальное n', corner_radius=15, width=BTN_WIDTH, height=BTN_HEIGHT, command=self.solve_n_min)
        nm_solve_btn.place(relx=0.03, rely=0.26)

        runge_solve_btn = ctk.CTkButton(buttons_frame, text='Правило Рунге', corner_radius=15, width=BTN_WIDTH, height=BTN_HEIGHT, command=self.runge)
        runge_solve_btn.place(relx=0.03, rely=0.44)

        graphic_btn = ctk.CTkButton(buttons_frame, text='Построить график выбранной функции', corner_radius=15, width=BTN_WIDTH, height=BTN_HEIGHT, command=self.build_graphic)
        graphic_btn.place(relx=0.03, rely=0.62)

        back_to_menu_btn = ctk.CTkButton(buttons_frame, text='Вернуться в меню<', corner_radius=15, width=BTN_WIDTH, height=BTN_HEIGHT, command=lambda func=self.create_new_window: func('Меню'))
        back_to_menu_btn.place(relx=0.03, rely=0.8)
    
    def show_error(self, text):
        tkm.showerror('Ошибка', message=text)
    
    def validate(self, a, b, n=None, eps_num=None):
        if not self.check_is_number(a):
            self.show_error('a должно быть числом!')
            return False
        elif not self.check_is_number(b):
            self.show_error('b должно быть числом!')
            return False
        elif n is not None:
            if not self.check_is_number(n):
                self.show_error('n должно быть числом!')
                return False
            elif not n.isdigit():
                self.show_error('Число n должно быть натуральным!')
                return False

        if not (eps_num is None):
            if not self.check_is_number(eps_num):
                self.show_error('Точность должна быть числом!')
                return False
            if not (0 < float(eps_num) < 1):
                self.show_error('Точность должна ∈ (0; 1)!')
                return False
        
        return True
    
    def get_vals(self, **kwargs):
        if kwargs.get('a_field') is None:
            a_num = self.a_field.get().replace(',', '.')
            b_num = self.b_field.get().replace(',', '.')
            function_choice = self.radio_var.get()
            
            if not kwargs.get('is_n_min'):
                n_num = self.n_field.get().replace(',', '.')

                if not self.validate(a_num, b_num, n_num):
                    raise ValueError
                
                n_num = int(n_num)
            else:
                if not self.validate(a_num, b_num):
                    raise ValueError
        else:
            a_num = kwargs['a_field'].get().replace(',', '.')
            b_num = kwargs['b_field'].get().replace(',', '.')
            n_num = kwargs['n_field'].get().replace(',', '.')
            eps_num = kwargs['eps_field'].get().replace(',', '.')
            if not self.validate(a_num, b_num, n_num, eps_num):
                    raise ValueError

        a_num = float(a_num)
        b_num = float(b_num)
        if kwargs.get('a_field') is not None:
            eps_num = float(eps_num)
            return a_num, b_num, n_num, eps_num
        
        if not kwargs.get('is_n_min'):
            return a_num, b_num, n_num, function_choice

        return a_num, b_num, function_choice
    
    def solve_n_min(self):
        self.clear_and_update_fields()
        self.parent.update_idletasks()
        
        self.loading_dialog = LoadingDialog(self.parent)
        self.loading_dialog.show()
        
        self.calculation_thread = threading.Thread(target=self._calculate_n_min_thread)
        self.calculation_thread.daemon = True
        self.calculation_thread.start()
        
        self._check_calculation_thread()
    
    def _calculate_n_min_thread(self):
        try:
            a, b, function_choice = self.get_vals(is_n_min=True)

            if a >= b:
                self.parent.after(0, lambda: self.show_error('Нижний предел не может быть больше верхнего или равен ему!'))
                self.parent.after(0, self._hide_loading)
                return

            func = self.integral_func_two if function_choice else self.integral_func_one
            left_pointer = 0
            right_pointer = 5000
            n_min = None
            
            iteration = 0
            while left_pointer <= right_pointer and not self.loading_dialog.cancel_flag:
                mid_pointer = (left_pointer + right_pointer) // 2
                mid_pointer = mid_pointer + 1 if mid_pointer % 2 != 0 else mid_pointer
                
                iteration += 1
                if iteration % 10 == 0:
                    self.parent.after(0, lambda mp=mid_pointer: self._update_loading_message(f'Вычисление... Текущее n = {mp}'))
                
                x = np.linspace(a, b, mid_pointer + 1)
                step = (b - a) / mid_pointer
                
                if self.check_odz(x, function_choice) is None:
                    self.parent.after(0, self._hide_loading)
                    return
                
                if self.loading_dialog.cancel_flag:
                    return
                
                func_values = func(x)
                
                leftrect = self.smart_round(self.rectl(func_values, step), 3)
                rightrect = self.smart_round(self.rectr(func_values, step), 3)
                trap = self.smart_round(self.trap(func_values, step), 3)
                simp = self.smart_round(self.simp(func_values, step), 3)

                if leftrect == rightrect == trap == simp:
                    n_min = mid_pointer
                    right_pointer = mid_pointer - 2
                else:
                    if mid_pointer == right_pointer:
                        right_pointer += 50_000
                    left_pointer = mid_pointer + 2

            if not self.loading_dialog.cancel_flag:
                self.parent.after(0, self._update_nmin_field, n_min)
            
        except Exception as e:
            self.parent.after(0, lambda: self.show_error(f'Ошибка при вычислении: {str(e)}'))
        finally:
            self.parent.after(0, self._hide_loading)
    
    def _update_loading_message(self, message):
        if self.loading_dialog:
            self.loading_dialog.update_message(message)
    
    def _update_nmin_field(self, n_min):
        self.nmin_field.configure(state='normal')
        self.nmin_field.delete(0, tk.END)
        self.nmin_field.insert(0, str(n_min if n_min is not None else 'Не найдено'))
        self.nmin_field.configure(state='readonly')
    
    def _hide_loading(self):
        if self.loading_dialog:
            self.loading_dialog.hide()
            self.loading_dialog = None
    
    def _check_calculation_thread(self):
        if self.calculation_thread and self.calculation_thread.is_alive():
            self.parent.after(100, self._check_calculation_thread)
        else:
            self._hide_loading()
    
    def check_odz(self, x, function_choice):
        for val in x:
            if not function_choice:
                if 3 * val ** 2 - 2.5 <= 0:
                    self.show_error('Некорректно введен диапазон (x ∈ (-∞; -0,91) ∪ (0,91; +∞))')
                    return None
            else:
                if 2 * val - 2.6 < 0:
                    self.show_error('Некорректно введен диапазон (x ≥ 1,3)')
                    return None
        
        return True

    def get_full_values(self):
        try:
            a, b, n, function_choice = self.get_vals()
        except ValueError:
            raise ValueError

        if n == 0:
            self.show_error('Число разбиений не может быть равно 0!')
            raise ValueError
        elif a >= b:
            self.show_error('Нижний предел не может быть больше верхнего или равен ему!')
            raise ValueError
        
        return a, b, n, function_choice
    
    def solve_integrals(self):
        self.clear_and_update_fields()
        try:
            a, b, n, function_choice = self.get_full_values()
        except ValueError:
            return

        step = (b - a) / n
        x = np.linspace(a, b, n + 1)
        if self.check_odz(x, function_choice) is None:
            self.clear_and_update_fields()
            return
        
        if not function_choice:  # 0 - первый интеграл, 1 - второй
            func_values = self.integral_func_one(x)
        else:
            func_values = self.integral_func_two(x)
        
        for field in self.methods_fields:
            field[0].configure(state='normal')
            field[0].delete(0, tk.END)
            field[0].insert(0, str(self.smart_round(field[1](func_values, step), 5)))
            field[0].configure(state='readonly')
        
        if n % 2 != 0:
            self.simp_field.configure(state='normal')
            self.simp_field.delete(0, tk.END)
            self.simp_field.insert(0, '-')
            self.simp_field.configure(state='readonly')
        else:
            self.simp_field.configure(state='normal')
            self.simp_field.delete(0, tk.END)
            self.simp_field.insert(0, str(self.smart_round(self.simp(func_values, step), 5)))
            self.simp_field.configure(state='readonly')
    
    def show_graphic(self):
        function_choice = self.radio_var.get()
        self.figure = Figure(figsize=(5, 4), dpi=63)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title(f'График {"первой" if not function_choice else "второй"} функции')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.83, rely=0.5, anchor=tk.CENTER)
    
    def build_graphic(self):
        self.clear_and_update_fields()
        try:
            a, b, n, function_choice = self.get_full_values()
        except ValueError:
            return

        x_ax = np.linspace(a, b, n + 1)
        if self.check_odz(x_ax, function_choice) is None:
            self.clear_and_update_fields()
            return

        func_vals = self.integral_func_one(x_ax) if not function_choice else self.integral_func_two(x_ax)
        self.ax.plot(x_ax, func_vals, color='black')
        self.canvas.draw()

    def runge(self):
        self.loading_dialog = RungeDialog(self.parent)
        self.loading_dialog.show_runge()

    def initUI(self):
        super().initUI()
        self.create_values_fields()
        self.create_methods_fields()
        try:
            self.create_integrals()
        except tk.TclError:
            pass
        self.create_buttons()
        self.show_graphic()


from auxiliaryClasses.window import Window