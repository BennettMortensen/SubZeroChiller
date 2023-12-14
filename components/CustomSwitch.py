import tkinter as tk
import os

class CustomSwitch(tk.Canvas):
    def __init__(self, master=None, onChange=None, **kwargs):
        super().__init__(master, bg='#F8F9FA', borderwidth=0, highlightthickness=0, **kwargs)
        self.active = False
        self.on_image = tk.PhotoImage(file=os.path.abspath('chiller/assets/on_switch.png'), width=122, height=60)
        self.off_image = tk.PhotoImage(file=os.path.abspath('chiller/assets/off_switch.png'), width=122, height=60)
        self.onChange = onChange

        self.create_image(0, 0, anchor=tk.NW, image=self.off_image)
        self.bind("<Button-1>", self.toggle)

        self.config(width=122, height=60)

    def toggle(self, event):
        self.active = not self.active
        self.update_image()

        if self.onChange:
            self.onChange(self.active)

    def update_image(self):
        if self.active:
            self.itemconfig(1, image=self.on_image)
        else:
            self.itemconfig(1, image=self.off_image)
