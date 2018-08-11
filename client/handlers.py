import os
import time
import webbrowser

from json import load
from datetime import datetime
from playsound import playsound
from client.control import doors_open

settings = load(open(os.path.join(os.getcwd(), 'config.json')))
audio_settings = settings['audio']
time_settings = settings['timing']

close_door_sound_path = os.path.join(os.getcwd(), audio_settings['close door sound'])


def handle_open_doors():
    opened_at = datetime.now()
    time_allowed_open = time_settings['doors open patience']

    # Keep looping until all doors are closed
    while not doors_open.is_active:

        print("doors active: {}".format(doors_open.is_active))

        time_open = datetime.now() - opened_at

        # If the door has been open too long, yell to close it
        if time_open.total_seconds() > time_allowed_open:
            # playsound(close_door_sound_path)
            time.sleep(time_settings['wait between yells'])
            continue

        time.sleep(time_settings['door check interval'])

    # Tell the server to check that all expected wetsuits are present
    webbrowser.open(settings['door close url'])
