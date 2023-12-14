import tkinter as tk
import RPi.GPIO as GPIO
from components.CustomLabel import CustomLabel
import os

class FloatSensor:
    def __init__(self, parent, root, pin):
        self.parent = parent
        self.root = root
        self.pin = pin
        self.goodIcon = tk.PhotoImage(file=os.path.abspath('chiller/assets/check.png'))
        self.fullIcon = tk.PhotoImage(file=os.path.abspath('chiller/assets/warning.png'))
        self.status = 'Good'
        self.timerId = None

        frame = tk.Frame(self.parent, bg='#F8F9FA')
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        floatSensor = CustomLabel(frame, text="Float Sensor")
        floatSensor.pack()

        self.statusIcon = tk.Label(frame, bg="#F8F9FA")
        self.statusIcon.pack()

        self.statusLabel = CustomLabel(frame)
        self.statusLabel.pack()

        self.updateSensorStatus('Good')
        self.getSensorStatus()

    def updateSensorStatus(self, status):
        self.statusLabel.config(text=status)
        if status == "Good":
            self.statusIcon.config(image=self.goodIcon)
            self.statusIcon.photo = self.goodIcon
        else:
            self.statusIcon.config(image=self.fullIcon)
            self.statusIcon.photo = self.fullIcon

    def getSensorStatus(self):
        if GPIO.input(17) == GPIO.LOW:
            if self.status == 'Good':
                return
            self.status = 'Good'
            self.updateSensorStatus('Good')
        else:
            if self.status == 'Full':
                return
            self.status = 'Full'
            self.updateSensorStatus('Full')
        self.timerId = self.root.after(1000, self.getSensorStatus)

    def endTimer(self):
        if self.timerId:
            self.root.after_cancel(self.timerId)
