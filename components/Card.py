import tkinter as tk

class Card(tk.Frame):
    def __init__(self, parent, row=0, column=0, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(bg='#F8F9FA')
        padx = 8
        pady = 8
        if row > 0:
            pady=(0, 8)
        if column > 0:
            padx=(0, 8)
        self.grid(padx=padx, pady=pady, row=row, column=column, sticky='nsew')

