import tkinter as tk
from components.CustomLabel import CustomLabel
import os

TOTAL_FILE = os.path.abspath('total-mins.txt')

class TotalTime:
    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        self.totalTimeMins = self.getTotalMinutes()
        self.timerId = None

        frame = tk.Frame(self.parent, bg='#F8F9FA')
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label = CustomLabel(frame, text="Total Time On")
        label.pack()

        self.hourValueLabel = CustomLabel(frame, text=str(self.totalTimeMins // 60), fontSize=24)
        self.hourValueLabel.pack()

        hours = 'Hours'
        if (self.totalTimeMins // 60 == 1):
            hours = 'Hour'
        self.hourLabel = CustomLabel(frame, text=hours)
        self.hourLabel.pack()

    def startHourCount(self):
        self.timerId = self.root.after(60 * 1000, self.incrementCount)

    def incrementCount(self):
        self.totalTimeMins += 1
        self.hourValueLabel.config(text=str(self.totalTimeMins // 60))
        hours = 'Hours'
        if (self.totalTimeMins // 60 == 1):
            hours = 'Hour'
        self.hourLabel.config(text=hours)
        self.timerId = self.root.after(60 * 1000, self.incrementCount)

    def endHourCount(self):
        if (self.timerId):
            self.root.after_cancel(self.timerId)
        with open(TOTAL_FILE, 'w') as file:
            file.write(str(self.totalTimeMins))

    def getTotalMinutes(self):
        if not os.path.exists(TOTAL_FILE):
            return 0
        with open(TOTAL_FILE, 'r') as file:
            content = file.read()
            return int(content)