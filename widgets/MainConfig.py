import tkinter as tk
from components.CustomLabel import CustomLabel
from components.CustomSwitch import CustomSwitch
from components.Card import Card
import RPi.GPIO as GPIO

class MainConfig:
    def __init__(self, parent, root, pin):
        self.parent = parent
        self.root = root
        self.pin = pin
        self.timeElapsed = 0
        self.lastTime = 0
        self.timerId = None

        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=4)
        parent.rowconfigure(1, weight=1)
        parent.rowconfigure(2, weight=1)

        mainCard = tk.Frame(self.parent, bg='#F8F9FA')
        mainCard.grid(padx=8, pady=8, row=0, column=0, sticky='nsew')

        frame = tk.Frame(mainCard, bg='#F8F9FA')
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        mainLabel = CustomLabel(frame, text="Main")
        mainLabel.pack()

        switchFrame = tk.Frame(frame, bg='#F8F9FA')
        switchFrame.pack()

        stopLabel = CustomLabel(switchFrame, text='Stop')
        self.switch = CustomSwitch(switchFrame, onChange=self.handleChange)
        startLabel = CustomLabel(switchFrame, text="Start")

        stopLabel.pack(side=tk.LEFT)
        self.switch.pack(side=tk.LEFT, padx=16, pady=16)
        startLabel.pack(side=tk.LEFT)

        timeElapsedCard = tk.Frame(self.parent, bg='#F8F9FA')
        timeElapsedCard.grid(padx=8, pady=(0, 8), row=1, column=0, sticky='nsew')

        timeElapsedLabel = CustomLabel(timeElapsedCard, text="Time Elapsed")
        timeElapsedLabel.pack(side=tk.LEFT, padx=24)

        self.timeElapsedValue = CustomLabel(timeElapsedCard, text=f"{self.timeElapsed}m", fontSize=24)
        self.timeElapsedValue.pack(side=tk.RIGHT, padx=24)

        lastTimeCard = tk.Frame(self.parent, bg='#F8F9FA')
        lastTimeCard.grid(padx=8, pady=(0, 8), row=2, column=0, sticky='nsew')

        lastTimeLabel = CustomLabel(lastTimeCard, text="Last Time On")
        lastTimeLabel.pack(side=tk.LEFT, padx=24)

        self.lastTimeValue = CustomLabel(lastTimeCard, text=f"{self.lastTime}m", fontSize=24)
        self.lastTimeValue.pack(side=tk.RIGHT, padx=24)


    def handleChange(self, isActive):
        if isActive:
            GPIO.output(self.pin, 1)
            self.root.after(60 * 1000, self.setTimeElapsed)
        else:
            GPIO.output(self.pin, 0)
            self.lastTime = self.timeElapsed
            self.timeElapsed = 0
            self.timeElapsedValue.config(text=f"{self.timeElapsed}m")
            self.lastTimeValue.config(text=f"{self.lastTime}m")
            if self.timerId:
                self.root.after_cancel(self.timerId)


    def setTimeElapsed(self):
        self.timeElapsed += 1
        self.timeElapsedValue.config(text=f"{self.timeElapsed}m")
        self.timerId = self.root.after(60 * 1000, self.setTimeElapsed)