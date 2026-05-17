import customtkinter as ctk
import webbrowser

# Функция, открывающая GitHub
def open_github():
    webbrowser.open("https://github.com")

# Настройка главного окна
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Пример ссылки на GitHub")
app.geometry("350x200")

# Кнопка, стилизованная под ссылку
link_button = ctk.CTkButton(
    master=app,
    text="Открыть GitHub",
    command=open_github,
    fg_color="transparent",
    text_color="blue",
    hover_color="#e8e8e8",
    cursor="hand2"
)
link_button.pack(pady=60)

app.mainloop()