import tkinter as tk
from components.CustomLabel import CustomLabel
from components.IconButton import IconButton

class PowerRange:
    def __init__(self, parent, low, high, onRangeChange):
        self.parent = parent
        self.lowRange = low
        self.highRange = high
        self.onRangeChange = onRangeChange

        frame = tk.Frame(self.parent, bg='#F8F9FA')
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        powerRange = CustomLabel(frame, text="Power Range")
        powerRange.pack()

        lowFrame = tk.Frame(frame, bg='#F8F9FA')
        lowFrame.pack(pady=24)

        self.lowAddBtn = IconButton(lowFrame, './assets/add.png', command=lambda: self.increaseRange('low'))
        lowRangeFrame = tk.Frame(lowFrame, bg='#F8F9FA')
        self.lowRangeLabel = CustomLabel(lowRangeFrame, fontSize=24, text=str(self.lowRange))
        self.lowRangeLabel.pack()
        lowLabel = CustomLabel(lowRangeFrame, text='Low')
        lowLabel.pack()
        self.lowMinusBtn = IconButton(lowFrame, './assets/minimize.png', command=lambda: self.decreaseRange('low'))

        self.lowMinusBtn.pack(side=tk.LEFT)
        lowRangeFrame.pack(side=tk.LEFT, padx=48)
        self.lowAddBtn.pack(side=tk.LEFT)

        highFrame = tk.Frame(frame, bg='#F8F9FA')
        highFrame.pack()

        self.highAddBtn = IconButton(highFrame, './assets/add.png', command=lambda: self.increaseRange('high'))
        highRangeFrame = tk.Frame(highFrame, bg='#F8F9FA')
        self.highRangeLabel = CustomLabel(highRangeFrame, fontSize=24, text=str(self.highRange))
        self.highRangeLabel.pack()
        highLabel = CustomLabel(highRangeFrame, text='High')
        highLabel.pack()
        self.highMinusBtn = IconButton(highFrame, './assets/minimize.png', command=lambda: self.decreaseRange('high'))

        self.highMinusBtn.pack(side=tk.LEFT)
        highRangeFrame.pack(side=tk.LEFT, padx=48)
        self.highAddBtn.pack(side=tk.LEFT)

    def increaseRange(self, range):
        if range == 'low':
            if self.lowRange >= 10:
                return
            self.lowRange += 1
            self.lowRangeLabel.config(text=str(self.lowRange))
            self.onRangeChange(self.lowRange, self.highRange)
        else:
            if self.highRange >= 10:
                return
            self.highRange += 1
            self.highRangeLabel.config(text=str(self.highRange))
            self.onRangeChange(self.lowRange, self.highRange)

    def decreaseRange(self, range):
        if range == 'low':
            if self.lowRange <= 1:
                return
            self.lowRange -= 1
            self.lowRangeLabel.config(text=str(self.lowRange))
            self.onRangeChange(self.lowRange, self.highRange)
        else:
            if self.highRange <=1:
                return
            self.highRange -= 1
            self.highRangeLabel.config(text=str(self.highRange))
            self.onRangeChange(self.lowRange, self.highRange)

    def disableControls(self, disable):
            if disable:
                self.lowAddBtn['state'] = 'disabled'
                self.lowMinusBtn['state'] = 'disabled'
                self.highAddBtn['state'] = 'disabled'
                self.highMinusBtn['state'] = 'disabled'
            else:
                self.lowAddBtn['state'] = 'normal'
                self.lowMinusBtn['state'] = 'normal'
                self.highAddBtn['state'] = 'normal'
                self.highMinusBtn['state'] = 'normal'