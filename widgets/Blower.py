import tkinter as tk
import RPi.GPIO as GPIO
from components.CustomLabel import CustomLabel
from components.CustomSwitch import CustomSwitch

class Blower:
    def __init__(self, parent, onChange, pin):
        self.parent = parent
        self.onChange = onChange
        self.pin = pin

        frame = tk.Frame(self.parent, bg='#F8F9FA')
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        blower = CustomLabel(frame, text="Blower")
        blower.pack()

        switchFrame = tk.Frame(frame, bg='#F8F9FA')
        switchFrame.pack()

        stopLabel = CustomLabel(switchFrame, text='Stop')
        self.switch = CustomSwitch(switchFrame, onChange=self.handleChange)
        startLabel = CustomLabel(switchFrame, text="Start")

        stopLabel.pack(side=tk.LEFT)
        self.switch.pack(side=tk.LEFT, padx=16, pady=24)
        startLabel.pack(side=tk.LEFT)

    def handleChange(self, isActive):
        if isActive:
            GPIO.output(self.pin, 1)
        else:
            GPIO.output(self.pin, 0)
            GPIO.output(18, 0)
        self.onChange(isActive)

    def toggleSwitch(self):
        self.switch.toggle(None)