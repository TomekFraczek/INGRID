import os
import webbrowser

from json import load

from client.control import doors_open
from client.handlers import handle_open_doors


settings = load(open(os.path.join(os.getcwd(), 'config.json')))


webbrowser.open(settings['index url'])


# Main client loop, keeps the program running indefinitely
while True:

    if not doors_open.is_active:
        handle_open_doors()



