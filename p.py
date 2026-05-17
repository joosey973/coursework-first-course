import tkinter as tk

class Logo(tk.Frame):
    def __init__(self, parent, width=600, height=520):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.width = width
        self.height = height
        self.initUI()
    
    def centrize_window(self):
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - self.width) // 2
        y = (sh - self.height) // 2
        self.parent.geometry(f'{self.width}x{self.height}+{x}+{y}')
        self.parent.resizable(False, False)
    
    def create_triangles(self):
        colors = ['#2CB1A4', '#FCD77C']
        offset = 0
        for color in colors:
            x1, y1 = 25 + offset, 150
            x2, y2 = 175 + offset, 150
            x3, y3 = 100 + offset, 20
            self.canvas.create_polygon(
                x1, y1,
                x2, y2,
                x3, y3,
                fill=color,
                outline=color,
                width=2,
            )
            offset += 200
        
        x1, y1 = 25, 300
        x2, y2 = 175, 300
        x3, y3 = 100, 170
        color = '#FFC641'
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, outline=color, width=2)
    
    def create_circles(self):
        offset = 200
        color = '#41A0E0'
        subcolor = '#222126'

        self.canvas.create_oval(230, 175, 365, 310, fill=color, outline=color, width=2)
        self.canvas.create_oval(230, 175, 280, 225, fill=subcolor, outline=subcolor, width=2)
        self.canvas.create_oval(298, 242, 366, 310, fill=subcolor, outline=subcolor, width=2)

        color = '#FC7239'
        self.canvas.create_oval(420, 175, 555, 310, fill=color, outline=color, width=2)
        self.canvas.create_oval(447, 200, 547, 300, fill=subcolor, outline=subcolor, width=2)

        color = '#6C4DAA'
        self.canvas.create_arc(230, 350, 365, 485, fill=color, outline=color, width=2, start=90, extent=180)
        color = '#FC6495'
        self.canvas.create_arc(230, 350, 365, 485, fill=color, outline=color, width=2, start=-90, extent=180)
        self.canvas.create_oval(267.5, 387.5, 327.5, 447.5, fill=subcolor, outline=subcolor, width=2)

        color = '#2E5399'
        self.canvas.create_oval(420, 350, 555, 485, fill=color, outline=color, width=2)
        self.canvas.create_oval(457.5, 387.5, 592.5, 447.5, fill=subcolor, outline=subcolor, width=2)
    
    def create_cross_and_kite(self):
        side = 45
        color = 'crimson'
        subcolor = '#222126'
        self.canvas.create_rectangle(420, 15, 420 + side * 3, 15 + side * 3, fill=color, outline=color, width=2)
        self.canvas.create_rectangle(420, 15, 420 + side, 15 + side, fill=subcolor, outline=subcolor, width=2)
        self.canvas.create_rectangle(420, 15 + side * 2, 420 + side, 15 + side * 3, fill=subcolor, outline=subcolor, width=2)
        self.canvas.create_rectangle(420 + side * 2, 15, 420 + side * 3, 15 + side, fill=subcolor, outline=subcolor, width=2)
        self.canvas.create_rectangle(420 + side * 2, 15 + side * 2, 420 + side * 3, 15 + side * 3, fill=subcolor, outline=subcolor, width=2)

        x1, y1 = 25, 400
        x2, y2 = 100, 350
        x3, y3 = 175, 400
        x4, y4 = 100, 485
        color = "#41E083"
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, fill=color, outline=color, width=2)

    def initUI(self):
        self.parent.title('Логотип')
        self.centrize_window()
        self.canvas = tk.Canvas(self.parent, width=self.width, height=self.height, bg='#222126')
        self.canvas.place(width=self.width, height=self.height)
        self.config(bg='#222126')
        self.create_circles()
        self.create_triangles()
        self.create_cross_and_kite()
        self.place(width=self.width, height=self.height)


def main():
    root = tk.Tk()
    Logo(root)
    root.mainloop()

if __name__ == '__main__':
    main()