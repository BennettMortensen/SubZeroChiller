import tkinter as tk
from components.CustomLabel import CustomLabel
from components.CustomSwitch import CustomSwitch
from components.Card import Card
import RPi.GPIO as GPIO
import time

class DefrostConfig:
    def __init__(self, parent, root, defrostPin, zcTimeDiff):
        self.parent = parent
        self.root = root
        self.defrostPin = defrostPin
        self.zcTimeDiff = zcTimeDiff

        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=3)
        parent.rowconfigure(1, weight=1)

        defrostCard = tk.Frame(self.parent, bg='#F8F9FA')
        defrostCard.grid(padx=8, pady=8, row=0, column=0, sticky='nsew')

        frame = tk.Frame(defrostCard, bg='#F8F9FA')
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        defrostLabel = CustomLabel(frame, text="Defrost")
        defrostLabel.pack()

        switchFrame = tk.Frame(frame, bg='#F8F9FA')
        switchFrame.pack()

        stopLabel = CustomLabel(switchFrame, text='Stop')
        self.switch = CustomSwitch(switchFrame, onChange=self.handleChange)
        startLabel = CustomLabel(switchFrame, text="Start")

        stopLabel.pack(side=tk.LEFT)
        self.switch.pack(side=tk.LEFT, padx=16, pady=16)
        startLabel.pack(side=tk.LEFT)

        zeroCrossCard = tk.Frame(self.parent, bg='#F8F9FA')
        zeroCrossCard.grid(padx=8, pady=(0, 8), row=1, column=0, sticky='nsew')

        zeroCrossLabel = CustomLabel(zeroCrossCard, text="Zerocross Time")
        zeroCrossLabel.pack(side=tk.LEFT, padx=24)

        self.zeroCrossValue = CustomLabel(zeroCrossCard, text=f"{round(self.zcTimeDiff,5)}", fontSize=24)
        self.zeroCrossValue.pack(side=tk.RIGHT, padx=24)

    def handleChange(self, isActive):
        if isActive:
            GPIO.output(self.defrostPin, 1)
        else:
            GPIO.output(self.defrostPin, 0)

    def updateZcValue(self, zcValue):
        self.zcTimeDiff = zcValue
        self.zeroCrossValue.config(text=f"{zcValue:.3f}")