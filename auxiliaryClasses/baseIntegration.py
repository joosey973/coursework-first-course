import numpy as np

from auxiliaryClasses.baseWindow import BaseWindow


class BaseIntegration(BaseWindow):
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