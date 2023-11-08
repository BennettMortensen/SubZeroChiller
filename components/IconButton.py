import tkinter as tk

class IconButton(tk.Button):
    def __init__(self, master, image_path, disabled=False, small=False, **kwargs):
        image = tk.PhotoImage(file=image_path)
        super().__init__(
            master,
            image=image,
            bg='#F6FAFE',
            bd=0,
            highlightthickness=1,
            highlightbackground='#0088FF',
            width=60,
            height=60,
            **kwargs
        )
        self.image = image

        if small:
            self.configure(width=44, height=44)