import tkinter as tk

from auxiliaryClasses.menu import Menu


def main():
    menu_root = tk.Tk()
    menu_app = Menu(menu_root, 'Курсовая работа - Меню')
    menu_root.mainloop()


if __name__ == '__main__':
    main()