from gpiozero import OutputDevice, Button
from json import load
from time import sleep
import os

# Load the GPIO pin settings from the settings file.
settings_file = os.path.join(os.getcwd(), 'ingrid', 'static', 'config.json')
settings = load(settings_file)
gpio_settings = settings['GPIO Pins']


#: sensor that detects if any of the doors are open
doors_open = Button(gpio_settings['door open pin'])


