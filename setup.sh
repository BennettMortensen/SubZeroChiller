#!/bin/sh

# Copy the project into a directory called chiller to the home directory (install git to run clone command)
# Note: after running this command it should prompt you to login to your github account.
sudo apt update
sudo apt install git
git clone https://github.com/BennettMortensen/SubZeroChiller.git chiller

# Change the startup image.
# Note: This command only works if the image is in the assets folder and named splash.png
#       otherwise you'll just need to replace the splash.png in the /usr/share/plymouth/themes/pix/ directory
#       with a file of the same name.
sudo cp chiller/assets/splash.png /usr/share/plymouth/themes/pix/splash.png

#w1thermsensor
pip install w1thermsensor --break-system-packages
sudo nano /boot/firmware/config.txt
dtoverlay=w1-gpio,gpiopin=4



# Set the app to run on startup
# Note: /home/bmorty23/chiller/chillerApp.py may be a different path on a different raspberryPi. I think the default
#       is something along these lines: /home/pi/chiller/chillerApp.py.
#sudo nano /etc/xdg/autostart/display.desktop
echo -e "[Desktop Entry]\nName=Chiller\nExec=/usr/bin/python3 /home/bmorty23/chiller/chillerApp.py" | sudo tee /etc/xdg/autostart/display.desktop

# Reboot to make sure everything is setup correctly
sudo reboot
