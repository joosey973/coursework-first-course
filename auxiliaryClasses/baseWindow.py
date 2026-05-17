__all__ = []

import tkinter as tk

import config


class BaseMethods:
    def check_is_number(self, number):
        try:
            float(number)
            return True
        except ValueError:
            return False

    def matrix_multiplication(self, A, B):
        result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]

        return result

    def create_matrix(self, n=None, *coefs, x=None):
        if coefs:
            matrix = [[0 for j in range(n + 1)] for i in range(n + 1)]
            A, C, B, F = coefs[0]
            matrix[0][0] = -C[0]
            count = 0
            for i in range(1, n):
                matrix[i][count] = A[i]
                matrix[i][count + 1] = -C[i]
                matrix[i][count + 2] = B[i]
                count += 1

            matrix[-1][-1] = -C[-1]
        else:
            matrix = []
            for i in range(len(x)):
                temp = []
                for j in range(len(x)):
                    temp.append(x[i] ** j)

                matrix.append(temp)

            return matrix

        return matrix

    def kanon_polinom(self, x, y):
        A = self.create_matrix(x=x)
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
        A = self.create_matrix(x=x)
        detA = self.find_determinante(A)
        determinates = []
        for i in range(len(A)):
            matrix = [el[:] for el in A]
            for j in range(len(A)):
                matrix[j][i] = y[j]

            determinates.append(self.find_determinante(matrix))

        C = [det / detA for det in determinates]
        return C

    def find_minor(self, matrix, row, col):
        matrix = [cop[:] for cop in matrix]
        del matrix[row]
        for i in range(len(matrix)):
            matrix[i] = matrix[i][:col] + matrix[i][col + 1 :]

        return matrix

    def find_determinante(self, matrix):
        if len(matrix) == 1:
            return matrix[0][0]

        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

        summa = 0
        for j in range(len(matrix)):
            summa += (
                matrix[0][j]
                * (-1) ** j
                * self.find_determinante(self.find_minor(matrix, 0, j))
            )

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
                alg_dop = (-1) ** (i + j) * self.find_determinante(
                    self.find_minor(matrix, i, j),
                )
                temp.append(alg_dop)

            arr.append(temp)

        rev_arr = list(map(lambda x: [i / det for i in x], zip(*arr)))
        return rev_arr


class BaseWindow(BaseMethods, tk.Frame):
    def __init__(self, parent, title, width=500, height=400, x=None, y=None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.width = width
        self.height = height
        self.title = title
        self.x = x
        self.y = y
        self.pack(fill=tk.BOTH, expand=True)
        self.parent.config(bg=config.BACKGROUNG_COLOR)
        self.config(bg=config.BACKGROUNG_COLOR)
        self.initUI()

    def create_new_window(self, window_name, x=None, y=None):
        from auxiliaryClasses.menu import Menu
        from courseThemes.equation import Equation
        from courseThemes.integration import Integration
        from courseThemes.mkr import MKR
        from courseThemes.mnk import MNK
        from courseThemes.polinom import Polinom
        from settings import Settings

        window_classes = {
            "Интегралы": Integration,
            "Уравнения": Equation,
            "Полиномы": Polinom,
            "МНК": MNK,
            "МКР": MKR,
            "Меню": Menu,
            "Настройки": Settings,
        }

        window_titles = {
            "Интегралы": "Численное интегрирование (Интегралы)",
            "Уравнения": "Решение НУ",
            "Полиномы": "Решение полинома",
            "МНК": "Аппроксимация МНК",
            "МКР": "Метод конечных разностей",
            "Меню": "Курсовая работа - Меню",
            "Настройки": "Настройки",
        }

        self.parent.destroy()
        root = tk.Tk()
        app_class = window_classes.get(window_name)
        title = window_titles.get(window_name, window_name)

        if app_class:
            _ = app_class(root, title, x=x, y=y)
            root.mainloop()

    def centrize_window(self):
        if self.x is None and self.y is None:
            sw = self.parent.winfo_screenwidth()
            sh = self.parent.winfo_screenheight()
            x, y = (sw - self.width) // 2, (sh - self.height) // 2
            self.parent.geometry(f"{self.width}x{self.height}+{x}+{y}")
            self.parent.resizable(False, False)
            return x, y
        else:
            self.parent.geometry(
                f"{self.width}x{self.height}+{self.x}+{self.y}",
            )
            self.parent.resizable(False, False)

        return None, None

    def initUI(self):
        self.parent.title(self.title)
        self.centrize_window()
