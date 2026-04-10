import tkinter as tk
import tkinter.ttk as ttk


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