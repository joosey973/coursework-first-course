__all__ = []

import customtkinter as ctk

from auxiliaryClasses.baseWindow import BaseWindow
import config


class Settings(BaseWindow):
    DARK_THEME = "Темная тема"
    WHITE_THEME = "Светлая тема"

    def __init__(self, parent, title, width=500, height=400, x=None, y=None):
        self.theme_color = (
            Settings.DARK_THEME
            if config.COLOR_THEME == "black"
            else Settings.WHITE_THEME
        )
        super().__init__(parent, title, width, height, x, y)
        if x is None:
            self.x, self.y = self.centrize_window()

    def create_theme_button(self):
        ctk.CTkLabel(
            self,
            text="Смена темы",
            font=("Arial", 15, "bold"),
            text_color=config.TEXT_COLOR_IN_FRAME,
        ).place(relx=0.5, rely=0.35, anchor=ctk.CENTER)
        if config.COLOR_THEME == "black":
            switch_var = ctk.StringVar(value="on")
        else:
            switch_var = ctk.StringVar(value="off")

        self.switch = ctk.CTkSwitch(
            self,
            text=self.theme_color,
            command=self.switch_color,
            variable=switch_var,
            onvalue="on",
            offvalue="off",
            width=100,
            height=50,
            text_color=config.TEXT_COLOR_IN_FRAME,
            progress_color=config.BUTTON_COLOR,
        )
        self.switch.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        return_btn = ctk.CTkButton(
            self,
            text="Вернуться в меню<",
            width=200,
            corner_radius=15,
            command=lambda: self.create_new_window("Меню", self.x, self.y),
            fg_color=config.BUTTON_COLOR,
            text_color=config.TEXT_COLOR_IN_BTN,
            hover_color=config.HOVER_BUTTON_COLOR,
        )
        return_btn.place(relx=0.5, rely=0.8)

    def switch_color(self):
        if self.theme_color == Settings.DARK_THEME:
            self.theme_color = Settings.WHITE_THEME
            self.switch.configure(text=self.theme_color)
            config.COLOR_THEME = "white"
        elif self.theme_color == Settings.WHITE_THEME:
            self.theme_color = Settings.DARK_THEME
            self.switch.configure(text=self.theme_color)
            config.COLOR_THEME = "black"

        config.update_colors()
        self.x, self.y = self.winfo_rootx(), self.winfo_rooty() - 28
        Settings(self.parent, self.title, x=self.x, y=self.y)
        self.destroy()

    def initUI(self):
        self.create_theme_button()
        super().initUI()
