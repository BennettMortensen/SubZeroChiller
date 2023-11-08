import tkinter as tk
from tkinter import font

class CustomLabel(tk.Label):
    def __init__(self, master, fontSize=20, **kwargs):
        super().__init__(master, bg='#F8F9FA', fg='#212529', **kwargs)

        custom_font = ("Helvetica", fontSize)
        self.config(font=custom_font)