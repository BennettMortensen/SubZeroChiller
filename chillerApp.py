import tkinter as tk
from tkinter import ttk
import RPi.GPIO as GPIO
import time
from components.CustomSwitch import CustomSwitch
from components.Card import Card
from components.IconButton import IconButton
from components.PowerControl import PowerControl
from components.CustomLabel import CustomLabel
from widgets.Blower import Blower
from widgets.PowerLevel import PowerLevel
from widgets.Timer import Timer
from widgets.ChamberTemp import ChamberTemp
from widgets.FloatSensor import FloatSensor
from widgets.TotalTime import TotalTime
from widgets.PowerRange import PowerRange
from widgets.MainConfig import MainConfig
from widgets.DefrostConfig import DefrostConfig

TITLE = "Chiller"
LOGO_PATH = "./assets/logo.png"
PIN_BLOWER = 24
PIN_MAIN = 16
PIN_DEFROST = 25
PIN_FLOAT_SENSOR = 17
PIN_ZEROCROSS = 23
INIT_DELAY = 0.008

class ChillerApp:
    def __init__(self, root):
        self.root = root
        self.holdTImer = None
        self.isConfig = False
        self.lowRange = 1
        self.highRange = 10
        self.delay = INIT_DELAY
        self.zcTimeDiff = 0
        self.lastZcTime = time.time()

        self.setupGpio()
        self.renderMain()

        GPIO.add_event_detect(self.zcPin, GPIO.FALLING, callback=lambda channel: self.onZeroCross(channel, self.delay))

    def setupGpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(24, GPIO.OUT,initial=0)
        GPIO.setup(25, GPIO.OUT,initial=0)
        GPIO.setup(16, GPIO.OUT,initial=0)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(13, GPIO.IN)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def onZeroCross(self, channel, delay):
        if GPIO.input(PIN_BLOWER):
            time.sleep(delay*.5)
            GPIO.output(18,1)
            time.sleep(0.00001)
            GPIO.output(18,0)

            self.zcTimeDiff = time.time() - self.lastZcTime
            self.lastZcTime = time.time()
            if self.isConfig:
                self.defrostConfig.updateZcValue(self.zcTimeDiff)


    def renderMain(self):
        header = tk.Frame(self.root, bg="#F8F9FA", height=96)
        header.pack(side="top", fill="x", padx=4, pady=4)

        logo_img = tk.PhotoImage(file=LOGO_PATH)
        logo_label = tk.Label(header, image=logo_img, bg="#F8F9FA", height=96)
        logo_label.photo = logo_img
        logo_label.pack(side=tk.LEFT, padx=24)

        label = CustomLabel(header, text="Main Dashboard", fontSize=28)
        label.place(relx=0.5, rely=0.5, anchor="center")

        button = IconButton(header, './assets/settings.png', small=True)
        button.pack(side=tk.RIGHT, padx=24)

        button.bind("<ButtonPress-1>", self.configPress)
        button.bind("<ButtonRelease-1>", lambda event: self.root.after_cancel(self.holdTimer))

        main = tk.Frame(self.root, bg="#DEE2E6")
        main.pack(padx=16, pady=16, fill="both", expand=True)

        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)
        main.rowconfigure(2, weight=1)

        card1 = Card(main)
        self.blower = Blower(card1, self.onBlowerChange, PIN_BLOWER)

        card2 = Card(main, row=1)
        self.powerLevel = PowerLevel(card2, low=self.lowRange, high=self.highRange, delay=self.delay, onChange=self.onPowerChange)

        card3 = Card(main, row=2)
        self.timer = Timer(card3, self.root, onTimerEnd=lambda: self.blower.toggleSwitch())

        card4 = Card(main, column=1)
        self.chamberTemp = ChamberTemp(card4, self.root)

        card5 = Card(main, row=1, column=1)
        self.totalTime = TotalTime(card5, self.root)

        card6 = Card(main, row=2, column=1)
        self.floatSensor = FloatSensor(card6, self.root, PIN_FLOAT_SENSOR)

    def renderConfig(self):
        header = tk.Frame(self.root, bg="#F8F9FA")
        header.pack(side="top", fill="x", padx=4, pady=4)

        logo_img = tk.PhotoImage(file=LOGO_PATH)
        logo_label = tk.Label(header, image=logo_img, bg="#F8F9FA", height=96)
        logo_label.photo = logo_img
        logo_label.pack(side=tk.LEFT, padx=24)

        label = CustomLabel(header, text="Configuration", fontSize=28)
        label.place(relx=0.5, rely=0.5, anchor="center")

        button = IconButton(header, './assets/arrow_back.png', small=True, command=lambda: self.changeView('main'))
        button.pack(side=tk.RIGHT, padx=24)

        mainFrame = tk.Frame(self.root)
        mainFrame.pack(fill="both", expand=True)

        mainFrame.columnconfigure(0, weight=1)
        mainFrame.columnconfigure(1, weight=0)
        mainFrame.rowconfigure(0, weight=1)
        mainFrame.rowconfigure(1, weight=1)

        main = tk.Frame(mainFrame, bg="#DEE2E6")
        main.grid(padx=16, pady=(12, 16), row=0, column=0, rowspan=2, sticky='nsew')

        main.columnconfigure(0, weight=2)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)
        main.rowconfigure(2, weight=2)

        mainConfigFrame = tk.Frame(mainFrame, bg="#DEE2E6")
        mainConfigFrame.grid(padx=(0, 16), pady=(12, 16), row=0, column=1, sticky='nsew')

        self.mainConfig = MainConfig(mainConfigFrame, self.root, PIN_MAIN)

        defrostConfigFrame = tk.Frame(mainFrame, bg="#DEE2E6")
        defrostConfigFrame.grid(padx=(0, 16), pady=(0, 16), row=1, column=1, sticky='nsew')

        self.defrostConfig = DefrostConfig(defrostConfigFrame, self.root, PIN_DEFROST, self.zcTimeDiff)

        card1 = Card(main)
        self.blower = Blower(card1, self.onBlowerChange, PIN_BLOWER)

        card2 = Card(main, row=1)
        self.powerLevel = PowerLevel(card2, low=self.lowRange, high=self.highRange, delay=self.delay, onChange=self.onPowerChange)

        card3 = Card(main, row=2)
        self.powerRange = PowerRange(card3, low=self.lowRange, high=self.highRange, onRangeChange=self.onRangeChange)

        card4 = Card(main, column=1)
        self.chamberTemp = ChamberTemp(card4, self.root)

        card5 = Card(main, row=1, column=1)
        self.totalTime = TotalTime(card5, self.root)

        card6 = Card(main, row=2, column=1)
        self.floatSensor = FloatSensor(card6, self.root, PIN_FLOAT_SENSOR)

    def changeView(self, view):
        self.floatSensor.endTimer()
        self.chamberTemp.endTimer()
        for widget in self.root.winfo_children():
            widget.destroy()

        if (view == 'config'):
            self.renderConfig()
            self.isConfig = True
        else:
            self.renderMain()
            self.isConfig = False

    def configPress(self, event):
        self.holdTimer = self.root.after(5000, lambda: self.changeView('config'))

    def onBlowerChange(self, isActive):
        self.powerLevel.disableControls(not isActive)
        if (isActive):
            if self.isConfig:
                self.powerRange.disableControls(True)
            else:
                self.timer.startTimer()
            self.totalTime.startHourCount()
        else:
            if not self.isConfig:
                self.timer.endTimer()
            self.totalTime.endHourCount()

    def onRangeChange(self, low, high):
        print(low, high)
        self.lowRange = low
        self.highRange = high

    def onPowerChange(self, delay):
        self.delay = delay

def main():
    root = tk.Tk()
    root.title(TITLE)
    root.attributes("-fullscreen", True)
    root.configure(bg='#CED4DA', cursor="none")
    ChillerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()