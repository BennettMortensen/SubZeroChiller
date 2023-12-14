import tkinter as tk
from components.IconButton import IconButton

class PowerControl(tk.Canvas):
    def __init__(self, master, isConfig, min=1, max=10, **kwargs):
        super().__init__(master, bg='#F8F9FA', borderwidth=0, highlightthickness=0, **kwargs)
        self.controlCount = 10
        self.rectangles = []

        self.controlWidth = 40
        if isConfig:
            self.controlWidth = 20
        canvasWidth = (self.controlCount * self.controlWidth) + 144
        self.config(width=canvasWidth, height=64)

        self.reset()

    def change_color_plus(self, level):
        if level >= self.controlCount:
            return
        for i in range(level + 1):
            self.itemconfig(self.rectangles[i], fill='#0088FF')

    def change_color_minus(self, level):
        if level < 0:
            return
        for index in range(level + 1, 10):
            self.itemconfig(self.rectangles[index], fill='#E9ECEF')

    def reset(self):
        self.rectangles = []
        for i in range(self.controlCount):
            rect = self.create_rectangle(0, 0, self.controlWidth - 1, 64, fill='#E9ECEF', outline='#F8F9FA')
            self.rectangles.append(rect)
            x = i * self.controlWidth
            self.coords(rect, x, 0, x + (self.controlWidth - 1), 64)