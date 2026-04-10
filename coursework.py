import threading

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkm
import customtkinter as ctk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config

class LoadingDialog:
    def __init__(self, parent):
        self.parent = parent
        self.dialog = None
        self.progress = None
        self.label = None
        self.cancel_button = None
        self.cancel_flag = False
        
    def show(self, message='Вычисление минимального n...\nЭто может занять некоторое время'):
        self.cancel_flag = False
        
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title('Подождите')
        self.dialog.geometry('350x150')
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (350 // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (150 // 2)
        self.dialog.geometry(f'+{x}+{y}')
        
        self.label = ttk.Label(
            self.dialog, 
            text=message,
            font=('Arial', 11),
            justify=tk.CENTER
        )
        self.label.pack(pady=15)
        
        self.progress = ttk.Progressbar(
            self.dialog,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=10)
        self.progress.start(10)
        
        self.cancel_button = ttk.Button(
            self.dialog,
            text='Отмена',
            command=self.cancel,
        )
        self.cancel_button.pack(pady=10)
        
        self.dialog.protocol('WM_DELETE_WINDOW', lambda: None)
        
        self.dialog.update()
        
    def hide(self):
        if self.dialog:
            if self.progress:
                self.progress.stop()
            self.dialog.destroy()
            self.dialog = None
            
    def cancel(self):
        self.cancel_flag = True
        self.label.config(text='Отмена вычислений...')
        self.cancel_button.config(state='disabled')
        self.dialog.update()
        
    def update_message(self, message):
        if self.dialog and self.label:
            self.label.config(text=message)
            self.dialog.update()


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


class Menu(Window):
    def __init__(self, parent, title):
        super().__init__(parent, title)
    
    def create_buttons_and_label(self):
        theme_label = ctk.CTkLabel(self.parent, text='Выберите тему', font=('Arial', 25, 'bold'))
        theme_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        buttons_texts = ['Интегралы', 'МНК', 'Уравнения', 'МКР', 'Полиномы', 'От автора']
        count = 0
        add_x, add_y = 0.05, 0.3
        for button_text in buttons_texts:
            btn = ctk.CTkButton(self.parent, corner_radius=10, text=button_text, width=200, height=50, 
                          command=lambda text=button_text: self.create_new_window(text))
            btn.place(relx=add_x, rely=add_y)
            count += 1
            add_x += 0.47
            if count == 2:
                add_x = 0.05
                add_y += 0.2
                count = 0
    
    def initUI(self):
        super().initUI()
        self.create_buttons_and_label()


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


class RungeDialog(Integration):
    def __init__(self, parent):
        self.parent = parent
        self.runge_dialog = None
        self.width = 900
        self.height = 550
        self.photos = []
        
        self.METHOD_ORDERS = {
            'rectl': 1,
            'rectr': 1,
            'trap': 2,
            'simp': 4,
        }
        
        self.METHOD_NAMES = {
            'rectl': 'Левые прямоугольники',
            'rectr': 'Правые прямоугольники',
            'trap': 'Метод трапеций',
            'simp': 'Метод Симпсона'
        }
        
        self.METHOD_FIELDS = [
            ('rectl', 'i_n_leftrect_field', 'i_2n_leftrect_field', 'n_leftrect_field'),
            ('rectr', 'i_n_rightrect_field', 'i_2n_rightrect_field', 'n_rightrect_field'),
            ('trap', 'i_n_trap_field', 'i_2n_trap_field', 'n_trap_field'),
            ('simp', 'i_n_simp_field', 'i_2n_simp_field', 'n_simp_field')
        ]
    
    def clear_result_fields(self):
        for cort in self.METHOD_FIELDS:
            for j in cort[1:]:
                field = getattr(self, j)
                field.configure(state='normal', fg_color='#353638')
                field.delete(0, tk.END)
                field.configure(state='readonly')
    
    def calculate_integral(self, method_name, a, b, n, func_choice):
        x = np.linspace(a, b, n + 1)
        step = (b - a) / n
        
        if func_choice == 0:
            func_values = self.integral_func_one(x)
        else:
            func_values = self.integral_func_two(x)
        
        if method_name == 'rectl':
            return self.rectl(func_values, step)
        elif method_name == 'rectr':
            return self.rectr(func_values, step)
        elif method_name == 'trap':
            return self.trap(func_values, step)
        elif method_name == 'simp':
            if n % 2 != 0:
                n += 1
                x = np.linspace(a, b, n + 1)
                step = (b - a) / n
                if func_choice == 0:
                    func_values = self.integral_func_one(x)
                else:
                    func_values = self.integral_func_two(x)
            
            result = self.simp(func_values, step)
            if result is None:
                raise ValueError('Метод Симпсона требует четного числа разбиений')
            return result
    
    def calculate_with_runge_rule(self, method_name, a, b, n, eps, func_choice):
        current_n = n
        max_iterations = 20
        iteration = 0
        k = self.METHOD_ORDERS[method_name]
        
        while iteration < max_iterations:
            x_check = np.linspace(a, b, current_n + 1)
            if self.check_odz_runge(x_check, func_choice) is None:
                return None, None, None, None, float('inf')
            
            i_n = self.calculate_integral(method_name, a, b, current_n, func_choice)
            i_2n = self.calculate_integral(method_name, a, b, current_n * 2, func_choice)
            
            if abs(i_2n) > 1e-10:
                runge_error = abs(i_2n - i_n) / (2**k - 1)
            else:
                runge_error = abs(i_2n - i_n)
            
            improved_value = i_2n + (i_2n - i_n) / (2**k - 1)
            
            if runge_error < eps:
                return i_n, i_2n, current_n, improved_value, runge_error
            
            current_n *= 2
            iteration += 1
        
        return i_n, i_2n, current_n, None, runge_error
    
    def validate(self, a, b, n=None, eps_num=None):
        self.clear_result_fields()
        return super().validate(a, b, n, eps_num)
    
    def calculate_runge(self):
        try:
            a, b, n, eps = self.get_vals(
                a_field=self.a_field,
                b_field=self.b_field,
                n_field=self.n_field,
                eps_field=self.eps_field
            )
        except ValueError:
            return
        
        n = int(n)
        
        if n == 0:
            self.show_error('Число разбиений не может быть равно 0!')
            return
        elif a >= b:
            self.show_error('Нижний предел не может быть больше верхнего или равен ему!')
            return
        
        integral_choice = self.radio_var.get()
        
        self.clear_result_fields()
        
        try:
            x_check = np.linspace(a, b, n + 1)
            if self.check_odz_runge(x_check, integral_choice) is None:
                return
            
            results_summary = []
            
            for method_name, i_n_field_name, i_2n_field_name, n_field_name in self.METHOD_FIELDS:
                i_n_field = getattr(self, i_n_field_name)
                i_2n_field = getattr(self, i_2n_field_name)
                n_field = getattr(self, n_field_name)
                
                try:
                    result = self.calculate_with_runge_rule(
                        method_name, a, b, n, eps, integral_choice
                    )
                    
                    i_n, i_2n, final_n, improved_value, error = result
                    
                    if i_n is None:
                        continue
                    
                    i_n_field.configure(state='normal')
                    i_n_field.delete(0, tk.END)
                    i_n_field.insert(0, f'{i_n:.8f}')
                    i_n_field.configure(state='readonly')
                    
                    i_2n_field.configure(state='normal')
                    i_2n_field.delete(0, tk.END)
                    i_2n_field.insert(0, f'{i_2n:.8f}')
                    
                    if error < eps:
                        i_2n_field.configure(fg_color='green')
                    else:
                        i_2n_field.configure(fg_color='coral')
                    
                    i_2n_field.configure(state='readonly')
                    
                    n_field.configure(state='normal')
                    n_field.delete(0, tk.END)
                    n_field.insert(0, str(final_n))
                    n_field.configure(state='readonly')
                    
                    results_summary.append({
                        'method': self.METHOD_NAMES[method_name],
                        'error': error,
                        'final_n': final_n,
                        'improved_value': improved_value,
                        'i_2n': i_2n,
                        'accuracy_achieved': error < eps
                    })
                    
                except Exception as e:
                    continue
            
            self.show_results_summary(results_summary, eps)
            
        except Exception as e:
            self.show_error(f'Ошибка при вычислении: {str(e)}')
    
    def show_results_summary(self, results, eps):
        if not results:
            self.show_info('Нет результатов для отображения')
            return
        
        summary = 'Результаты применения правила Рунге:\n'
        summary += '=' * 50 + '\n\n'
        
        for result in results:
            summary += f'{result['method']}:\n'
            
            if result['accuracy_achieved']:
                summary += f'  ✓ Точность достигнута при n = {result['final_n']}\n'
                summary += f'  ○ Погрешность: {result['error']:.2e}\n'
                if result['improved_value'] is not None:
                    summary += f'  ○ Уточненное значение: {result['improved_value']:.8f}\n'
            else:
                summary += f'  ✗ Точность НЕ достигнута при n = {result['final_n']}\n'
                summary += f'  ○ Текущая погрешность: {result['error']:.2e}\n'
                summary += f'  ○ Требуемая точность: {eps}\n'
            
            summary += '\n' + '-' * 30 + '\n\n'
        
        tkm.showinfo('Результаты правила Рунге', summary)
    
    def check_odz_runge(self, x, function_choice):
        for val in x:
            if not function_choice:  # Первая функция
                if 3 * val ** 2 - 2.5 <= 0:
                    self.show_error('Некорректно введен диапазон (x ∈ (-∞; -√30/6) ∪ (√30/6; +∞))')
                    return None
            else:  # Вторая функция
                if 2 * val - 2.6 < 0:
                    self.show_error('Некорректно введен диапазон (x ≥ 1,3)')
                    return None
                denominator = 1.8 + np.sqrt(2 * val - 2.6)
                if abs(denominator) < 1e-10:
                    self.show_error('Знаменатель обращается в ноль!')
                    return None
        
        return True
    
    def runge_window_setup(self):
        self.runge_dialog = tk.Toplevel(self.parent)
        self.runge_dialog.title('Правило Рунге')
        self.runge_dialog.geometry(f'{self.width}x{self.height}')
        self.runge_dialog.transient(self.parent)
        self.runge_dialog.grab_set()
        self.runge_dialog.resizable(False, False)
        
        self.runge_dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.width // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.height // 2)
        self.runge_dialog.geometry(f'+{x}+{y}')
        
        self.runge_dialog.protocol('WM_DELETE_WINDOW', lambda: None)
    
    def create_insert_fields(self):
        insert_frame = ctk.CTkFrame(self.runge_dialog, corner_radius=15, width=400, height=250)
        insert_frame.place(relx=0.05, rely=0.03)

        a_label = ctk.CTkLabel(insert_frame, text='a:', font=('Arial', 15, 'bold'))
        a_label.place(relx=0.05, rely=0.1)
        
        self.a_field = ctk.CTkEntry(insert_frame, font=('Arial', 15, 'bold'), width=200, corner_radius=10)
        self.a_field.place(relx=0.4, rely=0.1)
        
        b_label = ctk.CTkLabel(insert_frame, text='b:', font=('Arial', 15, 'bold'))
        b_label.place(relx=0.05, rely=0.32)
        
        self.b_field = ctk.CTkEntry(insert_frame, font=('Arial', 15, 'bold'), width=200, corner_radius=10)
        self.b_field.place(relx=0.4, rely=0.32)

        n_label = ctk.CTkLabel(insert_frame, text='n:', font=('Arial', 15, 'bold'))
        n_label.place(relx=0.05, rely=0.52)

        self.n_field = ctk.CTkEntry(insert_frame, font=('Arial', 15, 'bold'), width=200, corner_radius=10)
        self.n_field.place(relx=0.4, rely=0.52)

        eps_label = ctk.CTkLabel(insert_frame, text='ε (точность):', font=('Arial', 15, 'bold'))
        eps_label.place(relx=0.05, rely=0.75)

        self.eps_field = ctk.CTkEntry(insert_frame, font=('Arial', 15, 'bold'), width=200, corner_radius=10)
        self.eps_field.place(relx=0.4, rely=0.75)

    def create_integrals(self):
        integral_frame = ctk.CTkFrame(self.runge_dialog, corner_radius=15, width=310, height=250)
        integral_frame.place(relx=0.6, rely=0.03)

        self.radio_var = tk.IntVar(value=0)
        first_integral_button = ctk.CTkRadioButton(integral_frame, text='', variable=self.radio_var, value=0, command=self.clear_result_fields)
        second_integral_button = ctk.CTkRadioButton(integral_frame, text='', variable=self.radio_var, value=1, command=self.clear_result_fields)

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

    def create_results_fields(self):
        methods_frame = ctk.CTkFrame(self.runge_dialog, corner_radius=15, width=550, height=200)
        methods_frame.place(relx=0.2, rely=0.53)

        leftrect_label = ctk.CTkLabel(methods_frame, text='Левые прям-ки:', font=('Arial', 15, 'bold'))
        leftrect_label.place(relx=0.05, rely=0.2)
        
        rightrect_label = ctk.CTkLabel(methods_frame, text='Правые прям-ки:', font=('Arial', 15, 'bold'))
        rightrect_label.place(relx=0.05, rely=0.4)

        trap_label = ctk.CTkLabel(methods_frame, text='Трапеция:', font=('Arial', 15, 'bold'))
        trap_label.place(relx=0.05, rely=0.6)

        simp_label = ctk.CTkLabel(methods_frame, text='Симпсона:', font=('Arial', 15, 'bold'))
        simp_label.place(relx=0.05, rely=0.8)

        in_label = ctk.CTkLabel(methods_frame, text='I(n)', font=('Arial', 15, 'bold'))
        in_label.place(relx=0.35, rely=0.05)

        i2n_label = ctk.CTkLabel(methods_frame, text='I(2n)', font=('Arial', 15, 'bold'))
        i2n_label.place(relx=0.55, rely=0.05)

        n_label = ctk.CTkLabel(methods_frame, text='n', font=('Arial', 15, 'bold'))
        n_label.place(relx=0.78, rely=0.05)

        self.i_n_leftrect_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=100, corner_radius=10)
        self.i_n_leftrect_field.place(relx=0.35, rely=0.2)
        
        self.i_2n_leftrect_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=100, corner_radius=10)
        self.i_2n_leftrect_field.place(relx=0.55, rely=0.2)
        
        self.n_leftrect_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=100, corner_radius=10)
        self.n_leftrect_field.place(relx=0.75, rely=0.2)

        self.i_n_rightrect_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=100, corner_radius=10)
        self.i_n_rightrect_field.place(relx=0.35, rely=0.4)

        self.i_2n_rightrect_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=100, corner_radius=10)
        self.i_2n_rightrect_field.place(relx=0.55, rely=0.4)

        self.n_rightrect_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=100, corner_radius=10)
        self.n_rightrect_field.place(relx=0.75, rely=0.4)

        self.i_n_trap_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=100, corner_radius=10)
        self.i_n_trap_field.place(relx=0.35, rely=0.6)

        self.i_2n_trap_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=100, corner_radius=10)
        self.i_2n_trap_field.place(relx=0.55, rely=0.6)

        self.n_trap_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=100, corner_radius=10)
        self.n_trap_field.place(relx=0.75, rely=0.6)

        self.i_n_simp_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=100, corner_radius=10)
        self.i_n_simp_field.place(relx=0.35, rely=0.8)

        self.i_2n_simp_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=100, corner_radius=10)
        self.i_2n_simp_field.place(relx=0.55, rely=0.8)

        self.n_simp_field = ctk.CTkEntry(methods_frame, font=('Arial', 15, 'bold'), width=100, corner_radius=10)
        self.n_simp_field.place(relx=0.75, rely=0.8)

        readonly_fields = [
            self.i_n_simp_field, self.i_n_rightrect_field, self.i_n_trap_field, self.i_n_leftrect_field,
            self.i_2n_simp_field, self.i_2n_rightrect_field, self.i_2n_trap_field, self.i_2n_leftrect_field,
            self.n_simp_field, self.n_rightrect_field, self.n_trap_field, self.n_leftrect_field
        ]
        
        for field in readonly_fields:
            field.configure(state='readonly')

    def create_buttons(self):
        solve_btn = ctk.CTkButton(
            self.runge_dialog, 
            text='Применить правило Рунге', 
            height=30,
            width=200,
            corner_radius=15,
            command=self.calculate_runge
        )
        solve_btn.place(relx=0.3, rely=0.92)

        return_btn = ctk.CTkButton(
            self.runge_dialog, 
            text='Вернуться', 
            height=30,
            width=150,
            corner_radius=15,
            command=self.back
        )
        return_btn.place(relx=0.55, rely=0.92)

    def back(self):
        if self.runge_dialog:
            self.runge_dialog.destroy()
            self.runge_dialog = None

    def show_runge(self):
        self.runge_window_setup()
        self.create_insert_fields()
        try:
            self.create_integrals()
        except tk.TclError:
            pass
        self.create_results_fields()
        self.create_buttons()
    
    def show_error(self, text):
        tkm.showerror('Ошибка', message=text)
    
    def show_info(self, message):
        tkm.showinfo('Информация', message)


class Equation(Window):
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
    
    def find_section(self, function_choice, a=0, step=0.05):
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
            print(xn)
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


class Polinom(Window):
    def __init__(self, parent, title):
        super().__init__(parent, title, width=800, height=700)


def main():
    menu_root = tk.Tk()
    menu_app = Menu(menu_root, 'Курсовая работа - Меню')
    menu_root.mainloop()


if __name__ == '__main__':
    main()