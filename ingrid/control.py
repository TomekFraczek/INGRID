from gpiozero import OutputDevice, Button
from json import load
from time import sleep
import os

# Load the GPIO pin settings from the settings file.
settings_file = os.path.join(os.getcwd(), 'ingrid', 'static', 'config.json')
settings = load(settings_file)
gpio_settings = settings['GPIO Pins']
time_settings = settings['timing']


class Lock(OutputDevice):

    def __init__(self, locker_num):
        pin = locker_num + gpio_settings["lock start pin"]
        super(Lock, self).__init__(pin)

    def open(self):
        self.on()
        sleep(time_settings["lock open"])
        self.close()


class HangerSensor(Button):

    def __init__(self, locker_num):
        pin = locker_num + gpio_settings["hanger start pin"]
        super(HangerSensor, self).__init__(pin)


