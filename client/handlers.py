import os
import time
import webbrowser

from json import load
from datetime import datetime
from playsound import playsound
from client.control import doors_open, HangerSensor


settings = load(os.path.join(os.getcwd(), 'config.json'))
audio_settings = settings['audio']
time_settings = settings['timing']

close_door_sound_path = os.path.join(os.getcwd(), audio_settings['close door sound'])


def handle_open_doors():

    opened_at = datetime.now()

    while True:

        # If the doors have been closed, then break out of this loop
        if doors_open.is_active:
            webbrowser.open(settings['door close url'])
            break

        # If the door has been open too long yell to close it
        time_open = datetime.now() - opened_at
        time_allowed_open = time_settings['door open patience']
        if time_open.total_seconds() > time_allowed_open:
            playsound(close_door_sound_path)
            time.sleep(time_settings['wait between yells'])
            continue
