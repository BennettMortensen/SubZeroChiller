import tkinter as tk
from components.CustomLabel import CustomLabel
from w1thermsensor import W1ThermSensor as sensor


class ChamberTemp:
    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        self.isCelsius = True
        self.tempValue = 20
        self.timerId = None

        frame = tk.Frame(self.parent, bg='#F8F9FA')
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label = CustomLabel(frame, text="Chamber Temp")
        label.pack()

        self.tempLabel = CustomLabel(frame, text=f"{self.tempValue}\u00b0C", fontSize=24)
        self.tempLabel.pack()

        self.changeLabel = CustomLabel(frame, text="View Fahrenheit", fontSize=16)
        self.changeLabel.config(fg='#0088FF')
        self.changeLabel.pack()

        self.parent.bind("<Button-1>", self.changeView)
        label.bind("<Button-1>", self.changeView)
        self.tempLabel.bind("<Button-1>", self.changeView)
        self.changeLabel.bind("<Button-1>", self.changeView)
        frame.bind("<Button-1>", self.changeView)

        self.getTemp()

    def convertToFahrenheit(self):
        return (self.tempValue * 1.8) + 32

    def changeView(self, event):
        if self.isCelsius:
            self.isCelsius = False
            fValue = self.convertToFahrenheit()
            self.tempLabel.config(text=f"{fValue}\u00b0F")
            self.changeLabel.config(text="View Celsius")
        else:
            self.isCelsius = True
            self.tempLabel.config(text=f"{self.tempValue}\u00b0C")
            self.changeLabel.config(text="View Fahrenheit")

    def getTemp(self):
        tempC = sensor().get_temperature()
        self.tempValue = round(tempC,1)
        if self.isCelsius:
            self.tempLabel.config(text=f"{self.tempValue}\u00b0C")
        else:
            fValue = self.convertToFahrenheit()
            self.tempLabel.config(text=f"{fValue}\u00b0F")
        self.timerId = self.root.after(5000, self.getTemp)

    def endTimer(self):
        if self.timerId:
            self.root.after_cancel(self.timerId)