import django
import os
import progressbar

from random import choice, randint

from django.contrib.auth.models import User
from .ingridbackend.models import Locker, Wetsuit

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'INGRID.settings')
django.setup()

ADMIN_RFID = '0000000000'
SYSTEM_RFID = '1111111111'
PASSWORD = 'admin'

used_rfids = [ADMIN_RFID, SYSTEM_RFID]

RFIDS_TO_HAND_OUT = ['1000000000', '2000000000', '3000000000', '4000000000', '5000000000', '6000000000', '7000000000']


def gen_rfid():
    """generates a random and unique rfid"""
    rfid = str(randint(1000000000, 9999999999))
    if rfid in used_rfids:
        rfid = gen_rfid()
    else:
        used_rfids.append(rfid)
    return rfid


# Add the master admin  and excursion system accounts
admin = User.objects.create_superuser("admin",
                                      "admin@excursionclubucsb.org",
                                      "admin")

# Add Lockers
print('Making lockers and wetsuits...')
num_lockers = 20
genders = ["M", "W", "U"]
sizes = ["S", "M", "L", "XL"]
bar = progressbar.ProgressBar()
for i in bar(range(num_lockers)):
    wetsuit = Wetsuit(rfid=gen_rfid(), gender=choice(genders), size=choice(sizes))
    wetsuit.save()

    locker_id = i + 1
    locker = Locker(locker_id=locker_id, wetsuit=wetsuit)
    locker.save()

print('')
print("DONE!")
