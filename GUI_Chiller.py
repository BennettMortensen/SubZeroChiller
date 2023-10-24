from guizero import App, Box, Text, PushButton, Slider
import RPi.GPIO as GPIO
import time
import math
import threading
from w1thermsensor import W1ThermSensor as sensor

try:

    #coutner code
    def counter():
        text.value = int(text.value)+1
        
    #zerocross average
    def on_zero_cross(channel):
        if GPIO.input(24):
            global zc_count, zc_time_sum, last_zc_time, zc_time_avg, delay
            
            time.sleep(delay*.5)
            GPIO.output(18,1)
            time.sleep(0.00001)
            GPIO.output(18,0)

                             
            
            zc_count += 1
            zc_time_diff = time.time() - last_zc_time
            last_zc_time = time.time()
            zc_time_sum += zc_time_diff
        
            #cal average
            zc_time_avg = zc_time_sum / zc_count
            average.value = round(zc_time_diff,5)
            
                

            
        

    #bar increase / decrease
    def increase_blower(pin):
        global delay
        value=int(bar.value)
        if value < 10 and GPIO.input(pin) and pin == 24:
            value += 1
            bar.value = int(value)
            value_text.value = str(round(0.0088-(0.0008*value),4))
            update_slider_color()
            delay = round(0.0088-(0.0008*value),4)
            
            
            
    def decrease_blower(pin):
        global delay
        value=int(bar.value)
        if value > 1 and GPIO.input(pin) and pin == 24:
            value -= 1
            bar.value = int(value)
            value_text.value = str(round(0.0088-(0.0008*value),4))
            update_slider_color()
            delay = round(0.0088-(0.0008*value),4)
            
            
    # color gradient for bar
    def update_slider_color():
        value = int(bar.value)
        gradient_colors = ['#0072B2', '#2D708E', '#5D5E8F', '#8A5586', '#BF4D6F', '#EE4E58', '#FF6A4C', '#FFA05D', '#FFC28D', '#FFE0B2']
        index = int((value/10)*(len(gradient_colors) - 1))
        bar.bg = gradient_colors[index]
            

    # Function to toggle the switch and change the color
    def toggle_switch(pin, button):
        global delay
        if GPIO.input(pin) and pin == 16:
            GPIO.output(pin, 0)
            button.bg = "red"
            timeon.value = int(text.value)
            text.value = 0
        elif GPIO.input(pin)==False and pin == 24:
            GPIO.output(pin, 1)
            button.bg = "green"
            bar.value = 1
            bar.bg = '#0072B2'
            value_text.value = .008
            delay = 0.008
        elif GPIO.input(pin) and pin == 24:
            GPIO.output(pin, 0)
            button.bg = "red"
            bar.value = 1
            bar.bg = '#0072B2'
            value_text.value = .008
            delay = 0.008
            GPIO.output(18, 0)
        elif GPIO.input(pin)==False and pin == 16:
              GPIO.output(pin, 1)
              button.bg = "green"
              text.value = 0
        elif GPIO.input(pin):
              GPIO.output(pin, 0)
              button.bg = "red"
        else:
            GPIO.output(pin, 1)
            button.bg = "green"
            


    def FloatSense():
        while 1<2:
            if GPIO.input(17) == GPIO.LOW:
                floatsense.bg = "#0072B2"
                temp_c=sensor().get_temperature()
                tempc.value=str(round(temp_c,1))+" C"
            else:
                floatsense.bg = "red"
                temp_c=sensor().get_temperature()
                tempc.value=str(round(temp_c,1))+" C"
        time.sleep(1000)
        
    TempThread = threading.Thread(target=FloatSense)
        
    def TempThreadCall():
        TempThread.start()
        
           
    

    app = App(title="Toggle Switches")
    app.set_full_screen()

    # Set up the GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(24, GPIO.OUT,initial=0)
    GPIO.setup(25, GPIO.OUT,initial=0)
    GPIO.setup(16, GPIO.OUT,initial=0)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(13, GPIO.IN)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)



    # Create a box to hold the toggle switches
    center_box = Box(app,layout="grid")

    # Create the toggle switches
    blower_switch = PushButton(center_box, grid=[0,0], text="Blower", align="left",width=30,height=10, command=lambda: toggle_switch(24, blower_switch))
    blower_switch.bg = "red"
    defrost_switch = PushButton(center_box, grid=[1,0], text="Defrost", align="left",width=30,height=10, command=lambda: toggle_switch(25, defrost_switch))
    defrost_switch.bg = "red"
    main_switch = PushButton(center_box, grid=[2,0], text="Main", align="left",width=30,height=10, command=lambda: toggle_switch(16, main_switch))
    main_switch.bg = "red"
    bar = Slider(center_box,grid=[0,1],start=1,end=10,align="center",width=200, height=30, horizontal=True)
    bar.value = 1
    bar.bg = '#0072B2'
    up_button = PushButton(center_box,grid=[0,2],text="\u25B2", align="center",width=10,height=7,command=lambda: increase_blower(24))
    down_button = PushButton(center_box,grid=[0,3],text="\u25BC", align="center",width=10,height=7,command=lambda: decrease_blower(24))
    value_text = Text(center_box,grid=[0,4],text="0.008",align="left",width=30, height=10)


    text = Text(center_box, grid=[2,2],text="1")
    text.repeat(1000,counter)
    timeon = Text(center_box, grid=[2,4],text="0")

    time_on_off = Text(center_box, grid=[2,1],text="Time Elapsed (s)")
    ltot = Text(center_box, grid=[2,3],text="Last Time ON Total (s)")
    average = Text(center_box, grid=[1,1],text="0")
    
    
    tempc = Text(center_box, grid=[1,2],text="20.0 C")
    
    floatsense = Text(center_box, grid=[1,3],text="FLOAT SENSOR")
    floatsense.bg = "#0072B2"
    TempThreadCall()

    
    zc_count = 0
    zc_time_sum = 0
    zc_time_avg = 0
    previous_time = 0
    last_zc_time = time.time()
    delay = 0.008
    GPIO.add_event_detect(23, GPIO.FALLING, callback=on_zero_cross)
    

    app.display()

except KeyboardInterrupt:
    GPIO.cleanup()
