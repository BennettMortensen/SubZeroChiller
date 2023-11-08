import tkinter as tk
import time
from components.CustomLabel import CustomLabel
from components.IconButton import IconButton

class Timer:
    def __init__(self, parent, root, onTimerEnd):
        self.parent = parent
        self.root = root
        self.time = 1
        self.timeRemaining = 1
        self.running = False
        self.onTimerEnd = onTimerEnd

        frame = tk.Frame(self.parent, bg='#F8F9FA')
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.timeRemainingLabel = CustomLabel(frame, text="Timer")
        self.timeRemainingLabel.pack(side="top", fill="x")

        timerFrame = tk.Frame(frame, bg='#F8F9FA')
        timerFrame.pack(pady=24)

        self.addBtn = IconButton(timerFrame, './assets/add.png', command=self.increaseTime)

        timeFrame = tk.Frame(timerFrame, bg='#F8F9FA')
        self.timeLabel = CustomLabel(timeFrame, fontSize=24)
        self.timeLabel.pack()
        self.minuteLabel = CustomLabel(timeFrame)
        self.minuteLabel.pack()
        self.formatTime()

        self.minusBtn = IconButton(timerFrame, './assets/minimize.png', command=self.decreaseTime)

        self.minusBtn.pack(side=tk.LEFT)
        timeFrame.pack(side=tk.LEFT, padx=48)
        self.addBtn.pack(side=tk.LEFT)

    def formatTime(self):
        self.timeLabel.config(text=f"{self.time}")
        if (self.time > 1):
            self.minuteLabel.config(text='Minutes')
        else:
            self.minuteLabel.config(text='Minute')

    def increaseTime(self):
        self.time += 1
        self.formatTime()

    def decreaseTime(self):
        if self.time <=1:
            return
        self.time -= 1
        self.formatTime()

    def disableControls(self, disable):
        if disable:
            self.addBtn['state'] = 'disabled'
            self.minusBtn['state'] = 'disabled'
        else:
            self.addBtn['state'] = 'normal'
            self.minusBtn['state'] = 'normal'

    def endTimer(self):
        self.running = False
        self.timeRemainingLabel.config(text="Timer")
        self.disableControls(False)

    def formatTimeRemaining(self):
        minutes = "Minutes"
        if self.timeRemaining <= 1:
            minutes = 'Minute'
        self.timeRemainingLabel.config(text=f"Timer - {self.timeRemaining} {minutes} Remaining")

    def updateTimeRemaining(self):
        if self.running == False:
            return
        self.timeRemaining -= 1
        if (self.timeRemaining <= 0):
            self.onTimerEnd()
            self.endTimer()
            return

        self.formatTimeRemaining()
        self.root.after(60 * 1000, self.updateTimeRemaining)

    def startTimer(self):
        self.disableControls(True)
        self.timeRemaining = self.time
        self.running = True
        self.formatTimeRemaining()
        self.root.after(60 * 1000, self.updateTimeRemaining)