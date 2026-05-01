import tkinter as tk

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from auxiliaryClasses.baseMnk import BaseMNK
from auxiliaryClasses.baseWindow import BaseWindow


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
        self.graphic_frame = ctk.CTkFrame(self, corner_radius=15, width=self.GRAPHIC_FRAME_WIDTH, height=self.GRAPHIC_FRAME_HEIGHT)
        self.graphic_frame.place(relx=0.6, rely=0.03)

        title_label = ctk.CTkLabel(self.graphic_frame, text='Аппроксимация методом наименьших квадратов', font=('Arial', 15, 'bold'))
        title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        self.figure = Figure(figsize=(5.5, 4.5), dpi=65)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('x', fontsize=10)
        self.ax.set_ylabel('y', fontsize=10)
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graphic_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.5, rely=0.54, anchor=tk.CENTER, width=350, height=270)
    
    def insert_base_dots(self):
        x = [0.01, 0.02, 0.1, 0.2, 0.34, 0.4, 0.55, 0.6, 0.77, 0.87, 0.9, 1]
        y = [10, 9.2, 8.5, 6.1, 4.3, 3.4, 3.3, 2.5, 2.2, 1.5, 1.1, 0.1]
        self.x_y_list = list(zip(x, y))
        self.update_listbox()
    
    def create_buttons(self):
        insert_base_dots = ctk.CTkButton(self, text='Вставить базовые значения в таблицу', width=300, corner_radius=15, command=self.insert_base_dots)
        to_pro_btn = ctk.CTkButton(self, text='Перейти в Base mode', width=300, corner_radius=15, command=lambda: self.destroy())

        insert_base_dots.place(relx=0.38, rely=0.82)
        to_pro_btn.place(relx=0.38, rely=0.9)
    
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