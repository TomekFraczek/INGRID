from gpiozero import Button
from json import load
import os

# Load the GPIO pin settings from the settings file.
settings_file = open(os.path.join(os.getcwd(), 'config.json'))
settings = load(settings_file)
gpio_settings = settings['GPIO Pins']

#: sensor that detects if any of the doors are open
doors_open = Button(gpio_settings['door open pin'])
