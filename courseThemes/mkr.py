__all__ = []

import tkinter as tk

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import sympy as sp
from sympy import lambdify
from sympy import symbols

from auxiliaryClasses.baseWindow import BaseWindow
import config


class MKR(BaseWindow):
    PROGONKA = 0
    MATRIX = 1
    KRAMER = 2

    def __init__(self, parent, title, width=1300, height=700, x=None, y=None):
        super().__init__(parent, title, width, height, x=x, y=y)

    def create_task_parametrs_fields(self):
        frame = ctk.CTkFrame(
            self,
            corner_radius=15,
            width=450,
            height=250,
            fg_color=config.BACKGROUND_FRAME,
        )
        frame.place(relx=0.03, rely=0.05)
        frame_label = ctk.CTkLabel(
            frame,
            text="Задайте параметры",
            corner_radius=15,
            fg_color="#d6d1d1",
            width=30,
            height=30,
            text_color="#2b2b2b",
        )
        frame_label.place(relx=0.02, rely=0.02)

        self.p_x_field = ctk.CTkEntry(
            frame,
            corner_radius=15,
            width=100,
            height=30,
            fg_color=config.BACKGROUND_FIELD_COLOR,
            text_color=config.TEXT_COLOR_IN_FRAME,
            border_color=config.BORDER_COLOR,
        )
        ctk.CTkLabel(
            frame,
            text="p(x):",
            text_color=config.TEXT_COLOR_IN_FRAME,
        ).place(relx=0.03, rely=0.17)
        self.p_x_field.place(relx=0.22, rely=0.17)
        self.q_x_field = ctk.CTkEntry(
            frame,
            corner_radius=15,
            width=100,
            height=30,
            fg_color=config.BACKGROUND_FIELD_COLOR,
            text_color=config.TEXT_COLOR_IN_FRAME,
            border_color=config.BORDER_COLOR,
        )
        ctk.CTkLabel(
            frame,
            text="q(x):",
            text_color=config.TEXT_COLOR_IN_FRAME,
        ).place(relx=0.03, rely=0.37)
        self.q_x_field.place(relx=0.22, rely=0.37)
        self.r_x_field = ctk.CTkEntry(
            frame,
            corner_radius=15,
            width=100,
            height=30,
            fg_color=config.BACKGROUND_FIELD_COLOR,
            text_color=config.TEXT_COLOR_IN_FRAME,
            border_color=config.BORDER_COLOR,
        )
        ctk.CTkLabel(
            frame,
            text="r(x):",
            text_color=config.TEXT_COLOR_IN_FRAME,
        ).place(relx=0.03, rely=0.57)
        self.r_x_field.place(relx=0.22, rely=0.57)
        self.n_field = ctk.CTkEntry(
            frame,
            corner_radius=15,
            width=100,
            height=30,
            fg_color=config.BACKGROUND_FIELD_COLOR,
            text_color=config.TEXT_COLOR_IN_FRAME,
            border_color=config.BORDER_COLOR,
        )
        ctk.CTkLabel(
            frame,
            text="n (число отрезков):",
            wraplength=80,
            justify=ctk.LEFT,
            text_color=config.TEXT_COLOR_IN_FRAME,
        ).place(relx=0.03, rely=0.77)
        self.n_field.place(relx=0.22, rely=0.77)

        self.x_0_field = ctk.CTkEntry(
            frame,
            corner_radius=15,
            width=100,
            height=30,
            fg_color=config.BACKGROUND_FIELD_COLOR,
            text_color=config.TEXT_COLOR_IN_FRAME,
            border_color=config.BORDER_COLOR,
        )
        ctk.CTkLabel(
            frame,
            text="x0:",
            text_color=config.TEXT_COLOR_IN_FRAME,
        ).place(relx=0.55, rely=0.17)
        self.x_0_field.place(relx=0.64, rely=0.17)
        self.x_k_field = ctk.CTkEntry(
            frame,
            corner_radius=15,
            width=100,
            height=30,
            fg_color=config.BACKGROUND_FIELD_COLOR,
            text_color=config.TEXT_COLOR_IN_FRAME,
            border_color=config.BORDER_COLOR,
        )
        ctk.CTkLabel(
            frame,
            text="xk:",
            text_color=config.TEXT_COLOR_IN_FRAME,
        ).place(relx=0.55, rely=0.37)
        self.x_k_field.place(relx=0.64, rely=0.37)
        self.y_0_field = ctk.CTkEntry(
            frame,
            corner_radius=15,
            width=100,
            height=30,
            fg_color=config.BACKGROUND_FIELD_COLOR,
            text_color=config.TEXT_COLOR_IN_FRAME,
            border_color=config.BORDER_COLOR,
        )
        ctk.CTkLabel(
            frame,
            text="y(x0):",
            text_color=config.TEXT_COLOR_IN_FRAME,
        ).place(relx=0.55, rely=0.57)
        self.y_0_field.place(relx=0.64, rely=0.57)
        self.y_k_field = ctk.CTkEntry(
            frame,
            corner_radius=15,
            width=100,
            height=30,
            fg_color=config.BACKGROUND_FIELD_COLOR,
            text_color=config.TEXT_COLOR_IN_FRAME,
            border_color=config.BORDER_COLOR,
        )
        ctk.CTkLabel(
            frame,
            text="y(xk):",
            text_color=config.TEXT_COLOR_IN_FRAME,
        ).place(relx=0.55, rely=0.77)
        self.y_k_field.place(relx=0.64, rely=0.77)

    def create_buttons_with_method(self):
        frame = ctk.CTkFrame(
            self,
            corner_radius=15,
            width=450,
            height=250,
            fg_color=config.BACKGROUND_FRAME,
        )
        frame.place(relx=0.5, rely=0.05)
        ctk.CTkLabel(
            frame,
            text="Метод решения",
            corner_radius=15,
            fg_color="#d6d1d1",
            width=30,
            height=30,
            text_color="#2b2b2b",
        ).place(relx=0.02, rely=0.02)

        self.radio_var = tk.IntVar(value=0)
        vr_1 = ctk.CTkRadioButton(
            frame,
            text="Прогонка",
            variable=self.radio_var,
            value=0,
            fg_color=config.BUTTON_COLOR,
            hover_color=config.HOVER_BUTTON_COLOR,
            text_color=config.TEXT_COLOR_IN_FRAME,
        )
        vr_2 = ctk.CTkRadioButton(
            frame,
            text="Матричный",
            variable=self.radio_var,
            value=1,
            fg_color=config.BUTTON_COLOR,
            hover_color=config.HOVER_BUTTON_COLOR,
            text_color=config.TEXT_COLOR_IN_FRAME,
        )
        vr_3 = ctk.CTkRadioButton(
            frame,
            text="Крамер",
            variable=self.radio_var,
            value=2,
            fg_color=config.BUTTON_COLOR,
            hover_color=config.HOVER_BUTTON_COLOR,
            text_color=config.TEXT_COLOR_IN_FRAME,
        )

        vr_1.place(relx=0.05, rely=0.25)
        vr_2.place(relx=0.05, rely=0.5)
        vr_3.place(relx=0.05, rely=0.75)

        solve_btn = ctk.CTkButton(
            frame,
            text="Решить",
            width=200,
            corner_radius=15,
            command=self.solve,
            fg_color=config.BUTTON_COLOR,
            text_color=config.TEXT_COLOR_IN_BTN,
            hover_color=config.HOVER_BUTTON_COLOR,
        )
        insrt_btn = ctk.CTkButton(
            frame,
            text="Вставить по умолчанию",
            width=200,
            corner_radius=15,
            command=self.insert_base_vals,
            fg_color=config.BUTTON_COLOR,
            text_color=config.TEXT_COLOR_IN_BTN,
            hover_color=config.HOVER_BUTTON_COLOR,
        )

        ctk.CTkButton(
            frame,
            text="Вернуться в меню<",
            width=200,
            corner_radius=15,
            command=lambda: self.create_new_window("Меню"),
            fg_color=config.BUTTON_COLOR,
            text_color=config.TEXT_COLOR_IN_BTN,
            hover_color=config.HOVER_BUTTON_COLOR,
        ).place(relx=0.5, rely=0.75)
        solve_btn.place(relx=0.5, rely=0.35)
        insrt_btn.place(relx=0.5, rely=0.55)

    def kramer_method(self, x, h):
        coefs = self.get_coefs(x, h)
        if coefs is None:
            return None

        A, C, B, F = coefs

        matrix = self.create_matrix(self.n, coefs, x=None)

        n = self.n + 1
        b = [[F[i]] for i in range(n)]

        result = self.solve_by_kramer(matrix, b)
        if result is None:
            return None

        y = [float(result[i]) for i in range(n)]

        return y

    def solve_by_kramer(self, A, b):
        n = len(A)

        det_A = self.find_determinante(A)

        if abs(det_A) < 1e-10:
            self.show_popup(
                "Определитель равен нулю, метод Крамера неприменим",
            )
            return None

        x = []

        for i in range(n):
            Ai = [row[:] for row in A]

            for j in range(n):
                Ai[j][i] = b[j][0]

            det_Ai = self.find_determinante(Ai)

            xi = det_Ai / det_A
            x.append(xi)

        return x

    def solve(self):
        fields = {
            "x0": (self.x_0_field, "x0", float),
            "xk": (self.x_k_field, "xk", float),
            "y0": (self.y_0_field, "y(x0)", float),
            "yk": (self.y_k_field, "y(xk)", float),
            "n": (self.n_field, "n (число отрезков)", int),
            "p(x)": (self.p_x_field, "p(x)", str),
            "q(x)": (self.q_x_field, "q(x)", str),
            "r(x)": (self.r_x_field, "r(x)", str),
        }

        validated_data = {}

        for field_name, (
            field_widget,
            display_name,
            expected_type,
        ) in fields.items():
            raw_value = field_widget.get().strip()

            if not raw_value:
                self.show_popup(f"Поле {display_name} пустое!")
                return

            if expected_type is str:
                value = raw_value
            else:
                raw_value = raw_value.replace(",", ".")
                if field_name == "n" and not raw_value.isdigit():
                    self.show_popup(
                        f"Значение поля '{display_name}' должно быть int",
                    )
                    return

                if expected_type is int:
                    value = int(raw_value)
                else:
                    try:
                        value = float(raw_value)
                    except ValueError:
                        self.show_popup(
                            f"Значение поля '{display_name}'" " должно быть float/int",
                        )
                        return

            validated_data[field_name] = value

        self.n = validated_data.get("n")
        self.x_0 = validated_data.get("x0")
        self.x_k = validated_data.get("xk")
        self.y_0 = validated_data.get("y0")
        self.y_k = validated_data.get("yk")
        self.p = validated_data.get("p(x)")
        self.q = validated_data.get("q(x)")
        self.r = validated_data.get("r(x)")

        h = (self.x_k - self.x_0) / self.n
        x = [self.x_0]
        if self.x_0 >= self.x_k:
            self.show_popup("x0 не может быть больше xk!")
            self.clear_fields()
            return

        for i in range(1, self.n + 1):
            x.append(self.x_0 + i * h)

        if (
            "log" in self.p
            or "log" in self.q
            or "log" in self.r
            or "ln" in self.p
            or "ln" in self.q
            or "ln" in self.r
        ) and not all([val > 0 for val in x]):
            self.show_popup("x должны быть больше 0")
            return

        variant = self.radio_var.get()
        y = []
        try:
            if variant == MKR.PROGONKA:
                y = self.progonka_method(x, h)
            elif variant == MKR.MATRIX:
                y = self.matrix_method(x, h)
            else:
                y = self.kramer_method(x, h)

        except Exception:
            self.show_popup("Ошибка в синтаксе написания функции!")
            return

        if y is None:
            self.clear_fields()
            return

        self.show_table(x, y)
        coefs = self.kramer_polinom(x, y)
        self.update_polinom_and_gprahic(coefs, x, y)

    def clear_fields(self):
        self.show_table([], [])
        self.update_polinom_and_gprahic([], [], [])

    def update_polinom_and_gprahic(self, coefs, x, y):
        self.polinom_field.configure(state="normal")
        self.polinom_field.delete(0, ctk.END)
        self.polinom_field.insert(0, self.get_polinom(coefs, x))
        self.polinom_field.configure(state="readonly")

        if x and y:
            x_dots = np.linspace(self.x_0, self.x_k, 1000)
            y_dots = []
            for x_val in x_dots:
                temp_x = coefs[0]
                for i in range(1, len(coefs)):
                    temp_x += coefs[i] * x_val**i

                y_dots.append(temp_x)

            self.ax.clear()
            self.ax.grid(True, alpha=0.3)
            self.ax.plot(
                x_dots,
                y_dots,
                "b-",
                linewidth=2,
                label="Интерполяционный полином",
            )
            self.ax.scatter(
                x,
                y,
                label="Узлы интерполяции",
                marker="o",
                color="red",
            )
            self.ax.legend()
            self.canvas.draw()
        else:
            self.ax.clear()
            self.ax.grid(True, alpha=0.3)
            self.canvas.draw()

    def get_polinom(self, coefs, x):
        if not coefs:
            return ""

        terms = []
        for i in range(len(x) - 1, -1, -1):
            coeff = round(coefs[i], 6)
            if i == 0:
                terms.append(f"{coeff}")
            elif i == 1:
                terms.append(f"{coeff}*x")
            else:
                terms.append(f"{coeff}*x^{i}")

        polinom = f"P{len(coefs) - 1}(x)=" + " + ".join(terms).replace(
            " + -",
            " - ",
        )
        self.adjust_font_size(polinom)
        return polinom

    def adjust_font_size(self, text):
        import tkinter.font as tkfont

        max_width = 275
        font_size = 15

        test_font = tkfont.Font(family="Arial", size=font_size)
        text_width = test_font.measure(text)

        while text_width > max_width and font_size > 8:
            font_size -= 1
            test_font.configure(size=font_size)
            text_width = test_font.measure(text)

        self.polinom_field.configure(font=("Arial", font_size + 3))

    def matrix_method(self, x, h):
        coefs = self.get_coefs(x, h)
        if coefs is None:
            return

        matrix = self.create_matrix(self.n, coefs, x=None)

        det = self.find_determinante(matrix)
        if abs(det) < 1e-15:
            self.show_popup("Матрица вырождена, определитель равен 0")
            return

        reversed_matrix = self.find_reversed_matrix(matrix)
        if reversed_matrix is None:
            self.show_popup("Не удалось найти обратную матрицу")
            return

        result_matrix = self.matrix_multiplication(
            reversed_matrix,
            [[i] for i in coefs[-1]],
        )
        result_matrix = [i[0] for i in result_matrix]
        if result_matrix is None:
            self.show_popup("Ошибка при умножении матриц")
            return None

        return result_matrix

    def progonka_method(self, x, h):
        alpha = [0 for i in range(self.n + 1)]
        beta = [0 for i in range(self.n + 1)]
        coefs = self.get_coefs(x, h)
        if coefs is None:
            return

        A, C, B, F = coefs

        if abs(C[0]) < 1e-15:
            self.show_popup("Деление на ноль в методе прогонки (C[0] = 0)")
            return

        alpha[0], beta[0] = B[0] / C[0], -F[0] / C[0]

        if (
            np.isnan(alpha[0])
            or np.isinf(alpha[0])
            or np.isnan(beta[0])
            or np.isinf(beta[0])
        ):
            self.show_popup("Некорректные значения в методе прогонки")
            return

        for i in range(1, self.n + 1):
            denominator = C[i] - alpha[i - 1] * A[i]

            if abs(denominator) < 1e-15:
                self.show_popup(
                    f"Деление на ноль в методе прогонки на шаге {i}",
                )
                return

            alpha[i] = B[i] / denominator
            beta[i] = (beta[i - 1] * A[i] - F[i]) / denominator
            if (
                np.isnan(alpha[i])
                or np.isinf(alpha[i])
                or np.isnan(beta[i])
                or np.isinf(beta[i])
            ):
                self.show_popup(
                    f"Некорректные значения в методе прогонки на шаге {i}",
                )
                return

        y = [0 for i in range(len(x))]
        y[-1] = beta[-1]

        if np.isnan(y[-1]) or np.isinf(y[-1]):
            self.show_popup("Некорректное значение y[0] в методе прогонки")
            return

        for i in range(self.n - 1, -1, -1):
            y[i] = alpha[i] * y[i + 1] + beta[i]
            if np.isnan(y[i]) or np.isinf(y[i]):
                self.show_popup(
                    f"Некорректное значение y[{i}] в методе прогонки",
                )
                return

        return y

    def get_coefs(self, x, h):
        import warnings

        x_vals = symbols("x")
        p_func = lambdify(x_vals, sp.sympify(self.p), "numpy")
        q_func = lambdify(x_vals, sp.sympify(self.q), "numpy")
        r_func = lambdify(x_vals, sp.sympify(self.r), "numpy")
        x = np.array(x)

        with warnings.catch_warnings():
            warnings.filterwarnings("error", category=RuntimeWarning)
            try:
                p = p_func(x)
                q = q_func(x)
                r = r_func(x)
            except RuntimeWarning:
                self.show_popup("Деление на ноль!")
                return

        if type(p) in (int, float):
            p = np.array([p for i in range(len(x))])

        if type(q) in (int, float):
            q = np.array([q for i in range(len(x))])

        if type(r) in (int, float):
            r = np.array([r for i in range(len(x))])

        A = [0 for _ in range(len(x))]
        C = [0 for _ in range(len(x))]
        B = [0 for _ in range(len(x))]
        F = [0 for _ in range(len(x))]
        F[0], F[-1] = self.y_0, self.y_k
        C[0], C[-1] = -1, -1

        for i in range(1, self.n):
            A[i] = 1 - p[i] * h / 2
            C[i] = 2 - q[i] * h**2
            B[i] = 1 + p[i] * h / 2
            F[i] = r[i] * h**2

        return A, C, B, F

    def insert_base_vals(self):
        self.p_x_field.delete(0, ctk.END)
        self.q_x_field.delete(0, ctk.END)
        self.r_x_field.delete(0, ctk.END)
        self.x_0_field.delete(0, ctk.END)
        self.x_k_field.delete(0, ctk.END)
        self.y_0_field.delete(0, ctk.END)
        self.y_k_field.delete(0, ctk.END)
        self.n_field.delete(0, ctk.END)

        self.p_x_field.insert(0, "-x")
        self.q_x_field.insert(0, "2")
        self.r_x_field.insert(0, "x^2")
        self.x_0_field.insert(0, "0")
        self.x_k_field.insert(0, "2")
        self.y_0_field.insert(0, "1")
        self.y_k_field.insert(0, "4")
        self.n_field.insert(0, "8")

    def show_popup(self, text, type_popup="error"):
        import tkinter.messagebox as tkm

        if type_popup == "error":
            tkm.showerror("Ошибка", message=text)
            return

    def show_polinom(self):
        ctk.CTkLabel(
            self,
            text="Формула полинома",
            corner_radius=15,
            fg_color="#d6d1d1",
            width=30,
            height=30,
            text_color="#2b2b2b",
        ).place(relx=0.4, rely=0.85)
        self.polinom_field = ctk.CTkEntry(
            self,
            width=720,
            corner_radius=15,
            fg_color=config.BACKGROUND_FIELD_COLOR,
            text_color=config.TEXT_COLOR_IN_FRAME,
            border_color=config.BORDER_COLOR,
        )
        self.polinom_field.place(relx=0.4, rely=0.9)
        self.polinom_field.configure(state="readonly")

    def show_table(self, x_values=[], y_values=[]):
        table_frame = ctk.CTkFrame(
            self,
            corner_radius=15,
            fg_color=config.BACKGROUND_FRAME,
        )
        table_frame.place(relx=0.4, rely=0.45, relwidth=0.57, relheight=0.36)

        scroll_frame = ctk.CTkScrollableFrame(
            table_frame,
            corner_radius=10,
            fg_color="#f0f0f0",
        )
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        headers_frame = ctk.CTkFrame(
            scroll_frame,
            fg_color="#d6d1d1",
            corner_radius=8,
        )
        headers_frame.pack(fill="x", pady=(0, 5))

        headers_frame.grid_columnconfigure(0, weight=1)
        headers_frame.grid_columnconfigure(1, weight=1)
        headers_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(
            headers_frame,
            text="N",
            font=ctk.CTkFont(weight="bold"),
            text_color="#2b2b2b",
        ).grid(row=0, column=0, padx=10, pady=5)

        ctk.CTkLabel(
            headers_frame,
            text="x",
            font=ctk.CTkFont(weight="bold"),
            text_color="#2b2b2b",
        ).grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(
            headers_frame,
            text="y",
            font=ctk.CTkFont(weight="bold"),
            text_color="#2b2b2b",
        ).grid(row=0, column=2, padx=10, pady=5)

        for i, (x, y) in enumerate(zip(x_values, y_values)):
            bg_color = "#ffffff" if i % 2 == 0 else "#e8e8e8"

            row_frame = ctk.CTkFrame(
                scroll_frame,
                fg_color=bg_color,
                corner_radius=5,
            )
            row_frame.pack(fill="x", pady=1)

            row_frame.grid_columnconfigure(0, weight=1)
            row_frame.grid_columnconfigure(1, weight=1)
            row_frame.grid_columnconfigure(2, weight=1)

            ctk.CTkLabel(row_frame, text=str(i), text_color="#2b2b2b").grid(
                row=0,
                column=0,
                padx=10,
                pady=3,
            )

            ctk.CTkLabel(
                row_frame,
                text=f"{x:.4f}",
                text_color="#2b2b2b",
            ).grid(row=0, column=1, padx=10, pady=3)

            ctk.CTkLabel(
                row_frame,
                text=f"{y:.6f}",
                text_color="#2b2b2b",
            ).grid(row=0, column=2, padx=10, pady=3)

    def show_graphic(self):
        graphic_frame = ctk.CTkFrame(
            self,
            corner_radius=15,
            width=450,
            height=350,
            fg_color=config.BACKGROUND_FRAME,
        )
        graphic_frame.place(relx=0.03, rely=0.45)

        title_label = ctk.CTkLabel(
            graphic_frame,
            text="МКР",
            font=("Arial", 15, "bold"),
            text_color=config.TEXT_COLOR_IN_FRAME,
        )
        title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        self.figure = Figure(figsize=(5.5, 4.5), dpi=60)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel("x", fontsize=10)
        self.ax.set_ylabel("y", fontsize=10)
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.figure, master=graphic_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(
            relx=0.5,
            rely=0.54,
            anchor=tk.CENTER,
            width=400,
            height=300,
        )

    def initUI(self):
        super().initUI()
        self.create_task_parametrs_fields()
        self.create_buttons_with_method()
        self.show_table()
        self.show_polinom()
        self.show_graphic()
