import os
import time
import webbrowser

from json import load

from client.control import doors_open
from client.handlers import handle_open_doors

settings = load(open(os.path.join(os.getcwd(), 'config.json')))
time_settings = settings['timing']

webbrowser.open(settings['index url'])

# Main client loop, keeps the program running indefinitely
while True:

    time.sleep(time_settings['door check interval'])
    print("Door state in main loop: {}".format(doors_open.is_active))

    if not doors_open.is_active:
        handle_open_doors()
