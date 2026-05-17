__all__ = []

import tkinter as tk

import customtkinter as ctk

from auxiliaryClasses.baseWindow import BaseWindow
import config


class Menu(BaseWindow):
    def __init__(self, parent, title, width=500, height=500, x=None, y=None):
        super().__init__(parent, title, width, height, x, y)

    def create_buttons_and_label(self):
        theme_label = ctk.CTkLabel(
            self.parent,
            text='Выберите тему',
            font=('Arial', 25, 'bold'),
            text_color=config.TEXT_COLOR_IN_FRAME,
        )
        theme_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        buttons_texts = [
            'Интегралы',
            'МНК',
            'Уравнения',
            'МКР',
            'Полиномы',
            'От автора',
        ]
        count = 0
        add_x, add_y = 0.05, 0.3
        for button_text in buttons_texts:
            btn = ctk.CTkButton(
                self.parent,
                corner_radius=10,
                text=button_text,
                width=200,
                height=50,
                command=lambda text=button_text: self.create_new_window(text),
                fg_color=config.BUTTON_COLOR,
                text_color=config.TEXT_COLOR_IN_BTN,
                hover_color=config.HOVER_BUTTON_COLOR,
            )
            btn.place(relx=add_x, rely=add_y)
            count += 1
            add_x += 0.47
            if count == 2:
                add_x = 0.05
                add_y += 0.18
                count = 0

        button_text = 'Настройки'
        btn = ctk.CTkButton(
            self.parent,
            corner_radius=10,
            text=button_text,
            width=200,
            height=50,
            command=lambda text=button_text: self.create_new_window(text),
            fg_color=config.BUTTON_COLOR,
            text_color=config.TEXT_COLOR_IN_BTN,
            hover_color=config.HOVER_BUTTON_COLOR,
        )
        btn.place(relx=0.29, rely=0.82)

    def initUI(self):
        super().initUI()
        self.create_buttons_and_label()
