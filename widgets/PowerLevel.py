import tkinter as tk
from components.IconButton import IconButton
from components.PowerControl import PowerControl
from components.CustomLabel import CustomLabel
import os

class PowerLevel:
    def __init__(self, parent, rangeLow, rangeHigh, delay, onChange, isConfig):
        self.parent = parent
        self.rangeLow = rangeLow
        self.rangeHigh = rangeHigh
        self.delay = delay
        self.onChange = onChange
        self.value = 1

        frame = tk.Frame(self.parent, bg='#F8F9FA')
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label = CustomLabel(frame, text="Power Level")
        label.pack()
        self.powerControl = PowerControl(frame, isConfig=isConfig)
        self.powerControl.pack(pady=24)

        powerControlFrame = tk.Frame(self.powerControl, bg='#F8F9FA')
        powerControlFrame.place(relx=1.0, rely=0.5, anchor='e')

        self.minusBtn = IconButton(powerControlFrame, os.path.abspath('chiller/assets/minimize.png'), command=self.decreaseLevel)
        self.minusBtn.pack(side=tk.LEFT, padx=8)
        self.addBtn = IconButton(powerControlFrame, os.path.abspath('chiller/assets/add.png'), command=self.increaseLevel)
        self.addBtn.pack(side=tk.LEFT)

        self.minusBtn['state'] = 'disabled'
        self.addBtn['state'] = 'disabled'

    def updateDelay(self, value):
        # value -> the level of the blower (10 increments)
        # self.rangeLow, self.rangeHigh -> the powerRange adjustment (1 - 100)

        scale = (.0008 - .0088) / 100 # default scale
        if self.rangeLow != 1 or self.rangeHigh != 100: # adjust scale if not default of 1 - 100
            newHigh = .0088 + (self.rangeHigh - 1) * scale
            newLow = .0088 + (self.rangeLow - 1) * scale
            scale = (newHigh - newLow) / 100

        # calculate and then update the delay
        self.delay = .0088 + (value - 1) * scale
        self.onChange(self.delay)

    def resetControls(self):
        self.value = 1
        self.updateDelay(self.rangeLow)
        self.powerControl.reset()

    def disableControls(self, disable):
        if disable:
            self.minusBtn['state'] = 'disabled'
            self.addBtn['state'] = 'disabled'
            self.resetControls()
        else:
            self.minusBtn['state'] = 'normal'
            self.addBtn['state'] = 'normal'
            self.powerControl.change_color_plus(0)

    def increaseLevel(self):
        if self.value >= 10:
            return
        self.value += 1
        self.updateDelay(self.value)
        self.powerControl.change_color_plus(self.value - 1)

    def decreaseLevel(self):
        if self.value <= 1:
            return
        self.value -= 1
        self.updateDelay(self.value)
        self.powerControl.change_color_minus(self.value - 1)

    def updateRangeValues(self, rangeLow, rangeHigh):
        self.rangeLow = rangeLow
        self.rangeHigh = rangeHigh