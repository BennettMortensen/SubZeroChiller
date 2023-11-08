import tkinter as tk
from components.IconButton import IconButton
from components.PowerControl import PowerControl
from components.CustomLabel import CustomLabel

class PowerLevel:
    def __init__(self, parent, low, high, delay, onChange):
        self.parent = parent
        self.low = low
        self.high = high
        self.delay = delay
        self.onChange = onChange
        self.index = 0
        self.value = None

        frame = tk.Frame(self.parent, bg='#F8F9FA')
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label = CustomLabel(frame, text="Power Level")
        label.pack()
        self.powerControl = PowerControl(frame)
        self.powerControl.pack(pady=24)

        powerControlFrame = tk.Frame(self.powerControl, bg='#F8F9FA')
        powerControlFrame.place(relx=1.0, rely=0.5, anchor='e')

        self.minusBtn = IconButton(powerControlFrame, './assets/minimize.png', command=self.decreaseLevel)
        self.minusBtn.pack(side=tk.LEFT, padx=8)
        self.addBtn = IconButton(powerControlFrame, './assets/add.png', command=self.increaseLevel)
        self.addBtn.pack(side=tk.LEFT)

        self.minusBtn['state'] = 'disabled'
        self.addBtn['state'] = 'disabled'

    def updateDelay(self, value):
        delay = round(0.0088-(0.0008*value),4)
        self.onChange(delay)

    def resetControls(self):
        self.index = 0
        self.value = None
        self.updateDelay(self.low)
        self.powerControl.reset()

    def disableControls(self, disable):
        if disable:
            self.minusBtn['state'] = 'disabled'
            self.addBtn['state'] = 'disabled'
            self.resetControls()
        else:
            self.minusBtn['state'] = 'normal'
            self.addBtn['state'] = 'normal'

    def setIndex(self):
        self.index = self.value - 1
        if self.high < 10 and self.value == self.high:
            self.index = 9
        if self.value == self.low:
            self.index = 0

    def increaseLevel(self):
        if self.value != None and self.value >= self.high:
            return
        if self.value == None:
            self.value = self.low
        else:
            self.value += 1
        self.setIndex()
        self.updateDelay(self.value)
        self.powerControl.change_color_plus(self.index)

    def decreaseLevel(self):
        if self.value == None or self.index < self.low - 1:
            return
        self.value -= 1
        self.setIndex()
        self.updateDelay(self.value)
        self.powerControl.change_color_minus(self.index)