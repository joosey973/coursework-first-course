import tkinter as tk
import tkinter.messagebox as tkm

import numpy as np
import customtkinter as ctk

import config
from courseThemes.integration import Integration


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